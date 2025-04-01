import unittest
from unittest.mock import patch, MagicMock
import pytest
import pubmedpaperfetcher.papers_fetcher as papers_fetcher


# Sample XML responses for testing
test_xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation>
            <PMID>123456</PMID>
            <Article>
                <ArticleTitle>Sample Research Paper</ArticleTitle>
            </Article>
            <PubDate>
                <Year>2023</Year>
            </PubDate>
            <AuthorList>
                <Author>
                    <LastName>Doe</LastName>
                    <Initials>J</Initials>
                    <AffiliationInfo>
                        <Affiliation>XYZ Biotech Ltd, example@biotech.com</Affiliation>
                    </AffiliationInfo>
                </Author>
                <Author>
                    <LastName>Smith</LastName>
                    <Initials>K</Initials>
                    <AffiliationInfo>
                        <Affiliation>ABC University</Affiliation>
                    </AffiliationInfo>
                </Author>
            </AuthorList>
        </MedlineCitation>
    </PubmedArticle>
</PubmedArticleSet>
"""

empty_xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<PubmedArticleSet></PubmedArticleSet>
"""

xml_no_non_academic = """<?xml version="1.0" encoding="UTF-8"?>
<PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation>
            <PMID>789012</PMID>
            <Article>
                <ArticleTitle>Academic Research Paper</ArticleTitle>
            </Article>
            <PubDate>
                <Year>2024</Year>
            </PubDate>
            <AuthorList>
                <Author>
                    <LastName>Brown</LastName>
                    <Initials>M</Initials>
                    <AffiliationInfo>
                        <Affiliation>Harvard University</Affiliation>
                    </AffiliationInfo>
                </Author>
            </AuthorList>
        </MedlineCitation>
    </PubmedArticle>
</PubmedArticleSet>
"""

xml_missing_fields = """<?xml version="1.0" encoding="UTF-8"?>
<PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation>
            <PMID></PMID>
            <Article>
                <ArticleTitle></ArticleTitle>
            </Article>
            <PubDate>
                <Year></Year>
            </PubDate>
            <AuthorList>
                <Author>
                    <LastName></LastName>
                    <Initials></Initials>
                    <AffiliationInfo>
                        <Affiliation></Affiliation>
                    </AffiliationInfo>
                </Author>
            </AuthorList>
        </MedlineCitation>
    </PubmedArticle>
</PubmedArticleSet>
"""

xml_multiple_non_academic = """<?xml version="1.0" encoding="UTF-8"?>
<PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation>
            <PMID>456789</PMID>
            <Article>
                <ArticleTitle>Multi Non-Academic Research</ArticleTitle>
            </Article>
            <PubDate>
                <Year>2022</Year>
            </PubDate>
            <AuthorList>
                <Author>
                    <LastName>Lee</LastName>
                    <Initials>A</Initials>
                    <AffiliationInfo>
                        <Affiliation>Big Pharma Inc.</Affiliation>
                    </AffiliationInfo>
                </Author>
                <Author>
                    <LastName>Kim</LastName>
                    <Initials>B</Initials>
                    <AffiliationInfo>
                        <Affiliation>BioTech Solutions</Affiliation>
                    </AffiliationInfo>
                </Author>
            </AuthorList>
        </MedlineCitation>
    </PubmedArticle>
</PubmedArticleSet>
"""

# ------------------------------ TEST CASES ------------------------------

def test_parse_papers():
    """Test XML parsing function with a valid response"""
    papers = papers_fetcher.parse_papers(test_xml_response, debug=True)
    
    assert len(papers) == 1
    assert papers[0][0] == "123456"  # PubMed ID
    assert papers[0][1] == "Sample Research Paper"  # Title
    assert papers[0][2] == "2023"  # Publication Year
    assert papers[0][3] == "Doe J"  # Non-Academic Author
    assert papers[0][4].startswith("XYZ Biotech Ltd")  # Company Affiliation
    assert papers[0][5] == "example@biotech.com"  # Email

def test_parse_empty_response():
    """Test parsing an empty XML response"""
    papers = papers_fetcher.parse_papers(empty_xml_response, debug=True)
    assert papers == []  # No papers should be found

def test_parse_multiple_non_academic_authors():
    """Test parsing with multiple non-academic authors"""
    papers = papers_fetcher.parse_papers(xml_multiple_non_academic, debug=True)

    assert len(papers) == 1
    assert papers[0][3] == "Lee A; Kim B"  # Multiple Non-Academic Authors
    assert "Big Pharma Inc." in papers[0][4]  # Check company affiliation
    assert "BioTech Solutions" in papers[0][4]

def test_is_non_academic():
    """Test the affiliation classification function"""
    assert papers_fetcher.is_non_academic("XYZ Biotech Ltd") is True
    assert papers_fetcher.is_non_academic("Harvard University") is False
    assert papers_fetcher.is_non_academic("National Laboratory") is False
    assert papers_fetcher.is_non_academic("Pharma Research Inc.") is True


def test_is_non_academic_variations():
    """Test different variations of company names"""
    assert papers_fetcher.is_non_academic("Big Pharma Inc.") is True
    assert papers_fetcher.is_non_academic("Tech Solutions Pvt Ltd") is True
    assert papers_fetcher.is_non_academic("University of California") is False
    assert papers_fetcher.is_non_academic("MIT Research Labs") is False
    assert papers_fetcher.is_non_academic("Global Pharmaceuticals") is True


if __name__ == "__main__":
    pytest.main()
