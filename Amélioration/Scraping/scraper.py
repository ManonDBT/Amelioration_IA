import json
import time
import re

import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys



class Films:
    def __init__(self, titre, annee, certificate, duree, genres, stars, metascore, vote, description):
        self.titre = titre
        self.annee = annee 
        self.certificate = certificate
        self.metascore = metascore 
        self.stars = stars 
        self.genre = genres
        self.duree = duree
        self.vote = vote
        self.description = description
        
    def get_json(self):
        return {'titre': self.titre, 'année': self.annee, 'certificate': self.certificate, 'genre': self.genre, 'durée': self.duree, 'metascore':self.metascore, 'stars': self.stars, 'votes': self.vote, 'description': self.description}

class Scraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        
        self.films = []

    

    def scrap(self):
        self.browser = webdriver.Remote("http://127.0.0.1:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME, options=self.options)
        print('début')
    
        def next(nombre):
            
            self.browser.get('https://www.imdb.com/search/title/?title_type=feature&start=' + str(nombre))
            time.sleep(1)
            
            films_div = self.browser.find_elements_by_class_name('lister-item')
           
            
            for film in films_div : 
                titre = film.find_element_by_xpath('.//h3/a').text
                
                try :
                    annee = film.find_element_by_xpath('.//h3/span[2]').text.replace('(','').replace(')','').replace(' ','')
                    annee = int(re.sub('[^0-9]', '', annee))
                except: 
                    annee = None
                
                try: certificate = film.find_element_by_class_name('certificate').text
                except: certificate = None
                
                try: duree = int(film.find_element_by_class_name('runtime').text.replace(' min', ''))
                except: duree = None
                
                try: genres = film.find_element_by_class_name('genre').text.split(', ')
                except: genres = []
                
                try: stars = float(film.find_element_by_xpath('.//div[1]/strong').text)
                except: stars = None
                
                try: metascore = int(film.find_element_by_xpath('.//div[3]/span').text)
                except: metascore = None 
                
                try: vote = int(film.find_element_by_xpath('.//div[3]/p[4]/span[2]').text)
                except: vote = None 
                
                try: description = film.find_element_by_xpath('.//div[3]/p[2]').text
                except: description = [] 
                
                film = Films(titre, annee, certificate, duree, genres, stars, metascore, vote, description)
                self.films.append(film)
                
                print(film.titre)
                print(len(self.films))
                
        
        nombre = 1 
        while True : 
            next(nombre)
            nombre +=50
            
    
    
    def export_json(self):
        data = {'data' : [film.get_json() for film in self.films]}
        
        with open('imdb.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
        
scraper = Scraper()

try :     
    scraper.scrap()

finally: 
    scraper.browser.quit()
    scraper.export_json()
