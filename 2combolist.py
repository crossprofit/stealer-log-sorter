import os
import re
import logging
from urllib.parse import urlparse, quote
import unicodedata

# Logging configuration
logging.basicConfig(filename='error.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

def extract_credentials(line, domain):
    try:
        line = unicodedata.normalize('NFC', line)
        match = re.search(r'(.*://[^\s/]+(?:/[^\s]*))?(:[^:]+:[^\s]+)?', line)
        if match:
            url_string = quote(match.group(1), safe=':/@')
            url = urlparse(url_string)
            if url.netloc == domain:
                return line    # Return the entire line
        return None
    except Exception as e:
        logging.error(f"Error in extract_credentials: {e}")
        return None

def process_file(filename, url):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line_match = extract_credentials(line, url)
                if line_match:    # If a URL match is found
                    yield line_match    # Yield the entire line
    except Exception as e:
        logging.error(f"Error in process_file: {e}")

def process_directory(directory, url):
    credentials = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                credentials.extend(list(process_file(os.path.join(directory, filename), url)))
        return credentials
    except Exception as e:
        logging.error(f"Error in process_directory: {e}")
        return []

def write_to_file(credentials, output_file):
    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            for cred in sorted(credentials):
                file.write(cred.rstrip() + '\n')
    except Exception as e:
        logging.error(f"Error in writing file: {e}")

# Main execution
url = input("Enter a URL to search for credentials: ")
parsed_url = urlparse(url)
domain = parsed_url.netloc
credentials = process_directory('base', domain)
print(f"Found credentials: {credentials}")

if credentials:
    try:
        write_to_file(credentials, 'credentials.txt')
    except Exception as e:
        print(f"Error in writing file: {e}")
else:
    print("No credentials found.")