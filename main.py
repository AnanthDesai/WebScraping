import requests
from bs4 import BeautifulSoup
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
parser = BeautifulSoup(page.content,"html.parser")
print(parser.prettify())
