import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.imdb.com/list/ls091520106/"

class Movie:
    movieName = None
    releaseYear = None
    certification = None
    length = None
    genre = None
    rating = None
    metaScore = None
    plot = None
    gross = None

    def __init__(self):
        self.movieName = []
        self.releaseYear = []
        self.certification = []
        self.length = []
        self.genre = []
        self.rating = []
        self.metaScore = []
        self.plot = []
        self.gross = []

    def MovieBlock(self):
        source = requests.get(url)
        parser = BeautifulSoup(source.content, "html.parser")
        mainBlock = parser.find('div', class_="lister-list")
        self.Movies(mainBlock)

    def Movies(self, mainBlock):
        crew_combine = []
        rating = []
        i = 0
        j = 0
        k = 0
        for name in mainBlock.find_all('a', attrs={'href': re.compile('^/title/')}):
            self.movieName.append(list(name)[0])
        for year in mainBlock.find_all('span', class_="lister-item-year"):
            self.releaseYear.append(year.get_text())
        for cert in mainBlock.find_all('span', class_="certificate"):
            self.certification.append(cert.get_text())
        for length in mainBlock.find_all('span', class_="runtime"):
            self.length.append(length.get_text())
        for genre in mainBlock.find_all('span', class_="genre"):
            self.genre.append(genre.get_text())
        for rating in mainBlock.find_all('span', class_="ipl-rating-star__rating"):
            if i % 23 == 0:
                self.rating.append(rating.get_text())
            i = i+1
        for meta in mainBlock.find_all('span', class_="metascore"):
            self.metaScore.append(meta.get_text())
        for plot in mainBlock.find_all('p', class_=""):
            self.plot.append(plot.get_text())
        for gross in mainBlock.find_all('span', attrs={'data-value': re.compile('^[0-9]+[,]')}):
            self.gross.append(gross.get_text())

        while " " in self.movieName:
            self.movieName.remove(" ")



        self.pushDatabase()


    def pushDatabase(self):
        movies = {
            'Title': self.movieName,
            'Year of Release': self.releaseYear,
            'Certification': self.certification,
            'Duration': self.length,
            'Genre': self.genre,
            'Rating': self.rating,
            'Metascore': self.metaScore,
            'Plot': self.plot,
            'Market': self.gross
        }
        dataframe = pd.DataFrame.from_dict(movies, orient='index')
        dataframe = dataframe.transpose()
        dataframe.to_csv(r'/home/ananth/WebScrape/Movies.csv', header=True)


movie = Movie()
movie.MovieBlock()
