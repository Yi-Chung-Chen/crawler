from unicodedata import name
import urllib.request as req
import bs4
import pandas as pd
import csv


movie_names = []
movie_ratings = []
movie_years = []
movie_content = []

links = pd.read_csv('Mylinks2.csv')
num_movie = len(links)


def main():
        for imdbid in links['imdbId']:
            
            if imdbid<1000:
                url = 'https://www.imdb.com/title/tt0000'+str(imdbid)+'/'

            elif imdbid<10000:
                url = 'https://www.imdb.com/title/tt000'+str(imdbid)+'/'

            elif imdbid<100000: #處理imdbid長度問題小於100000的話，需要補零才會讓網址正確。
                url = 'https://www.imdb.com/title/tt00'+str(imdbid)+'/'

            elif imdbid<1000000:
                url = 'https://www.imdb.com/title/tt0'+str(imdbid)+'/'

            else:
                url = 'https://www.imdb.com/title/tt'+str(imdbid)+'/'
                
            request = req.Request(url , headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
            }) #避免發生403 https request failed

            print(url)

            with req.urlopen(request) as response:
                data = response.read().decode('utf-8')
                root = bs4.BeautifulSoup(data, "html.parser")

            ratings = root.find('span',attrs = {"class":"sc-7ab21ed2-1 jGRxWM"})
            movie_ratings.append(ratings.string)

            names = root.find('div',attrs={"class":"sc-dae4a1bc-0 gwBsXc"})

            if names == None:
                names = root.find('h1',attrs={"class":"sc-b73cd867-0 eKrKux"})
                if names != None:
                    movie_names.append(names.string)
                else:
                    if names == None:
                        names = root.find('h1',attrs={"class":"sc-b73cd867-0 fbOhB"})
                        if names != None:
                            movie_names.append(names.string)
                        else:
                            if names == None:
                                names = root.find('h1',attrs={"class":"sc-b73cd867-0 cAMrQp"})
                                movie_names.append(names.string)                               
            else:
                names = str(names.string)
                movie_names.append(names[16:]) #扣除original title : 這個字串


            years = root.find('span',attrs = {"class":"sc-8c396aa2-2 itZqyK"})
            movie_years.append(years.string)

            content = root.find('span',attrs = {"class":"sc-16ede01-2 gXUyNh"})
            movie_content.append(content.string)

def movie_writer():
    file = open('movie_info.csv',mode='a', newline='')
    writer = csv.writer(file)
    for i in range(num_movie):
        writer.writerow([movie_names[i],movie_ratings[i],movie_years[i],movie_content[i]])


if __name__ == '__main__':
    main()
    movie_writer()
