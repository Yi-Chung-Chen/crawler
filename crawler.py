import urllib.request as req
import bs4
import pandas as pd
import csv

movie_names = []
movie_ratings = []
movie_years = []
movie_content = []
movie_img_url = []

links = pd.read_csv('Mylinks.csv')
num_movie = len(links)

def get_movies_info():

        for imdbid in links['imdbId']:
            if imdbid<100000: #處理imdbid長度問題，如果imdbid<100000的話，需要補零才會讓網址正確。
                url = 'https://www.imdb.com/title/tt00'+str(imdbid)+'/'
            else:
                url = 'https://www.imdb.com/title/tt0'+str(imdbid)+'/'
                
            request = req.Request(url , headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
            })
            with req.urlopen(request) as response:
                data = response.read().decode('utf-8')

            root = bs4.BeautifulSoup(data, "html.parser")
            
            #處理title遺失
            names = root.find('div',attrs={"class":"sc-dae4a1bc-0 gwBsXc"})
            if names ==None:
                names = root.find('h1',attrs={"class":"sc-b73cd867-0 fbOhB"})
                movie_names.append(names.string)
            else:
                names = str(names.string)
                movie_names.append(names[16:])


            ratings = root.find('span',attrs = {"class":"sc-7ab21ed2-1 jGRxWM"})
            years = root.find('span',attrs = {"class":"sc-8c396aa2-2 itZqyK"})
            content = root.find('span',attrs = {"class":"sc-16ede01-2 gXUyNh"})
            img = root.find_all('a',attrs = {"class":"ipc-lockup-overlay ipc-focusable"})
            movie_img_url.append("https://www.imdb.com/"+str(img[0].get('href'))) #設0 就可以只拿到電影封面就好
            
            movie_ratings.append(ratings.string)
            movie_years.append(years.string)
            movie_content.append(content.string)

def movie_writer():
    file = open('movie_info.csv',mode='w', newline='')
    writer = csv.writer(file)
    for i in range(num_movie):
        writer.writerow([movie_names[i],movie_ratings[i],movie_years[i],movie_content[i],movie_img_url[i]])


if __name__ == '__main__':
    get_movies_info()
    movie_writer()
