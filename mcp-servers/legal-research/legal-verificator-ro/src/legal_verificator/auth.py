"""Lege5.ro / Lege6.ro session management with form-based authentication."""

import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger("legal-verificator.auth")

LEGE5_BASE = "https://lege5.ro"
LEGE5_LOGIN_URL = f"{LEGE5_BASE}/Authentication/Login"

LEGE6_BASE = "https://lege6.ro"
LEGE6_LOGIN_URL = f"{LEGE6_BASE}/account/login"

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


class Lege5Session:
    """Manages authenticated session with lege5.ro."""

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._authenticated = False
        self._email = os.environ.get("LEGE5_EMAIL", "")
        self._password = os.environ.get("LEGE5_PASSWORD", "")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers=BROWSER_HEADERS,
                follow_redirects=True,
                timeout=30.0,
            )
        return self._client

    async def login(self) -> bool:
        """Authenticate with lege5.ro using form-based login."""
        if not self._email or not self._password:
            logger.warning("Lege5 credentials not configured (LEGE5_EMAIL/LEGE5_PASSWORD)")
            return False

        client = await self._get_client()

        try:
            # GET the login page to get cookies and default form values
            resp = await client.get(LEGE5_LOGIN_URL)

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")

            # Build form data from actual form inputs (preserves hidden field defaults)
            form = soup.find("form", {"action": "/Authentication/Login"})
            login_data = {}
            if form:
                for inp in form.find_all("input"):
                    name = inp.get("name", "")
                    if name:
                        login_data[name] = inp.get("value", "")

            # Override email and password with our credentials
            login_data["Login.Mail"] = self._email
            login_data["Login.Password"] = self._password

            # Ensure required hidden fields have valid defaults
            login_data.setdefault("Login.IsMetro", "False")
            login_data.setdefault("Login.RequireCaptcha", "False")
            login_data.setdefault("Login.JsEncrypt", "False")

            resp = await client.post(
                LEGE5_LOGIN_URL,
                data=login_data,
                headers={
                    **BROWSER_HEADERS,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": LEGE5_LOGIN_URL,
                    "Origin": LEGE5_BASE,
                },
            )

            # Check if login succeeded (no redirect to login page)
            if "/Authentication/Login" not in str(resp.url) and resp.status_code == 200:
                self._authenticated = True
                logger.info("Lege5.ro login successful")
                return True
            else:
                logger.error("Lege5.ro login failed — check credentials")
                return False

        except Exception as e:
            logger.error("Lege5.ro login error: %s", e)
            return False

    async def ensure_authenticated(self) -> bool:
        """Ensure we have a valid session, re-authenticate if needed."""
        if self._authenticated:
            return True
        return await self.login()

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Authenticated GET request with auto-reauth on redirect to login."""
        client = await self._get_client()
        resp = await client.get(url, **kwargs)

        # If redirected to login, re-authenticate and retry
        if "/Authentication/Login" in str(resp.url) or "/Account/Login" in str(resp.url):
            logger.info("Session expired, re-authenticating...")
            self._authenticated = False
            if await self.login():
                resp = await client.get(url, **kwargs)

        return resp

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Authenticated POST request with auto-reauth."""
        client = await self._get_client()
        resp = await client.post(url, **kwargs)

        if "/Authentication/Login" in str(resp.url) or "/Account/Login" in str(resp.url):
            self._authenticated = False
            if await self.login():
                resp = await client.post(url, **kwargs)

        return resp

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None


class Lege6Session:
    """Manages authenticated session with lege6.ro (Indaco Systems modern platform)."""

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._authenticated = False
        self._email = os.environ.get("LEGE6_EMAIL", "") or os.environ.get("LEGE5_EMAIL", "")
        self._password = os.environ.get("LEGE6_PASSWORD", "") or os.environ.get("LEGE5_PASSWORD", "")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers=BROWSER_HEADERS,
                follow_redirects=True,
                timeout=45.0,
            )
        return self._client

    async def login(self) -> bool:
        """Authenticate with lege6.ro using ASP.NET Core Identity form login."""
        if not self._email or not self._password:
            logger.warning("Lege6 credentials not configured (LEGE6_EMAIL/LEGE6_PASSWORD)")
            return False

        client = await self._get_client()

        try:
            from bs4 import BeautifulSoup

            resp = await client.get(LEGE6_LOGIN_URL)
            soup = BeautifulSoup(resp.text, "html.parser")

            form = (
                soup.find("form", {"action": "/account/login"}) or
                soup.find("form", {"action": "/Account/Login"}) or
                soup.find("form", id="account") or
                soup.find("form")
            )

            login_data = {}
            if form:
                for inp in form.find_all("input"):
                    name = inp.get("name", "")
                    if name:
                        login_data[name] = inp.get("value", "")

            email_keys = ("Input.Email", "Email", "Login.Email", "Login.Mail", "username")
            password_keys = ("Input.Password", "Password", "Login.Password", "password")
            for k in email_keys:
                if k in login_data:
                    login_data[k] = self._email
                    break
            else:
                login_data["Input.Email"] = self._email
            for k in password_keys:
                if k in login_data:
                    login_data[k] = self._password
                    break
            else:
                login_data["Input.Password"] = self._password

            login_data.setdefault("Input.RememberMe", "true")

            action = form.get("action") if form else "/account/login"
            post_url = f"{LEGE6_BASE}{action}" if action and action.startswith("/") else (action or LEGE6_LOGIN_URL)

            resp = await client.post(
                post_url,
                data=login_data,
                headers={
                    **BROWSER_HEADERS,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": LEGE6_LOGIN_URL,
                    "Origin": LEGE6_BASE,
                },
            )

            final_url = str(resp.url).lower()
            login_failed = ("/account/login" in final_url) or ("/account/register" in final_url)
            if not login_failed and resp.status_code in (200, 302):
                self._authenticated = True
                logger.info("Lege6.ro login successful")
                return True
            logger.error("Lege6.ro login failed (status %s, final URL %s)", resp.status_code, final_url)
            return False

        except Exception as e:
            logger.error("Lege6.ro login error: %s", e)
            return False

    async def ensure_authenticated(self) -> bool:
        if self._authenticated:
            return True
        return await self.login()

    async def get(self, url: str, **kwargs) -> httpx.Response:
        client = await self._get_client()
        resp = await client.get(url, **kwargs)
        if "/account/login" in str(resp.url).lower():
            logger.info("Lege6 session expired, re-authenticating...")
            self._authenticated = False
            if await self.login():
                resp = await client.get(url, **kwargs)
        return resp

    async def post(self, url: str, **kwargs) -> httpx.Response:
        client = await self._get_client()
        resp = await client.post(url, **kwargs)
        if "/account/login" in str(resp.url).lower():
            self._authenticated = False
            if await self.login():
                resp = await client.post(url, **kwargs)
        return resp

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
