"""CLI entrypoint for fakename."""

import argparse
import json
import sys

from fakename.scraper import scrape_identity, scrape_multiple


def main():
    parser = argparse.ArgumentParser(
        prog="fakename",
        description="Scrape fake identities from fakenamegenerator.com",
    )
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of identities (default: 1)")
    parser.add_argument("-g", "--gender", choices=["random", "male", "female"], default="random")
    parser.add_argument("--nameset", default="us", help="Name set code (default: us)")
    parser.add_argument("--country", default="us", help="Country code (default: us)")
    parser.add_argument("-d", "--delay", type=float, default=2.0, help="Delay between requests in seconds (default: 2)")
    parser.add_argument("-o", "--output", help="Output JSON file path")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    try:
        if args.count == 1:
            result = scrape_identity(gender=args.gender, nameset=args.nameset, country=args.country)
        else:
            result = scrape_multiple(
                count=args.count, gender=args.gender, nameset=args.nameset,
                country=args.country, delay=args.delay,
            )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    indent = 2 if args.pretty else None
    json_output = json.dumps(result, indent=indent, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_output)
        print(f"Saved to {args.output}")
    else:
        print(json_output)
