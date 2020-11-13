import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv

string = "https://www.freshersworld.com/jobs-in-bangalore/9999016065?&limit=50&offset={}"
offset = {0, 50, 100, 150}


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
        # print(self.companyName)


class Database(Jobs):
    def putDataIntoDatabase(self, Jobs):
        jobs = {
            'Company': Jobs.companyName,
            'Designation': Jobs.designation,
            'Qualifications': Jobs.qualification,
            'Location': Jobs.location,
            'Last Date to Apply': Jobs.lastDate,
            'Link': Jobs.link
        }
        dataframe = pd.DataFrame.from_dict(jobs, orient='index')
        dataframe = dataframe.transpose()
        dataframe.to_csv(r'/home/ananth/WebScrape/Jobs.csv', index=True, header=True)


job = Jobs()
data = Database()
for i in offset:
    url = string.format(i)
    job.getBlocks()
    data.putDataIntoDatabase(job)
print("Done!")

print("Search by: ")
print('1.Company')
print('2.Designation')
print('3.Location')
print('4.Qualification')
print('5.Exit')
choice = 0
while int(choice) != 5:
    choice = input("Choice: ")

    if(int(choice) == 1):
        company = input('Enter Company:')
        with open(r'/home/ananth/WebScrape/Jobs.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == company:
                    print(row)
    if(int(choice) == 2):
        designation = input('Enter Designation:')
        with open(r'/home/ananth/WebScrape/Jobs.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == designation:
                    print(row)
    if(int(choice) == 3):
        location = input('Enter Location:')
        with open(r'/home/ananth/WebScrape/Jobs.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[4] == location:
                    print(row)
    if(int(choice) == 4):
        qualification = input('Enter Qualification:')
        with open(r'/home/ananth/WebScrape/Jobs.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[3] == qualification:
                    print(row)
