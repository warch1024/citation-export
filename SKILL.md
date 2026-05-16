---
name: citation-export
version: "2.1"
description: Use this skill when the user provides academic paper titles, DOIs, or PMIDs and wants to generate citation files in EndNote (.enw), RIS (.ris), or RIS+ format. Supports single papers or batch processing of multiple references. Automatically searches 47+ academic databases and platforms across biomedical, engineering, social sciences, Chinese literature, patents, standards, preprints, and open access repositories to retrieve complete bibliographic metadata. ENW/RIS formats comply with official specifications (EndNote X6 tag map, RIS 2011 spec).
---

# Citation Export Skill (v2.1)

## Overview

This skill generates citation files from academic paper titles, DOIs, or PMIDs. It supports multiple output formats (EndNote .enw, RIS .ris, RIS+) and can process single papers or batches of references. The skill automatically searches 40+ academic databases and platforms to retrieve complete bibliographic metadata including authors, journal, year, volume, issue, pages, DOI, PMID, abstract, keywords, and more.

## Supported Output Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| EndNote | `.enw` | EndNote tagged format (RIS/EndNote Tagged) |
| RIS | `.ris` | Research Information Systems format |
| RIS+ | `.ris` | Extended RIS with additional fields (abstract, keywords, PMCID) |

## Workflow

### Step 1: Understand User Requirements

When a user requests citation files, identify:

- **Input type**: Paper titles, DOIs, PMIDs, patent numbers, standard numbers, or other identifiers
- **Number of papers**: Single paper or batch
- **Output format**: EndNote (.enw), RIS (.ris), or RIS+
- **Output location**: Where to save the files (default: workspace folder)
- **Language hint**: Chinese or English title (determines database priority)

### Step 2: Classify the Paper and Select Databases

Based on the paper topic, language, and type, select the appropriate database category:

| Paper Type / Domain | Primary Databases | Secondary / Fallback |
|---------------------|-------------------|----------------------|
| Biomedical / Life Sciences | PubMed, PubMed Central (PMC), Cochrane Library | CrossRef, Semantic Scholar, Google Scholar |
| Chinese journal articles | CNKI, 万方, 维普, PubScholar | NSTL, 读秀, 国家哲学社会科学文献中心 |
| Engineering / CS / Physics | IEEE Xplore, ACM DL, SpringerLink, ScienceDirect | CrossRef, Semantic Scholar, Scopus |
| Social Sciences / Humanities | SSRN, JSTOR, 国家哲学社会科学文献中心 | Google Scholar, Dimensions, OpenAlex |
| Conference papers | IEEE Xplore (conferences), CPCI, ACM DL | Google Scholar, Semantic Scholar |
| Preprints | bioRxiv, ChemRxiv, EarthArXiv, SSRN, PSSXiv | CrossRef (after publication) |
| Patents | USPTO, EPO, Derwent Innovations Index | Google Patents, WIPO |
| Standards | ISO | IEC, IEEE Standards,国家标准全文公开系统 |
| Theses / Dissertations | ProQuest, CALIS | 万方学位论文, NSTL |
| Open Access papers | DOAJ, PubMed Central OA, CORE | Unpaywall, DOAB |
| General / Unknown | CrossRef, Google Scholar, Semantic Scholar | OpenAlex, Dimensions |

### Step 3: Search and Retrieve Metadata

#### Search Priority by Input Type

```
For each paper:
1. If DOI provided → CrossRef lookup (fastest, most reliable)
2. If PMID provided → Direct PubMed / PMC lookup
3. If patent number → USPTO / EPO / Derwent lookup
4. If standard number → ISO lookup
5. If title only → Follow domain-specific search strategy below
```

#### Domain-Specific Search Strategy

**Biomedical papers:**
1. PubMed (PMID / title search)
2. PubMed Central (PMC full-text metadata)
3. Cochrane Library (systematic reviews)
4. CrossRef API (DOI / title)
5. Semantic Scholar API
6. Google Scholar (fallback)

**Chinese papers (中文文献):**
1. CNKI 中国知网 (title / author / DOI)
2. 万方数据 (title / author)
3. 维普中文科技期刊 (title / author)
4. PubScholar (开放获取)
5. 国家哲学社会科学文献中心 (社科类)
6. NSTL 国家科技图书文献中心
7. 读秀学术搜索 (图书章节)
8. Google Scholar (fallback)

**Engineering / CS papers:**
1. IEEE Xplore (title / DOI)
2. ACM Digital Library (title / DOI)
3. SpringerLink (title / DOI)
4. Elsevier ScienceDirect (title / DOI)
5. CrossRef API
6. Semantic Scholar API
7. Google Scholar (fallback)

**Social Sciences / Humanities:**
1. SSRN (preprints and working papers)
2. JSTOR (archived journals)
3. 国家哲学社会科学文献中心 (Chinese)
4. Google Scholar
5. Dimensions
6. OpenAlex

**Conference papers:**
1. IEEE Xplore Conference Proceedings
2. CPCI (Conference Proceedings Citation Index)
3. ACM Digital Library
4. Google Scholar
5. Semantic Scholar

**Preprints:**
1. arXiv (physics, math, CS, EE, statistics)
2. bioRxiv (biology / health)
3. medRxiv (medicine / health)
4. ChemRxiv (chemistry)
5. EarthArXiv (earth science)
6. SSRN (social science / business / law)
7. PSSXiv (political science)
8. CrossRef (check if published version exists)

**Patents:**
1. USPTO (US patents)
2. EPO (European patents)
3. Derwent Innovations Index (enhanced patent data)
4. Google Patents (fallback)

**Standards:**
1. ISO (international standards)
2. IEEE Standards
3. 国家标准全文公开系统 (Chinese GB standards)

**Theses / Dissertations:**
1. ProQuest Dissertations & Theses Global
2. CALIS 高校学位论文库 (Chinese)
3. 万方学位论文 (Chinese)
4. NSTL

**Open Access:**
1. DOAJ (open access journals)
2. PubMed Central OA
3. CORE (open access research)
4. DOAB (open access books)
5. Unpaywall (OA link finder)

**General / Cross-domain:**
1. CrossRef API (DOI / title — best first step for any DOI)
2. Semantic Scholar API (title search)
3. Google Scholar (universal fallback)
4. OpenAlex (open metadata, very broad coverage)
5. Dimensions (linked research data)
6. DataCite (datasets, software, preprints)
7. Web of Science (WOS) — via institutional access
8. Scopus — via institutional access

### Step 4: Extract Metadata Fields

For each successfully found paper, extract:
- **Required**: title, authors, journal/source, year
- **Important**: volume, issue, pages, DOI
- **Extended**: PMID, PMCID, abstract, keywords, ISSN, publisher, language
- **Optional**: funding info, affiliations, references count, citation count

### Step 5: Generate Citation File

Based on user's requested format, generate the appropriate file.

#### EndNote Format (.enw)

Based on EndNote X6 export data (reverse-engineered tag map). Key tags:

```
%0 [Reference Type]          -- Must be first line (e.g., "Journal Article", "Conference Paper", "Thesis", "Patent", "Standard")
%T [Title]
%A [Author1 Last, First]     -- One per line
%A [Author2 Last, First]
%J [Journal Name]            -- For Journal Article type only
%B [Secondary Title]         -- For other types (book title, conference name)
%D [Year]
%V [Volume]
%N [Issue]
%P [Pages]
%@ [ISSN / ISBN]
%I [Publisher]
%X [Abstract]
%K [Keywords]
%R [DOI]                     -- Official DOI tag (NOT %U or %6)
%U [URL]                     -- Web link (NOT DOI URL)
%G [Language]
%Z [Notes]
%2 [PMCID]                   -- Custom 2 field
%M [PMID / Accession Number] -- Accession Number
```

**Common %0 Reference Types**: Journal Article, Conference Paper, Conference Proceedings, Book, Book Section, Thesis, Patent, Standard, Electronic Article, Report, Dataset, Computer Program, Web Page, Magazine Article, Newspaper Article, Blog, Manuscript, Generic

#### RIS Format (.ris)

Based on RIS specification (2001/2011, originally by Research Information Systems). Key rules:
- `TY` must be first line, `ER` must be last line
- Format: `XX  - value` (two-letter tag + two spaces + hyphen + space + value)
- `AU`, `KW`, `UR` can repeat; all others are single-use

```
TY  - [Type]                   -- Must be first line
TI  - [Title]
AU  - [Author1 Last, First]    -- One per line
AU  - [Author2 Last, First]
JO  - [Journal Full Name]      -- For journal articles (official journal tag)
T2  - [Secondary Title]        -- Journal/Book/Conference name (context-dependent)
PY  - [Year]                   -- Format: YYYY/MM/DD (year-only also accepted)
VL  - [Volume]
IS  - [Issue]
SP  - [Start Page]
EP  - [End Page]
SN  - [ISSN / ISBN]
PB  - [Publisher]
AB  - [Abstract]
KW  - [Keywords]               -- One per line
DO  - [DOI]                    -- Official DOI field
UR  - [URL]                    -- Web link (NOT DOI URL)
LA  - [Language]
ER  -                          -- Must be last line
```

#### RIS+ Format (.ris)

Extended RIS with additional fields. **Note: RIS+ is NOT an official standard** — it is a community convention. The M2/M3 fields are non-standard:
```
TY  - [Type]
TI  - [Title]
AU  - [Author1 Last, First]
...
M2  - [PMID]                    -- Non-standard convention (Miscellaneous 2)
M3  - [PMCID]                   -- Non-standard convention (Miscellaneous 3)
N1  - [Additional notes]        -- Standard RIS field
ER  - 
```

#### Special Document Types in RIS

For non-journal document types, adjust the `TY` field:

| Document Type | TY Value | Notes |
|---------------|----------|-------|
| Journal Article | `JOUR` | Default |
| Conference Paper | `CPAPER` | Individual conference paper |
| Conference Proceedings | `CONF` | Full proceedings |
| Book | `BOOK` | Monographs |
| Book Chapter | `CHAP` | Book sections |
| Thesis | `THES` | Dissertations |
| Patent | `PAT` | Use `N1` for patent number |
| Standard | `STAND` | Use `N1` for standard number |
| Preprint | `ELEC` | RIS has no PREPRINT; use Electronic Resource |
| Electronic Article | `EJOUR` | Electronic journal article |
| Report | `RPRT` | Technical reports |
| Dataset | `DATA` | Research datasets |
| Software | `COMP` | Computer programs |
| Magazine Article | `MGZN` | |
| Newspaper Article | `NEWS` | |
| Blog | `BLOG` | |
| Web Page | `ELEC` | |
| Manuscript | `MANSCPT` | |
| Generic | `GEN` | Fallback type |

## Database & Platform Reference

### Tier 1: Core APIs (Programmatic Access, No Authentication Required)

These databases provide free, open APIs suitable for automated metadata retrieval.

#### 1. CrossRef API
- **Coverage**: All DOI-registered works (journals, books, conferences, preprints, datasets)
- **Best for**: DOI lookup, title search, broad coverage
- **API**:
  ```
  # Lookup by DOI
  https://api.crossref.org/works/[DOI]

  # Search by title
  https://api.crossref.org/works?query.bibliographic=[title]&rows=3

  # Search with filters
  https://api.crossref.org/works?query=[title]&filter=from-pub-date:2020&type:journal-article&rows=3
  ```
- **Rate limit**: Polite pool (include `mailto` parameter)
- **Returns**: Full metadata including authors, abstract, references, funding, license

#### 2. PubMed / NCBI E-utilities
- **Coverage**: Biomedical and life sciences (36M+ citations)
- **Best for**: Biomedical papers, PMID/PMCID lookup
- **API**:
  ```
  # Search by title
  https://pubmed.ncbi.nlm.nih.gov/?term=[title]

  # Fetch by PMID
  https://pubmed.ncbi.nlm.nih.gov/[PMID]/

  # E-utilities API
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=[title]
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=[PMID]
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=[PMID]&rettype=medline
  ```
- **Rate limit**: 3 requests/second without API key, 10/second with key

#### 3. PubMed Central (PMC)
- **Coverage**: Free full-text biomedical articles (9M+)
- **Best for**: Open access biomedical papers, full-text metadata
- **API**:
  ```
  # PMC search
  https://www.ncbi.nlm.nih.gov/pmc/?term=[title]

  # OA API
  https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=[PMCID]
  ```

#### 4. Semantic Scholar API
- **Coverage**: 200M+ papers across all disciplines
- **Best for**: Title search, citation data, related papers, author info
- **API**:
  ```
  # Search by title
  https://api.semanticscholar.org/graph/v1/paper/search?query=[title]&limit=3

  # Get paper details
  https://api.semanticscholar.org/graph/v1/paper/[paperId]?fields=title,authors,year,venue,doi,abstract,citationCount

  # Lookup by DOI
  https://api.semanticscholar.org/graph/v1/paper/DOI:[DOI]?fields=title,authors,year,venue,doi
  ```
- **Rate limit**: 100 requests/5 minutes (no key), higher with API key

#### 5. OpenAlex API
- **Coverage**: 250M+ works, open metadata (replaces Microsoft Academic Graph)
- **Best for**: Broad coverage, author disambiguation, institution data
- **API**:
  ```
  # Search by title
  https://api.openalex.org/works?search=[title]&per_page=3

  # Lookup by DOI
  https://api.openalex.org/works/doi:[DOI]

  # Filter by type
  https://api.openalex.org/works?search=[title]&filter=type:article
  ```
- **Rate limit**: Polite pool (10/second), 100/second with email

#### 6. DataCite API
- **Coverage**: 20M+ datasets, software, preprints, technical reports
- **Best for**: Non-traditional scholarly outputs, datasets
- **API**:
  ```
  # Search by title
  https://api.datacite.org/dois?query=[title]

  # Lookup by DOI
  https://api.datacite.org/dois/[DOI]
  ```

#### 7. Dimensions API
- **Coverage**: 100M+ publications, grants, patents, clinical trials
- **Best for**: Linked research data, citation metrics, funding info
- **API** (free with registration):
  ```
  # Search by title
  https://app.dimensions.ai/discover/publication?search.text=[title]
  ```

#### 8. Unpaywall API
- **Coverage**: 200M+ OA paper locations, DOI-based lookup
- **Best for**: Finding open access versions of papers, OA metadata
- **API** (free, requires email):
  ```
  # Lookup by DOI (returns OA status, PDF URL, and metadata)
  https://api.unpaywall.org/v2/[DOI]?email=YOUR_EMAIL

  # Search OA papers
  https://api.unpaywall.org/v2/search?query=[title]&is_oa=true&email=YOUR_EMAIL
  ```
- **Note**: Essential for locating free full-text versions

### Tier 2: Publisher & Platform APIs (May Require Authentication)

#### 8. IEEE Xplore
- **Coverage**: 5M+ documents (journals, conferences, standards)
- **Best for**: Electrical engineering, computer science, electronics
- **API** (requires API key):
  ```
  https://ieeexploreapi.ieee.org/api/v1/search/articles?querytext=[title]
  ```
- **Web search fallback**: `https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=[title]`

#### 9. Elsevier ScienceDirect / Scopus
- **Coverage**: 18M+ publications (ScienceDirect), 90M+ (Scopus)
- **Best for**: Engineering, physical sciences, life sciences, social sciences
- **API** (requires API key):
  ```
  # ScienceDirect
  https://api.elsevier.com/content/search/sciencedirect?query=[title]

  # Scopus
  https://api.elsevier.com/content/search/scopus?query=[title]
  ```
- **Web search fallback**: `https://www.sciencedirect.com/search?query=[title]`

#### 10. Wiley Online Library
- **Coverage**: 4M+ articles across many disciplines
- **Best for**: Broad disciplinary coverage
- **Web search fallback**: `https://onlinelibrary.wiley.com/action/doSearch?AllField=[title]`

#### 11. SpringerLink
- **Coverage**: 13M+ documents (journals, books, protocols)
- **Best for**: Science, engineering, medicine, social sciences
- **API**:
  ```
  https://api.springernature.com/meta/v2/json?q=[title]&p=3
  ```
- **Web search fallback**: `https://link.springer.com/search?query=[title]`

#### 12. ACM Digital Library
- **Coverage**: 3M+ publications in computing
- **Best for**: Computer science, software engineering, HCI
- **API** (requires key):
  ```
  https://dl.acm.org/action/doSearch?AllField=[title]
  ```
- **Web search fallback**: `https://dl.acm.org/action/doSearch?AllField=[title]`

#### 13. JSTOR
- **Coverage**: 12M+ academic articles, books, primary sources
- **Best for**: Humanities, social sciences, archival content
- **Data for Research API** (free registration):
  ```
  https://www.jstor.org/action/doBasicSearch?Query=[title]
  ```
- **Note**: Some content requires institutional access for full text

#### 14. DBLP (Computer Science Bibliography)
- **Coverage**: 6M+ CS publications (journals, conferences, books). Most comprehensive CS bibliography
- **Best for**: Computer science papers, especially conference proceedings
- **Search**: `https://dblp.org/search?q=[title]`
- **API**: No formal REST API, but open XML data exports available
- **Note**: Particularly strong for conference paper metadata

#### 15. ERIC (Education Resources Information Center)
- **Coverage**: 1.6M+ education literature records
- **Best for**: Education research papers, reports, theses
- **API** (free):
  ```
  https://api.ies.ed.gov/eric/?search=title:[title]&rows=3
  ```

### Tier 3: Chinese Academic Databases (Web Search / Institutional Access)

#### 14. 中国知网 (CNKI)
- **Coverage**: Largest Chinese academic database (期刊、博硕、会议、专利、标准)
- **Best for**: Chinese journal articles, theses, conference papers
- **Search**: `https://www.cnki.net/` (title / author / keyword search)
- **Open Access**: CNKI 中国知网开放获取平台
- **Note**: Requires institutional access for full metadata; open access subset available

#### 15. 万方数据知识服务平台
- **Coverage**: Journals, theses, conferences, patents, standards
- **Best for**: Chinese theses, conference papers, patents
- **Search**: `https://www.wanfangdata.com.cn/`
- **Note**: Complementary to CNKI, some unique content

#### 16. 维普中文科技期刊数据库
- **Coverage**: Chinese scientific and technical journals
- **Best for**: Chinese science and engineering journals
- **Search**: `https://www.cqvip.com/`

#### 17. 国家哲学社会科学文献中心
- **Coverage**: Chinese social science journals (open access)
- **Best for**: Chinese social sciences and humanities
- **Search**: `https://www.ncpssd.cn/`

#### 18. 读秀学术搜索
- **Coverage**: Books, book chapters, theses
- **Best for**: Chinese books and book chapters
- **Search**: `https://www.duxiu.com/`
- **Note**: Primarily for book metadata

#### 19. CALIS 高校学位论文库
- **Coverage**: Chinese university dissertations
- **Best for**: Chinese master's and doctoral theses
- **Search**: Institutional access required

#### 20. 国家科技图书文献中心 (NSTL)
- **Coverage**: Science and technology literature (Chinese and foreign)
- **Best for**: Chinese science literature, document delivery
- **Search**: `https://www.nstl.gov.cn/`

#### 21. PubScholar
- **Coverage**: Chinese open access academic resources
- **Best for**: Open access Chinese papers
- **Search**: `https://pubscholar.cn/`

#### 22. AMiner
- **Coverage**: 260M+ papers, 130M+ scholar profiles. AI-driven academic search platform (Tsinghua University)
- **Best for**: CS/AI papers, scholar profiles, Chinese academic research
- **API** (open platform):
  ```
  https://open.aminer.cn/api
  ```
- **Search**: `https://www.aminer.cn/search?q=[title]`

### Tier 4: Preprint Servers

#### 22. arXiv
- **Coverage**: World's largest preprint server (284K+ papers/year). Physics, mathematics, CS, quantitative biology, statistics, EE, economics
- **Best for**: CS/physics/math papers (many never published elsewhere)
- **API** (free, open):
  ```
  # Search by title
  https://export.arxiv.org/api/query?search_query=all:[title]&start=0&max_results=3

  # Lookup by arXiv ID
  https://export.arxiv.org/api/query?id_list=[arXiv_ID]
  ```
- **Note**: arXiv IDs (e.g., 2301.00001) can serve as persistent identifiers

#### 23. bioRxiv
- **Coverage**: Biology and life sciences preprints
- **API**: `https://api.biorxiv.org/details/biorxiv/[DOI]/0/1/json`
- **Search**: `https://www.biorxiv.org/search/[title]`

#### 24. medRxiv
- **Coverage**: Medical and health sciences preprints (sister server to bioRxiv)
- **API**: `https://api.biorxiv.org/details/medrxiv/[DOI]/0/1/json` (shared API with bioRxiv)
- **Search**: `https://www.medrxiv.org/search/[title]`

#### 25. ChemRxiv
- **Coverage**: Chemistry preprints
- **Search**: `https://chemrxiv.org/engage/chemrxiv/search?search=[title]`

#### 26. EarthArXiv
- **Coverage**: Earth science preprints
- **Search**: `https://eartharxiv.org/search/?searchterm=[title]`

#### 27. SSRN (Social Science Research Network)
- **Coverage**: Social science, business, law preprints and working papers
- **Search**: `https://papers.ssrn.com/sol3/results.cfm?txtKey_Words=[title]`

#### 28. PSSXiv (Political Science)
- **Coverage**: Political science preprints
- **Search**: `https://osf.io/preprints/psixiv/`

### Tier 5: Open Access Repositories & Aggregators

#### 27. DOAJ (Directory of Open Access Journals)
- **Coverage**: 20,000+ open access journals
- **API**: `https://api.doaj.org/api/v1/search/articles/[title]?pageSize=3`
- **Best for**: Verifying OA journal metadata

#### 28. DOAB (Directory of Open Access Books)
- **Coverage**: Open access academic books
- **API**: `https://api.doab.org/api/v1/search/books/[title]`
- **Best for**: OA book chapters

#### 29. CORE
- **Coverage**: 250M+ open access research papers
- **API**: `https://api.core.ac.uk/v3/search/works?q=[title]`
- **Best for**: Finding OA versions of paywalled papers

#### 30. Figshare
- **Coverage**: Research data, figures, presentations, posters
- **API**: `https://api.figshare.com/v2/articles?search=[title]`
- **Best for**: Supplementary research outputs

#### 31. Zenodo
- **Coverage**: Research data, software, reports, preprints (hosted by CERN)
- **API**: `https://zenodo.org/api/records/?q=[title]`
- **Best for**: Datasets, software, preprints with DOI

#### 32. OpenGrey
- **Coverage**: European grey literature (reports, theses, conference papers)
- **Search**: `https://opengrey.eu/`
- **Best for**: Hard-to-find European reports and theses

### Tier 6: Citation Indexes (Institutional Access Typically Required)

#### 33. Web of Science (WOS)
- **Coverage**: 90M+ records, premium citation index
- **Best for**: Citation data, Journal Impact Factor, highly curated
- **Search**: `https://www.webofscience.com/wos/alldb/basic-search`
- **Note**: Requires institutional subscription; use as verification source

#### 34. Scopus
- **Coverage**: 90M+ records, largest abstract and citation database
- **Best for**: Citation analysis, author profiles, affiliation data
- **Search**: `https://www.scopus.com/results/results.uri?sort=plf-f&src=s&sot=b&sdt=b&sl=80&s=TITLE-ABS-KEY([title])`
- **Note**: Requires institutional subscription

#### 35. CPCI (Conference Proceedings Citation Index)
- **Coverage**: Conference proceedings across all disciplines
- **Best for**: Conference paper metadata and citation data
- **Note**: Part of Web of Science; requires institutional access

### Tier 7: Patent Databases

#### 36. USPTO (United States Patent and Trademark Office)
- **Coverage**: US patents and trademark data
- **API**: `https://developer.uspto.gov/data/api/patent/application/main?query=[title]`
- **Search**: `https://ppubs.uspto.gov/pubwebapp/`

#### 37. EPO (European Patent Office) / Espacenet
- **Coverage**: 130M+ patent documents worldwide
- **API**: `https://worldwide.espacenet.com/3.2/rest-services/search?q=[title]`
- **Search**: `https://worldwide.espacenet.com/`

#### 38. Derwent Innovations Index
- **Coverage**: Enhanced patent data with curated value-added information
- **Best for**: Patent citation analysis, patent families
- **Note**: Part of Web of Science; requires institutional access

### Tier 8: Standards

#### 39. ISO (International Organization for Standardization)
- **Coverage**: International standards
- **Search**: `https://www.iso.org/standards.html`
- **Note**: Full text requires purchase; metadata usually available

### Tier 9: Theses & Dissertations

#### 40. ProQuest Dissertations & Theses Global
- **Coverage**: 5M+ graduate works worldwide
- **Best for**: International theses and dissertations
- **Search**: `https://www.proquest.com/pqdtglobal`
- **Note**: Requires institutional access for full text

### Tier 10: Universal Fallback

#### 41. Google Scholar
- **Coverage**: Broadest coverage across all disciplines and languages
- **Best for**: Last resort fallback, finding papers not in other databases
- **Search**: `https://scholar.google.com/scholar?q=[title]`
- **Note**: No official API; use WebFetch for scraping; rate limiting possible

## Smart Search Strategy

### Decision Tree for Database Selection

```
Input received
├── Has DOI? → CrossRef API → (if not found) → Publisher platform
├── Has PMID? → PubMed → PMC (if OA)
├── Has patent number? → USPTO / EPO
├── Has standard number? → ISO / IEC
├── Title only
│   ├── Chinese title detected
│   │   └── CNKI → 万方 → 维普 → PubScholar → NSTL → Google Scholar
│   ├── Biomedical keywords detected
│   │   └── PubMed → PMC → Cochrane → CrossRef → Semantic Scholar → Google Scholar
│   ├── Engineering/CS keywords detected
│   │   └── IEEE Xplore → ACM DL → SpringerLink → ScienceDirect → CrossRef → Google Scholar
│   ├── Social science keywords detected
│   │   └── SSRN → JSTOR → 国家哲学社会科学文献中心 → Google Scholar → Dimensions
│   ├── Conference paper indicators
│   │   └── IEEE Xplore → CPCI → ACM DL → Google Scholar
│   ├── Preprint indicators (bioRxiv, arXiv, medRxiv, etc.)
│   │   └── Specific preprint server → CrossRef (check published version)
│   └── Unknown domain
│       └── CrossRef → Semantic Scholar → OpenAlex → Google Scholar
```

### Search Optimization Rules

1. **Always try DOI first** — CrossRef is the fastest and most reliable
2. **Use domain-specific databases before general ones** — Higher metadata quality
3. **For Chinese papers** — Always try CNKI/万方/维普 before English databases
4. **For preprints** — Check if a published version exists via CrossRef/DOI
5. **Extract DOI from URLs** — If a URL contains `doi.org/`, extract the bare DOI (e.g., `https://doi.org/10.1016/j.slast.2025.100250` → `10.1016/j.slast.2025.100250`). Always populate the DOI field separately from the URL field
6. **Batch similar papers** — Search multiple papers from the same domain together
7. **Respect rate limits** — Add delays between API calls when needed
8. **Cache results** — Save intermediate results to avoid redundant searches
9. **Cross-validate** — Compare metadata from multiple sources when possible

## Handling Special Cases

### Chinese Papers with English Titles

Many Chinese papers have English titles that are translations. Strategy:
1. Search Chinese databases (CNKI, 万方, 维普) with the English title
2. If not found, try searching with key Chinese terms
3. Check if the paper has a DOI via CrossRef
4. Use Google Scholar as fallback (often indexes Chinese papers)

### Conference Papers

Conference papers may lack volume/issue numbers. Include:
- Conference name in `T2` (secondary title) field
- Conference location and date in `N1` (notes) field
- Use `TY - CONF` instead of `TY - JOUR` in RIS

### Preprints

Preprints may not have journal/volume/issue. Include:
- Repository name (e.g., bioRxiv, arXiv) in `N1` field
- Preprint DOI if available
- Posted date instead of publication date
- Use `TY - ELEC` in RIS (RIS has no PREPRINT type)

### Patents

Patents have unique metadata fields. Include:
- Patent number in `N1` field
- Filing date and grant date
- Inventors (not authors) and assignee
- Use `TY - PAT` in RIS

### Standards

Standards have unique identifiers. Include:
- Standard number (e.g., ISO 9001:2015) in `N1` field
- Organization (ISO, IEC, IEEE, GB)
- Use `TY - STAND` in RIS

### Theses/Dissertations

Include:
- Degree type (PhD, Master's) in `N1` field
- University/institution
- Use `TY - THES` in RIS

## Handling Missing Information

When complete metadata cannot be found:

1. **Partial results**: Generate citation with available fields, mark missing fields as "Unknown"
2. **Chinese journals**: Search CNKI, 万方, 维普, PubScholar
3. **Conference papers**: May have limited metadata; include proceedings info
4. **Preprints**: Include repository identifier if available
5. **Patents**: Include patent number and assignee
6. **Standards**: Include standard number and organization

Report to user:
- Successfully processed papers
- Papers with partial information (specify missing fields)
- Papers not found (with suggestions for manual search and which databases to try)

## Output File Naming

Default naming convention:
- Single paper: `[FirstAuthor]_[Year]_[JournalAbbrev].enw` or `.ris`
- Batch: `references_batch.enw` or `references_batch.ris`
- User can specify custom filename

## Quality Checklist

Before delivering citation file, verify:

- [ ] All authors included (check for "et al." truncation)
- [ ] Journal/source name is full name (not abbreviation)
- [ ] Year, volume, issue, pages are complete
- [ ] DOI is valid and resolves (if available)
- [ ] PMID/PMCID included for PubMed-indexed papers
- [ ] Abstract included if available
- [ ] Keywords included if available
- [ ] Document type is correctly identified (JOUR, CONF, THES, PAT, etc.)
- [ ] No "Unknown" fields remain (or user is notified)
- [ ] Chinese papers have correct Chinese journal names (not just English translations)

## Common Issues and Solutions

### Issue: Paper not found in any database

Solution: Try these steps:
1. Verify the title is exact (check for typos, subtitle variations)
2. Search Google Scholar (broadest coverage)
3. Search with fewer title words (remove subtitle)
4. Try Chinese databases if the paper might be Chinese
5. Check if it's a preprint, thesis, or report (not a journal article)
6. Ask user for additional identifiers (DOI, author, year)

### Issue: Incomplete author list

Solution: 
- CrossRef and PubMed usually have complete author lists
- Publisher websites often have full author lists
- Google Scholar may truncate with "et al."

### Issue: Missing page numbers

Solution: Some early-view/online-first articles don't have page numbers yet. Use article ID or DOI instead.

### Issue: Duplicate papers in batch

Solution: Detect and merge duplicates, keeping the record with more complete metadata. Compare by DOI, then by title similarity.

### Issue: Chinese paper metadata only in Chinese

Solution: Keep Chinese metadata as-is. Most reference managers support Chinese characters. Optionally add English translation in notes field.

## Integration with Reference Managers

### EndNote

1. Open EndNote
2. File → Import → Import File
3. Select the .enw file
4. Import Option: EndNote Import
5. Click Import

### Zotero

1. Open Zotero
2. File → Import
3. Select the .ris file
4. Choose "RIS" as import format

### Mendeley

1. Open Mendeley
2. File → Import → RIS
3. Select the .ris file

### JabRef

1. Open JabRef
2. File → Import into new library
3. Select the .ris or .enw file

### NoteExpress (知网文献管理)

1. 打开 NoteExpress
2. 文件 → 导入题录
3. 选择 .ris 或 .enw 文件
4. 选择对应的过滤器

## Notes

- Always prefer DOI/PMID lookup over title search for accuracy
- For biomedical papers, PubMed is the most reliable source
- For engineering/CS papers, IEEE Xplore, ACM DL, SpringerLink, and DBLP are better
- For Chinese papers, CNKI/万方/维普 are essential
- For CS/physics/math preprints, arXiv is the primary source
- Google Scholar should be used as a last resort fallback
- OpenAlex provides excellent broad coverage with a free API
- Unpaywall is essential for finding OA versions of papers
- Batch processing may take time for many papers — inform user of progress
- Save intermediate results to avoid re-searching if process is interrupted
- Respect API rate limits and terms of service for each database

## Format Specification References

- **EndNote Tagged Format**: Based on EndNote X6 export data, reverse-engineered by Zotero translator project. See [ENW Tag Map](https://github.com/aurimasv/translators/wiki/ENW-Refer-BibIX-EndNote-tag-map)
- **RIS Format**: Based on RIS specification (2001/2011) by Research Information Systems / Thomson Reuters / Clarivate. See [RIS Tag Map](https://github.com/aurimasv/translators/wiki/RIS-Tag-Map) and [archived spec](https://web.archive.org/web/20120716182104/http://www.refman.com/support/risformat_intro.asp)
- **RIS+**: NOT an official standard. Community convention using M2 (PMID) and M3 (PMCID) as non-standard extensions
- **DOI in ENW**: Use `%R` tag (official DOI tag), NOT `%U` (URL) or `%6` (Number of Volumes)
- **DOI in RIS**: Use `DO` field (official DOI field), NOT `UR` (URL)
