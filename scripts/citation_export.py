#!/usr/bin/env python3
"""
Citation Export Script v2.1
Generates citation files in EndNote (.enw), RIS (.ris), or RIS+ format
from academic paper metadata.

Fixes in v2.1:
- Fixed ENW format: DOI now uses %R tag (official standard), not %U/%6
- Fixed ENW format: %U is now URL (not DOI URL)
- Fixed ENW format: %M is Accession Number (not PMID); PMID stored in custom field
- Fixed ENW format: Removed incorrect %6 (DOI) and %? (PMCID) usage
- Added ENW: %R (DOI), %Z (Notes), %2 (PMCID for Journal Article)
- Fixed RIS format: UR is now URL (not DOI URL); DO is DOI
- Added RIS: JO (Journal Full Name) tag alongside T2
- Fixed RIS+: M2/M3 documented as non-standard conventions for PMID/PMCID
- Added DOI extraction from doi.org URLs (e.g., "https://doi.org/10.xxx" -> "10.xxx")
- Added extract_doi() utility function
- Added support for document types: CONF, THES, PAT, STAND, ELEC, RPRT, DATA, COMP

Usage:
    python citation_export.py --input metadata.json --format enw --output references.enw
    python citation_export.py --input metadata.json --format ris --output references.ris
    python citation_export.py --input metadata.json --format ris+ --output references.ris
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple


# RIS Document Type mapping (official RIS standard values)
RIS_TYPE_MAP = {
    "journal article": "JOUR",
    "journal": "JOUR",
    "article": "JOUR",
    "conference paper": "CPAPER",
    "conference": "CPAPER",
    "conference proceedings": "CONF",
    "book": "BOOK",
    "book section": "CHAP",
    "book chapter": "CHAP",
    "chapter": "CHAP",
    "thesis": "THES",
    "dissertation": "THES",
    "phd": "THES",
    "master": "THES",
    "patent": "PAT",
    "standard": "STAND",
    "preprint": "ELEC",       # RIS has no PREPRINT; use ELEC (Electronic Resource)
    "report": "RPRT",
    "dataset": "DATA",
    "software": "COMP",
    "computer program": "COMP",
    "web page": "ELEC",
    "electronic": "ELEC",
    "magazine article": "MGZN",
    "newspaper article": "NEWS",
    "blog": "BLOG",
    "manuscript": "MANSCPT",
    "working paper": "RPRT",
    "unpublished": "UNPB",
    "generic": "GEN",
}

# ENW Document Type mapping (EndNote standard values)
ENW_TYPE_MAP = {
    "journal article": "Journal Article",
    "journal": "Journal Article",
    "article": "Journal Article",
    "conference paper": "Conference Paper",
    "conference": "Conference Proceedings",
    "conference proceedings": "Conference Proceedings",
    "book": "Book",
    "book section": "Book Section",
    "book chapter": "Book Section",
    "chapter": "Book Section",
    "thesis": "Thesis",
    "dissertation": "Thesis",
    "patent": "Patent",
    "standard": "Standard",
    "preprint": "Electronic Article",
    "report": "Report",
    "dataset": "Dataset",
    "software": "Computer Program",
    "web page": "Web Page",
    "electronic": "Electronic Article",
    "magazine article": "Magazine Article",
    "newspaper article": "Newspaper Article",
    "blog": "Blog",
    "manuscript": "Manuscript",
    "working paper": "Report",
    "generic": "Generic",
}


def extract_doi(value: str) -> Optional[str]:
    """
    Extract DOI from a URL string if it contains a doi.org link.
    
    Examples:
        "https://doi.org/10.1016/j.slast.2025.100250" -> "10.1016/j.slast.2025.100250"
        "http://dx.doi.org/10.1038/s41586-021-03819-2" -> "10.1038/s41586-021-03819-2"
        "10.1186/s12984-024-01420-y" -> "10.1186/s12984-024-01420-y"  (already a DOI)
        "https://www.nature.com/articles/s41586-021-03819-2" -> None (not a DOI URL)
    """
    if not value:
        return None
    
    value = value.strip()
    
    # If it's already a bare DOI (starts with 10.)
    if re.match(r'^10\.\d{4,9}/', value):
        return value
    
    # Extract DOI from doi.org URLs (handles https://doi.org/, http://dx.doi.org/, etc.)
    match = re.search(r'(?:https?://)?(?:dx\.)?doi\.org/(10\.\d{4,9}/[^\s]+)', value)
    if match:
        doi = match.group(1)
        # Remove trailing punctuation or query params
        doi = doi.rstrip('.,;)')
        return doi
    
    return None


def resolve_doi(paper: Dict) -> Tuple[Optional[str], Optional[str]]:
    """
    Resolve DOI and URL from paper metadata.
    
    Priority:
    1. If paper has 'doi' field -> use it as DOI, construct URL from it
    2. If paper has 'url' field containing doi.org -> extract DOI from URL
    3. If paper has 'url' field (non-DOI) -> use as URL, no DOI
    
    Returns:
        (doi, url) tuple
    """
    doi = paper.get('doi', '').strip() if paper.get('doi') else None
    url = paper.get('url', '').strip() if paper.get('url') else None
    
    # Case 1: DOI field exists
    if doi:
        # Construct DOI URL if no URL provided
        if not url:
            url = f"https://doi.org/{doi}"
        return doi, url
    
    # Case 2: No DOI field, but URL contains doi.org
    if url:
        extracted = extract_doi(url)
        if extracted:
            return extracted, url
    
    # Case 3: URL exists but not a DOI URL
    if url:
        return None, url
    
    return None, None


def parse_pages(pages: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse page range into start and end pages."""
    if not pages:
        return None, None
    if '-' in pages:
        parts = pages.split('-')
        return parts[0].strip(), parts[1].strip() if len(parts) > 1 else None
    return pages.strip(), None


def format_author_enw(author: str) -> str:
    """Format a single author for EndNote format."""
    if ',' in author:
        return f"%A {author}"
    else:
        parts = author.split()
        if len(parts) >= 2:
            last = parts[-1]
            first = ' '.join(parts[:-1])
            return f"%A {last}, {first}"
        else:
            return f"%A {author}"


def format_author_ris(author: str) -> str:
    """Format a single author for RIS format."""
    if ',' in author:
        return f"AU  - {author}"
    else:
        parts = author.split()
        if len(parts) >= 2:
            last = parts[-1]
            first = ' '.join(parts[:-1])
            return f"AU  - {last}, {first}"
        else:
            return f"AU  - {author}"


def get_ris_type(paper: Dict) -> str:
    """Get the RIS TY value based on paper's document type."""
    doc_type = paper.get('type', paper.get('document_type', '')).strip().lower()
    if doc_type and doc_type in RIS_TYPE_MAP:
        return RIS_TYPE_MAP[doc_type]
    return "JOUR"  # Default to journal article


def get_enw_type(paper: Dict) -> str:
    """Get the ENW %0 value based on paper's document type."""
    doc_type = paper.get('type', paper.get('document_type', '')).strip().lower()
    if doc_type and doc_type in ENW_TYPE_MAP:
        return ENW_TYPE_MAP[doc_type]
    return "Journal Article"  # Default


def generate_endnote(paper: Dict) -> str:
    """
    Generate EndNote (.enw) format citation.
    
    Tag reference (based on EndNote X6 export data):
    %0  - Reference Type (must be first)
    %T  - Title
    %A  - Author (one per line)
    %J  - Journal Name (for Journal Article type)
    %B  - Secondary Title (for non-journal types: book title, conference name)
    %D  - Year
    %V  - Volume
    %N  - Issue / Number
    %P  - Pages
    %@  - ISSN / ISBN
    %I  - Publisher
    %C  - Place Published
    %X  - Abstract
    %K  - Keywords
    %R  - DOI (official DOI tag)
    %U  - URL (web link, NOT DOI)
    %G  - Language
    %Z  - Notes
    %2  - Custom 2 (PMCID for Journal Article)
    %M  - Accession Number
    %W  - Database Provider
    """
    doc_type = get_enw_type(paper)
    lines = [f'%0 {doc_type}']
    
    if paper.get('title'):
        lines.append(f"%T {paper['title']}")
    
    if paper.get('authors'):
        for author in paper['authors']:
            lines.append(format_author_enw(author))
    
    # Journal name: %J for Journal Article, %B for other types
    if paper.get('journal'):
        if doc_type == "Journal Article" or doc_type == "Electronic Article":
            lines.append(f"%J {paper['journal']}")
        else:
            lines.append(f"%B {paper['journal']}")
    
    if paper.get('year'):
        lines.append(f"%D {paper['year']}")
    
    if paper.get('volume'):
        lines.append(f"%V {paper['volume']}")
    
    if paper.get('issue'):
        lines.append(f"%N {paper['issue']}")
    
    if paper.get('pages'):
        lines.append(f"%P {paper['pages']}")
    
    if paper.get('issn'):
        lines.append(f"%@ {paper['issn']}")
    
    if paper.get('publisher'):
        lines.append(f"%I {paper['publisher']}")
    
    if paper.get('abstract'):
        lines.append(f"%X {paper['abstract']}")
    
    if paper.get('keywords'):
        lines.append(f"%K {paper['keywords']}")
    
    # DOI and URL handling
    doi, url = resolve_doi(paper)
    if doi:
        lines.append(f"%R {doi}")  # Official DOI tag
    if url:
        lines.append(f"%U {url}")  # URL tag (web link)
    
    if paper.get('language'):
        lines.append(f"%G {paper['language']}")
    
    # PMCID: stored in %2 (Custom 2) for Journal Article
    if paper.get('pmcid'):
        lines.append(f"%2 {paper['pmcid']}")
    
    # PMID: stored in %M (Accession Number) - this is the closest standard tag
    if paper.get('pmid'):
        lines.append(f"%M {paper['pmid']}")
    
    # Notes
    if paper.get('notes'):
        lines.append(f"%Z {paper['notes']}")
    
    return '\n'.join(lines)


def generate_ris(paper: Dict, extended: bool = False) -> str:
    """
    Generate RIS (.ris) format citation.
    
    Key RIS tags (based on RIS specification):
    TY  - Type of Reference (must be first line)
    TI  - Title (or T1)
    AU  - Author (one per line, or A1)
    JO  - Journal Full Name (for journal articles)
    T2  - Secondary Title (journal/book/conference name)
    PY  - Publication Year (format: YYYY/MM/DD)
    VL  - Volume
    IS  - Issue
    SP  - Start Page
    EP  - End Page
    SN  - ISSN / ISBN
    PB  - Publisher
    AB  - Abstract
    KW  - Keywords (one per line)
    DO  - DOI (official DOI field)
    UR  - URL (web link, NOT DOI)
    LA  - Language
    N1  - Notes
    AN  - Accession Number
    C2  - Custom 2 (PMCID for Journal Article in some tools)
    M2  - Miscellaneous 2 (non-standard: PMID convention)
    M3  - Miscellaneous 3 (non-standard: PMCID convention)
    ER  - End of Record (must be last line)
    """
    doc_type = get_ris_type(paper)
    lines = [f'TY  - {doc_type}']
    
    if paper.get('title'):
        lines.append(f"TI  - {paper['title']}")
    
    if paper.get('authors'):
        for author in paper['authors']:
            lines.append(format_author_ris(author))
    
    # Journal/source name
    if paper.get('journal'):
        if doc_type == "JOUR" or doc_type == "ELEC":
            lines.append(f"JO  - {paper['journal']}")  # Journal Full Name
        lines.append(f"T2  - {paper['journal']}")  # Secondary Title (always include)
    
    if paper.get('year'):
        lines.append(f"PY  - {paper['year']}")
    
    if paper.get('volume'):
        lines.append(f"VL  - {paper['volume']}")
    
    if paper.get('issue'):
        lines.append(f"IS  - {paper['issue']}")
    
    if paper.get('pages'):
        start, end = parse_pages(paper['pages'])
        if start:
            lines.append(f"SP  - {start}")
        if end:
            lines.append(f"EP  - {end}")
    
    if paper.get('issn'):
        lines.append(f"SN  - {paper['issn']}")
    
    if paper.get('publisher'):
        lines.append(f"PB  - {paper['publisher']}")
    
    if paper.get('abstract'):
        lines.append(f"AB  - {paper['abstract']}")
    
    if paper.get('keywords'):
        for kw in paper['keywords'].split(';'):
            kw = kw.strip()
            if kw:
                lines.append(f"KW  - {kw}")
    
    if paper.get('language'):
        lines.append(f"LA  - {paper['language']}")
    
    # DOI and URL handling
    doi, url = resolve_doi(paper)
    if doi:
        lines.append(f"DO  - {doi}")  # Official DOI field
    if url:
        lines.append(f"UR  - {url}")  # URL field (web link)
    
    # RIS+ extended fields (non-standard conventions)
    if extended:
        # M2 for PMID (non-standard convention used by some PubMed export tools)
        if paper.get('pmid'):
            lines.append(f"M2  - {paper['pmid']}")
        
        # M3 for PMCID (non-standard convention)
        if paper.get('pmcid'):
            lines.append(f"M3  - {paper['pmcid']}")
        
        # N1 for additional notes
        if paper.get('notes'):
            lines.append(f"N1  - {paper['notes']}")
    
    lines.append('ER  - ')
    
    return '\n'.join(lines)


def generate_citations(papers: List[Dict], format_type: str) -> str:
    """Generate citations for all papers in specified format."""
    citations = []
    
    for paper in papers:
        if format_type == 'enw':
            citations.append(generate_endnote(paper))
        elif format_type == 'ris':
            citations.append(generate_ris(paper, extended=False))
        elif format_type == 'ris+':
            citations.append(generate_ris(paper, extended=True))
    
    return '\n\n'.join(citations)


def main():
    parser = argparse.ArgumentParser(description='Generate citation files (v2.1)')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file with paper metadata')
    parser.add_argument('--format', '-f', required=True, choices=['enw', 'ris', 'ris+'],
                        help='Output format: enw (EndNote), ris (RIS), ris+ (RIS extended)')
    parser.add_argument('--output', '-o', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    # Read input
    with open(args.input, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # Generate citations
    content = generate_citations(papers, args.format)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Generated {len(papers)} citations in {args.format} format: {args.output}")


if __name__ == '__main__':
    main()
