'''
import requests
from bs4 import BeautifulSoup

# Send an HTTP request to the URL of the webpage you want to access
url = "https://python.langchain.com/docs/integrations/vectorstores/chroma"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Extract the text content of the webpage
text = soup.get_text()
filename = 'scraped_data.txt'

# Save the data to a text file
with open(filename, 'w', encoding='utf-8') as outF:
    # Write the text to the file
    outF.write(text)



print(text)
print("        \
    $-&3+)$_   \
skjfekjdnd    snfkend ")


from langchain.document_loaders import WebBaseLoader

# Define the URL of the web page you want to scrape
# url = "https://www.example.com"

# Initialize the WebBaseLoader with the URL
loader = WebBaseLoader(url)

# Load the document from the web page
document = loader.load()

# Print the loaded document
print(document)
'''

import requests
from bs4 import BeautifulSoup
import os

# Define the paths to the URL list file and the processed URLs file
url_list_path = 'urls.txt'
processed_urls_path = 'processed_urls.txt'
unique_folder = 'wpages'

# Ensure the unique folder exists
if not os.path.exists(unique_folder):
    os.makedirs(unique_folder)

# Load the list of processed URLs
try:
    with open(processed_urls_path, 'r') as file:
        processed_urls = file.read().splitlines()
except FileNotFoundError:
    processed_urls = []

# Load the list of URLs to process
with open(url_list_path, 'r') as file:
    urls_to_process = file.read().splitlines()

# Process each URL
for url in urls_to_process:
    if url not in processed_urls:
        try:
            # Send an HTTP request to the URL
            response = requests.get(url)
            response.raise_for_status() # Raises an HTTPError if the response status is 4xx or 5xx

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract the text content of the webpage
            text = soup.get_text()

            # Create a unique filename based on the URL
            # Replace special characters and use the URL as the filename
            filename = os.path.join(unique_folder, url.replace('http://', '').replace('https://', '').replace('/', '_').replace('.', '_')) + '.txt'

            # Ensure the file exists
            if not os.path.exists(filename):
                with open(filename, 'w', encoding='utf-8') as file:
                    pass # Create the file

            # Write the data to the file
            with open(filename, 'w', encoding='utf-8') as outF:
                outF.write(text)

            # Add the URL to the list of processed URLs
            processed_urls.append(url)
            print(f"Processed {url} and saved to {filename}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while processing {url}: {e}")

# Update the list of processed URLs
with open(processed_urls_path, 'w') as file:
    for url in processed_urls:
        file.write(url + '\n')

print("Finished processing URLs.")
