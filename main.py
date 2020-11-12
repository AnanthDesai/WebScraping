import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

string = "https://www.freshersworld.com/jobs-in-bangalore/9999016065?&limit=50&offset={}"
offset = {0, 50, 100, 150, 200}


class Jobs:
    companyName = None
    designation = None
    qualification = None
    location = None
    link = None
    lastDate = None

    def __init__(self):
        self.companyName = []
        self.designation = []
        self.qualification = []
        self.lastDate = []
        self.location = []
        self.link = []

    def getBlocks(self):
        page = requests.get(url)
        parser = BeautifulSoup(page.content, "html.parser")
        blocks = parser.find('div', id="all-jobs-append")
        self.getDetails(blocks)

    def getDetails(self, block):
        for name in block.find_all('span', itemprop="name"):
            self.companyName.append(name.get_text())
        for designation in block.find_all('div', class_=""):
            self.designation.append(designation.get_text())
        for location in block.find_all('span', class_="job-location"):
            self.location.append(location.get_text())
        for qualification in block.find_all('span', class_="qualifications"):
            self.qualification.append(qualification.get_text())
        for lastDate in block.find_all('span', class_="padding-left-4"):
            self.lastDate.append(lastDate.get_text())
        for link in block.find_all('a',
                                   attrs={'href': re.compile('^https://'), 'class': re.compile('^view-apply-button')}):
            self.link.append(link.get('href'))
        self.putDataIntoDatabase()

    def putDataIntoDatabase(self):
        jobs = {
            'Company': self.companyName,
            'Designation': self.designation,
            'Qualifications': self.qualification,
            'Location': self.location,
            'Last Date to Apply': self.lastDate,
            'Link': self.link
        }
        dataframe = pd.DataFrame.from_dict(jobs, orient='index')
        dataframe = dataframe.transpose()
        dataframe.to_csv(r'/home/ananth/WebScrape/Jobs.csv', index=True, header=True)


job = Jobs()
for i in offset:
    url = string.format(i)
    job.getBlocks()
print("Done!")

