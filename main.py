import argparse
from research_papers_fetcher import fetch_paper_ids, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename", default=None)
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")

    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    try:
        papers = fetch_paper_ids(args.query)

        if args.file:
            save_to_csv(papers, args.file)
            print(f"Results saved to {args.file}")
        else:
            print(papers)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
