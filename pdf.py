import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pypdf import PdfReader


def download_pdfs_from_page(url, output_folder="pdf_downloads"):
    try:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the HTML content of the page
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links ending with .pdf
        pdf_links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.lower().endswith(".pdf"):
                full_url = urljoin(url, href)
                pdf_links.append(full_url)

        if not pdf_links:
            print("No PDF files found on the page.")
            return

        print(f"Found {len(pdf_links)} PDF(s). Downloading...")

        # Download each PDF
        for pdf_url in pdf_links:
            file_name = os.path.basename(urlparse(pdf_url).path)
            file_path = os.path.join(output_folder, file_name)

            try:
                pdf_response = requests.get(pdf_url, timeout=15)
                pdf_response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(pdf_response.content)
                print(f"Downloaded: {file_name}")
            except Exception as e:
                print(f"Failed to download {pdf_url}: {e}")

    except requests.RequestException as e:
        print(f"Error fetching page: {e}")


# Example usage:
# download_pdfs_from_page(
#     "https://sistemasprefeitura.cachoeiro.es.gov.br/servicos/site.php?nomePagina=SERFARM&anoplantao=2026&mesplantao=05")

download_pdfs_from_page(
    "https://sistemasprefeitura.cachoeiro.es.gov.br/servicos/site.php?nomePagina=SERFARM&anoplantao=PlantaoAnual")

reader = PdfReader('pdf_downloads/PLANTÃO FARMÁCIAS E DROGARIAS 2025 2026.pdf')


print(len(reader.pages))
# creating a page object
page = reader.pages[2]

# extracting text from page
print(page.  extract_text(extraction_mode="layout"))
