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


'''
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
