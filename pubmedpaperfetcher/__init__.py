# pubmedpaperfetcher/__init__.py

"""
pubmedpaperfetcher

This package provides functionality to fetch research papers from PubMed
and filter authors based on their affiliations.
"""

# You can also import specific functions or classes to make them available at the package level.
from .get_papers_list import main as get_papers_list
from .papers_fetcher import fetch_papers, save_to_csv

__all__ = ["get_papers_list", "fetch_papers", "save_to_csv"]