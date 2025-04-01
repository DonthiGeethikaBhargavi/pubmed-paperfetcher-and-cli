import os
import csv
import re
import logging
import requests
from typing import List, Tuple, Optional
from xml.etree import ElementTree as ET

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
DATA_DIR = "data"
RETRIES = 3  # Number of retries for API requests

# Ensure 'data' directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Keywords for classification
ACADEMIC_KEYWORDS = [
    "university", "institute", "college", "academy", "school", "lab",
    "research center", "department", "faculty", "center for", "school of",
    "national laboratory", "polytechnic", "higher education"
]

NON_ACADEMIC_KEYWORDS = [
    "pharma", "inc.", "corporation", "private ltd", "hospital", "clinic", "biotech",
    "limited", "ltd.", "corp.", "gmbh", "pvt", "s.a.", "llc", "co.", "foundation",
    "healthcare", "medical center", "biopharma", "research institute", "r&d", "venture"
]

class PubMedAPIError(Exception):
    """Custom exception for PubMed API errors."""
    pass

def fetch_papers(query: str, debug: bool = False) -> List[List[str]]:
    """
    Fetch papers from PubMed based on the search query.
    
    Args:
        query (str): The search term for PubMed.
        debug (bool): If True, enables detailed output.

    Returns:
        List[List[str]]: A list of papers with extracted details.
    """
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Adjust number of papers fetched
    }

    paper_ids = _make_request(PUBMED_API_URL, search_params, is_json=True).get("esearchresult", {}).get("idlist", [])

    if not paper_ids:
        logging.warning("⚠ No papers found for the query: %s", query)
        return []

    fetch_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }

    fetch_response = _make_request(PUBMED_FETCH_URL, fetch_params, is_json=False)
    return parse_papers(fetch_response, debug)

def _make_request(url: str, params: dict, is_json: bool = True) -> dict:
    """
    Helper function to make GET requests with retries.
    
    Args:
        url (str): The API endpoint URL.
        params (dict): Query parameters.
        is_json (bool): Whether to return JSON response.

    Returns:
        dict or str: Parsed JSON response or raw XML response.

    Raises:
        PubMedAPIError: If the request fails after retries.
    """
    for attempt in range(1, RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json() if is_json else response.text
        except requests.RequestException as e:
            logging.error("❌ API request failed (attempt %d/%d): %s", attempt, RETRIES, e)
            if attempt == RETRIES:
                raise PubMedAPIError(f"Failed to fetch data from PubMed after {RETRIES} attempts.") from e

def parse_papers(xml_data: str, debug: bool = False) -> List[List[str]]:
    """
    Parse XML response from PubMed and extract required details.

    Args:
        xml_data (str): XML response from PubMed API.
        debug (bool): If True, prints detailed information.

    Returns:
        List[List[str]]: List of parsed paper details.
    """
    root = ET.fromstring(xml_data)
    papers_list = []

    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.findtext(".//PMID", default="N/A")
        title = article.findtext(".//ArticleTitle", default="N/A")
        pub_date = article.findtext(".//PubDate/Year", default="N/A")

        authors = article.findall(".//Author")
        non_academic_authors, company_affiliations, corresponding_email = _extract_author_info(authors)

        if debug:
            logging.info(f"📄 PubMed ID: {pubmed_id}")
            logging.info(f"📝 Title: {title}")
            logging.info(f"📅 Publication Date: {pub_date}")
            logging.info(f"👨‍🔬 Non-Academic Authors: {', '.join(non_academic_authors) or 'N/A'}")
            logging.info(f"🏢 Company Affiliations: {', '.join(company_affiliations) or 'N/A'}")
            logging.info(f"📧 Corresponding Email: {corresponding_email or 'N/A'}")

        papers_list.append([
            pubmed_id, title, pub_date,
            "; ".join(non_academic_authors) if non_academic_authors else "N/A",
            "; ".join(company_affiliations) if company_affiliations else "N/A",
            corresponding_email
        ])

    return papers_list

def _extract_author_info(authors) -> Tuple[List[str], List[str], Optional[str]]:
    """
    Extracts author details such as name, affiliations, and emails.

    Args:
        authors (List[ET.Element]): List of author XML elements.

    Returns:
        Tuple[List[str], List[str], Optional[str]]: Non-academic authors, company affiliations, corresponding email.
    """
    non_academic_authors = []
    company_affiliations = []
    corresponding_email = None

    for author in authors:
        last_name = author.findtext("LastName", default="")
        initials = author.findtext("Initials", default="")
        full_name = f"{last_name} {initials}".strip()

        affiliation_element = author.find(".//AffiliationInfo/Affiliation")
        affiliation = affiliation_element.text if affiliation_element is not None else ""

        if is_non_academic(affiliation):
            non_academic_authors.append(full_name)
            company_affiliations.append(affiliation)

        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", affiliation)
        if email_match and not corresponding_email:
            corresponding_email = email_match.group()

    return non_academic_authors, company_affiliations, corresponding_email

def is_non_academic(affiliation: str) -> bool:
    """
    Determines if an affiliation is non-academic.

    Args:
        affiliation (str): The affiliation text.

    Returns:
        bool: True if non-academic, False otherwise.
    """
    affiliation_lower = affiliation.lower()

    if any(keyword in affiliation_lower for keyword in ACADEMIC_KEYWORDS):
        return False  # Academic institution

    if any(keyword in affiliation_lower for keyword in NON_ACADEMIC_KEYWORDS):
        return True  # Non-academic institution

    return False  # Default assumption: academic

def save_to_csv(papers: List[List[str]], filename: str) -> None:
    """
    Saves extracted paper data to a CSV file inside 'data/' directory.

    Args:
        papers (List[List[str]]): The list of paper details.
        filename (str): Name of the output CSV file.
    """
    output_path = os.path.join(DATA_DIR, filename)

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Email"])
        writer.writerows(papers)

    logging.info(f"✅ Papers saved to {output_path}")


if __name__ == "__main__":
    query = "biotecnology"  # Change this to your desired search term
    papers = fetch_papers(query, debug=True)  

    if papers:
        save_to_csv(papers, "papers.csv")
    else:
        print("❌ No papers found for the given query.")

