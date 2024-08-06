import re
import argparse
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode

# Define potential SQLi parameters by file type
sqli_parameters = {
    '.php': [
        'category', 'id', 'article_id', 'username', 'password', 'q',
        'post_id', 'thread_id', 'user_id', 'page', 'lang', 'search',
        'sort', 'order', 'dir', 'type', 'date', 'name', 'id'
    ],
    '.asp': [
        'catid', 'id', 'newsid', 'username', 'password', 'q',
        'postid', 'threadid', 'userid', 'item', 'prodid', 'key',
        'sort', 'order', 'date', 'action', 'page'
    ],
    '.aspx': [
        'catid', 'id', 'newsid', 'username', 'password', 'q',
        'postid', 'threadid', 'userid', 'product_id', 'view', 'sessionid',
        'sort', 'order', 'action', 'page', 'type'
    ],
    '.cfm': [
        'catid', 'id', 'newsid', 'username', 'password', 'q',
        'postid', 'threadid', 'userid', 'item', 'product_id', 'view',
        'sort', 'order', 'action', 'page', 'categoryid'
    ],
    '.jsp': [
        'catid', 'id', 'newsid', 'username', 'password', 'q',
        'postid', 'threadid', 'userid', 'item', 'product_id', 'action',
        'sort', 'order', 'view', 'page', 'session'
    ],
    '.htm': [
        'id', 'page', 'view', 'search', 'query', 'lang',
        'category', 'type', 'sort', 'order', 'date', 'filter'
    ],
    '.pl': [
        'id', 'page', 'view', 'search', 'query', 'lang',
        'category', 'type', 'sort', 'order', 'date', 'filter'
    ],
    '.py': [
        'id', 'page', 'view', 'search', 'query', 'lang',
        'category', 'type', 'sort', 'order', 'date', 'filter'
    ],
    '.cgi': [
        'id', 'page', 'view', 'search', 'query', 'lang',
        'category', 'type', 'sort', 'order', 'date', 'filter'
    ]
}

# Function to extract file extension from URL
def get_file_extension(url):
    match = re.search(r'\.(php|asp|aspx|cfm|jsp|html|htm|pl|py|cgi)', url)
    return match.group(0) if match else None

# Function to check for potential SQLi parameters in URL
def find_sqli_parameters(url):
    file_extension = get_file_extension(url)
    if not file_extension:
        return None

    potential_params = sqli_parameters.get(file_extension, [])
    found_params = []

    # Check if URL contains any of the potential parameters
    for param in potential_params:
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
parser = argparse.ArgumentParser(description='Find potential SQLi parameters in a list of URLs.')
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
        found = find_sqli_parameters(url)
        if found:
            # Print detailed information to the screen
            print(f"URL: {url}")
            print(f"Potential SQLi Parameters: {', '.join(found)}")
            print("-" * 50)
            # Write the URL only to the output file
            output_file.write(url + '\n')
