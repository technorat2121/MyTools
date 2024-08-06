import re
import argparse
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode

# Define the most vulnerable LFI parameters
lfi_parameters = [
    'file', 'document', 'folder', 'root', 'path', 'pg', 'style', 'pdf',
    'template', 'php_path', 'lang', 'language', 'load', 'view'
]

# Optionally, add the most commonly targeted file extensions
lfi_extensions = ['.php', '.asp', '.aspx', '.jsp', '.html', '.htm']

# Function to check for potential LFI parameters in URL
def find_lfi_parameters(url):
    found_params = []

    # Check if URL contains any of the potential parameters
    for param in lfi_parameters:
        if re.search(r'[?&]' + re.escape(param) + r'=', url):
            found_params.append(param)

    return found_params

# Function to deduplicate URLs
def deduplicate_urls(urls):
    seen = set()
    unique_urls = []
    for url in urls:
        # Parse the URL to normalize it (sort query params, etc.)
        parsed_url = urlparse(url.strip())
        sorted_query = sorted(parse_qsl(parsed_url.query))
        normalized_query = urlencode(sorted_query)
        normalized_url = urlunparse(parsed_url._replace(query=normalized_query))

        if normalized_url not in seen:
            seen.add(normalized_url)
            unique_urls.append(normalized_url)
    return unique_urls

# Setup argument parser
parser = argparse.ArgumentParser(description='Find potential LFI parameters in a list of URLs.')
parser.add_argument('-l', '--list', required=True, help='Path to the file containing the list of URLs.')
parser.add_argument('-o', '--output', required=True, help='Path to the file where to save the filtered URLs.')

# Parse arguments
args = parser.parse_args()

# Read URLs from the file
with open(args.list, 'r') as file:
    urls = file.readlines()

# Deduplicate URLs
unique_urls = deduplicate_urls(urls)

# Open the output file for writing
with open(args.output, 'w') as output_file:
    # Process each unique URL
    for url in unique_urls:
        found = find_lfi_parameters(url)
        if found:
            # Print detailed information to the screen
            print(f"URL: {url}")
            print(f"Potential LFI Parameters: {', '.join(found)}")
            print("-" * 50)
            # Write the URL only to the output file
            output_file.write(url + '\n')
