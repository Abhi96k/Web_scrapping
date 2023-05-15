import requests
from bs4 import BeautifulSoup

# The URL of the YouTube channel or search query to scrape
url = "https://www.youtube.com/results?search_query=python+programming"

# Send a GET request to the URL and store the response in a variable
response = requests.get(url)

# Use BeautifulSoup to parse the HTML content of the response
soup = BeautifulSoup(response.content, "html.parser")

# Find all the <a> tags that contain video titles and links
video_links = soup.find_all("a", {"class": "yt-uix-tile-link"})

# Loop through the links and print the title and URL of each video
for link in video_links:
    title = link.get("title")
    url = "https://www.youtube.com" + link.get("href")
    print(f"{title}: {url}")
