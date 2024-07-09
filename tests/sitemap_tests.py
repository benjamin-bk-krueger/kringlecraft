import pytest
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Now we can import from kringlecraft
from kringlecraft.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def get_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    root = ET.fromstring(response.content)

    # Define the namespace
    namespace = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    # Extract all URLs from the sitemap
    urls = [loc.text for loc in root.findall('.//sm:loc', namespace)]
    return urls


def test_sitemap_urls(client):
    # Fetch the sitemap
    sitemap_url = 'http://127.0.0.1:5006/sitemap.xml'
    urls = get_sitemap_urls(sitemap_url)

    # Test each URL
    for url in urls:
        # Convert relative URLs to absolute
        absolute_url = urljoin(sitemap_url, url)

        # Use the test client to make a request
        response = client.get(url)

        # Check if the response is successful
        assert response.status_code == 200, f"URL {absolute_url} returned status code {response.status_code}"


if __name__ == '__main__':
    pytest.main([__file__])
