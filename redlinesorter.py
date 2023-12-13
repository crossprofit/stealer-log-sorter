import os
import re

base_dir = 'base'
output_file = 'sorted_credentials.txt'

def find_files(base):
    for root, dirs, files in os.walk(base):
        if 'Passwords.txt' in files:
            yield os.path.join(root, 'Passwords.txt')

def extract_credentials(file_path):
    try:
        with open(file_path, 'r', encoding='utf8', errors='ignore') as file:
            content = file.read()
            urls = re.findall('URL: (.*?)\n', content)
            usernames = re.findall('Username: (.*?)\n', content)
            passwords = re.findall('Password: (.*?)\n', content)
            if len(urls) == len(usernames) == len(passwords):
                return list(zip(urls, usernames, passwords))
    except Exception as e:
        print(f'Error processing file {file_path}: {str(e)}')

from urllib.parse import quote

def write_to_file(credentials, output_file):
    with open(output_file, 'a', encoding='utf-8') as file:
        for credential in credentials:
            safe_url = quote(credential[0], safe='/:@%')  # URL encode the URL part
            username = credential[1]  # Keep the username as it is
            password = credential[2]  # Keep the password as it is
            file.write(f'{safe_url}:{username or "EMAIL"}:{password}\n')

credentials = []
for file in find_files(base_dir):
    print(f'Scanning file: {file}')
    file_credentials = extract_credentials(file)
    if file_credentials:
        credentials.extend(file_credentials)
    else:
        print(f'No credentials found in file: {file}')

if credentials:
    print(f'Writing credentials to file: {output_file}')
    write_to_file(credentials, output_file)
else:
    print('No credentials found to write.')
