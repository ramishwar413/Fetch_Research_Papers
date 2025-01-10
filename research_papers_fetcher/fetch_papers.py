import requests
import csv
from typing import List, Dict

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
EMAIL = "your-email@example.com"  # Replace with your actual email for API compliance

def fetch_paper_ids(query: str) -> List[str]:
    """Fetches PubMed IDs for a given query."""
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'email': EMAIL
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    return response.json().get('esearchresult', {}).get('idlist', [])

def fetch_paper_details(paper_ids: List[str]) -> List[Dict]:
    """Fetches detailed information for given PubMed IDs."""
    if not paper_ids:
        return []
    
    params = {
        'db': 'pubmed',
        'id': ','.join(paper_ids),
        'retmode': 'json',
        'email': EMAIL
    }
    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    response.raise_for_status()
    return list(response.json().get('result', {}).values())[1:]  # Exclude 'uids' field

def filter_papers(papers: List[Dict]) -> List[Dict]:
    """Filters papers with non-academic authors."""
    filtered = []
    for paper in papers:
        if 'authors' in paper:
            non_academic_authors = [author for author in paper['authors'] if is_non_academic_author(author)]
            if non_academic_authors:
                filtered.append({
                    'PubmedID': paper.get('uid'),
                    'Title': paper.get('title'),
                    'Publication Date': paper.get('pubdate'),
                    'Non-academic Author(s)': [author['name'] for author in non_academic_authors],
                    'Company Affiliation(s)': [author.get('affiliation', '') for author in non_academic_authors],
                    'Corresponding Author Email': paper.get('elocationid', '')
                })
    return filtered

def is_non_academic_author(author: Dict) -> bool:
    """Determines if an author is non-academic based on affiliation."""
    affiliation = author.get('affiliation', '').lower()
    return any(keyword in affiliation for keyword in ['pharma', 'biotech', 'company'])

def save_to_csv(papers: List[Dict], filename: str):
    """Saves filtered papers to a CSV file."""
    fieldnames = [
        'PubmedID', 'Title', 'Publication Date',
        'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'
    ]
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)
