import axios, { AxiosInstance } from "axios";
import * as cheerio from "cheerio";

const SPARQL_ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql";
const EURLEX_BASE = "https://eur-lex.europa.eu";
const MAX_RETRIES = 3;

const PREFIXES = `
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
`;

interface SparqlBinding {
  value: string;
  type: string;
}

interface SparqlResult {
  results: { bindings: Array<Record<string, SparqlBinding>> };
}

export class EurLexClient {
  private client: AxiosInstance;
  private lastRequest = 0;

  constructor() {
    this.client = axios.create({ timeout: 60000, headers: { "User-Agent": "LegalResearchMCP/1.0" } });
  }

  private async rateLimit(): Promise<void> {
    const wait = Math.max(0, 1000 - (Date.now() - this.lastRequest));
    if (wait > 0) await new Promise(r => setTimeout(r, wait));
    this.lastRequest = Date.now();
  }

  private async retry<T>(fn: () => Promise<T>): Promise<T> {
    for (let i = 0; i <= MAX_RETRIES; i++) {
      try { return await fn(); } catch (e) {
        if (i < MAX_RETRIES) { await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i))); continue; }
        throw e;
      }
    }
    throw new Error("Max retries");
  }

  async executeSparql(query: string): Promise<Array<Record<string, string>>> {
    await this.rateLimit();
    return this.retry(async () => {
      const fullQuery = PREFIXES + query;
      const resp = await this.client.get<SparqlResult>(SPARQL_ENDPOINT, {
        params: { query: fullQuery },
        headers: { Accept: "application/sparql-results+json" },
      });
      return resp.data.results.bindings.map(binding => {
        const row: Record<string, string> = {};
        for (const [key, val] of Object.entries(binding)) { row[key] = val.value; }
        return row;
      });
    });
  }

  async searchLegislation(keyword: string, docType: string, yearFrom: number, yearTo: number, limit: number, offset: number): Promise<Array<Record<string, string>>> {
    const typeFilter = docType === "all" ? "" : `FILTER(CONTAINS(LCASE(STR(?type)), "${docType.toLowerCase()}"))`;
    const query = `
SELECT DISTINCT ?celex ?title ?date ?type ?eli WHERE {
  ?work cdm:resource_legal_id_celex ?celex .
  ?work cdm:work_date_document ?date .
  OPTIONAL { ?work cdm:resource_legal_type ?type }
  OPTIONAL { ?work cdm:resource_legal_eli ?eli }
  ?exp cdm:expression_belongs_to_work ?work .
  ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
  ?exp cdm:expression_title ?title .
  FILTER(STRSTARTS(?celex, "3"))
  FILTER(CONTAINS(LCASE(?title), LCASE("${keyword}")))
  FILTER(?date >= "${yearFrom}-01-01"^^xsd:date)
  FILTER(?date <= "${yearTo}-12-31"^^xsd:date)
  ${typeFilter}
}
ORDER BY DESC(?date)
LIMIT ${limit}
OFFSET ${offset}`;
    return this.executeSparql(query);
  }

  async searchCaselaw(keyword: string, yearFrom: number, yearTo: number, limit: number, offset: number): Promise<Array<Record<string, string>>> {
    const query = `
SELECT DISTINCT ?celex ?title ?date ?ecli WHERE {
  ?work cdm:resource_legal_id_celex ?celex .
  ?work cdm:work_date_document ?date .
  OPTIONAL { ?work cdm:case_law_ecli ?ecli }
  ?exp cdm:expression_belongs_to_work ?work .
  ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
  ?exp cdm:expression_title ?title .
  FILTER(STRSTARTS(?celex, "6"))
  FILTER(CONTAINS(LCASE(?title), LCASE("${keyword}")))
  FILTER(?date >= "${yearFrom}-01-01"^^xsd:date)
  FILTER(?date <= "${yearTo}-12-31"^^xsd:date)
}
ORDER BY DESC(?date)
LIMIT ${limit}
OFFSET ${offset}`;
    return this.executeSparql(query);
  }

  /**
   * Convert ECJ case number (e.g. "C-83/14", "T-419/03") to CELEX format.
   * Tries multiple document types: CJ (Judgment), CC (AG Opinion), CO (Order).
   * Returns ARRAY of candidate CELEX numbers to probe.
   */
  caseNumberToCelexCandidates(caseNumber: string): string[] {
    // Match: C-83/14, T-419/03, F-1/05, C-83/14 P (P for appeal stays in case_no)
    const match = caseNumber.match(/([CTFcftCT]+)\s*-?\s*(\d+)\s*\/\s*(\d{2,4})/);
    if (!match) return [];
    const [, courtRaw, caseNoRaw, yearRaw] = match;
    const court = courtRaw.toUpperCase();
    const caseNo = caseNoRaw.padStart(4, "0");
    let year = yearRaw;
    if (year.length === 2) {
      const n = parseInt(year);
      year = (n >= 50 ? "19" : "20") + year;
    }
    const courtPrefix = court === "C" ? ["CJ", "CC", "CO"] : court === "T" ? ["TJ", "TO"] : court === "F" ? ["FJ", "FO"] : ["CJ"];
    return courtPrefix.map(t => `6${year}${t}${caseNo}`);
  }

  /**
   * Find a CJEU case by case number (e.g. "C-83/14") — tries CELEX candidates one by one.
   */
  async findCaseByNumber(caseNumber: string): Promise<Record<string, string> | null> {
    const candidates = this.caseNumberToCelexCandidates(caseNumber);
    for (const celex of candidates) {
      const meta = await this.getDocumentByCelex(celex);
      if (meta.title) return { ...meta, celex };
    }
    return null;
  }

  async getDocumentByCelex(celexNumber: string): Promise<Record<string, string>> {
    const query = `
SELECT ?title ?date ?type ?eli WHERE {
  ?work cdm:resource_legal_id_celex "${celexNumber}" .
  ?work cdm:work_date_document ?date .
  OPTIONAL { ?work cdm:resource_legal_type ?type }
  OPTIONAL { ?work cdm:resource_legal_eli ?eli }
  ?exp cdm:expression_belongs_to_work ?work .
  ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
  ?exp cdm:expression_title ?title .
}
LIMIT 1`;
    const results = await this.executeSparql(query);
    return results[0] ?? {};
  }

  async fetchDocumentHtml(celexNumber: string, language: string = "EN"): Promise<string> {
    await this.rateLimit();
    return this.retry(async () => {
      const url = `${EURLEX_BASE}/legal-content/${language}/TXT/HTML/?uri=CELEX:${celexNumber}`;
      const resp = await this.client.get<string>(url);
      const $ = cheerio.load(resp.data);
      $("script, style, nav, header, footer").remove();
      const text = $("body").text().replace(/\s+/g, " ").trim();
      return text;
    });
  }
}
