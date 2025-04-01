import argparse
import logging
import sys
from .papers_fetcher import fetch_papers, save_to_csv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    """
    Command-line interface for fetching and saving research papers from PubMed.
    """
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed and save them to a CSV file."
    )
    
    parser.add_argument(
        "query", type=str, help="Search query for fetching research papers from PubMed."
    )
    
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable detailed debug output."
    )
    
    parser.add_argument(
        "-f", "--file", type=str, default="papers.csv",
        help="Filename to save the output CSV (default: papers.csv)."
    )

    args = parser.parse_args()

    logging.info(f"🔍 Searching for papers related to: {args.query}")

    try:
        papers = fetch_papers(args.query, debug=args.debug)

        if not papers:
            logging.warning("⚠ No papers found for the query: %s", args.query)
            sys.exit(1)

        save_to_csv(papers, args.file)
        #logging.info(f"✅ Results successfully saved to {args.file}")

    except Exception as e:
        logging.error("❌ An error occurred: %s", e, exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
