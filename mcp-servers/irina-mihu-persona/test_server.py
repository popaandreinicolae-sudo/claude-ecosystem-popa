"""
Test rapid pentru irina-mihu-persona: verifica incarcarea continutului,
helperele de regasire si listarea capabilitatilor MCP (prompts/resources/tools).
Ruleaza: python test_server.py
"""

import asyncio

import server as s


def check_content() -> None:
    assert s.PERSONA_BODY.strip(), "corp persona gol"
    assert "Irina Mihu" in s.PERSONA_RAW
    assert s.PROFIL and s.CANON and s.SURSE and s.SABLOANE
    print("[ok] continut incarcat: persona + 4 fisiere de cunoastere")


def check_templates() -> None:
    genuri = ["nota-verbala", "telegrama", "fisa-dosar", "elemente-de-limbaj",
              "non-paper", "raport-misiune", "fisa-tara"]
    for g in genuri:
        t = s._extract_template(g)
        assert t and t.startswith("##"), f"sablon lipsa: {g}"
    print(f"[ok] {len(genuri)} sabloane extrase corect")


def check_tools_logic() -> None:
    r = s.search_knowledge("COREPER ECOFIN", max_results=3)
    assert "[" in r and "COREPER" in r.upper() or "ecofin" in r.lower()
    src = s.get_source("Viena 1961")
    assert "Viena" in src
    rg = s.research_guidance("diplomatie cibernetica Israel")
    assert "DOMENII RELEVANTE" in rg
    assert "diplomatie-cibernetica" in rg
    print("[ok] tools: search_knowledge, get_source, research_guidance")


async def check_mcp_surface() -> None:
    tools = await s.mcp.list_tools()
    resources = await s.mcp.list_resources()
    prompts = await s.mcp.list_prompts()
    print(f"[ok] MCP expune: {len(tools)} tools, {len(resources)} resources, "
          f"{len(prompts)} prompts")
    print("     tools:    ", ", ".join(t.name for t in tools))
    print("     resources:", ", ".join(str(r.uri) for r in resources))
    print("     prompts:  ", ", ".join(p.name for p in prompts))
    assert len(tools) >= 6 and len(resources) >= 5 and len(prompts) >= 4


def main() -> None:
    check_content()
    check_templates()
    check_tools_logic()
    asyncio.run(check_mcp_surface())
    print("\nTOATE TESTELE AU TRECUT.")


if __name__ == "__main__":
    main()
