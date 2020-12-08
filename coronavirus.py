# parsing coronavirusstat.ru statistics for Russia
import sys
import requests, fake_useragent  # pip install requests
import json
import re
from bs4 import BeautifulSoup
# There is now beautifulsoup4 for Python 3.6.

class CoronaVirus():
    """parsing coronavirusstat.ru statistics for Russia"""
    def __init__ (self, url="https://coronavirusstat.ru", filename="coronavirus.json"):
        self.url = url
        self.filename = filename
    
    @staticmethod
    def p(text, *args):
        print(text, *args, sep=' / ', end='\n')

    # regular function removes control characters \t \n \r
    @staticmethod
    def dntr(now):        
        # return re.sub("^\s+|\n|\r|\t|\s+$", '', now).replace('+', ' +')   	
        return ' '.join(re.sub("^\s+|\r|\t|\s+$", '', now).split()).replace(' +', '+').replace('+', ' +')

    @staticmethod
    def get_mortality_description():
        mortality_ = []
        mortality_.append('*Летальность 1 = Умершие/(Случаев)*100')
        mortality_.append('*Летальность 2 = Умершие/(Вылеченные+Умершие)*100')
        return mortality_
    
    def write_json(self, data, path = None):
        path = self.filename if path is None else path
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_json(self, path = None):
        path = self.filename if path is None else path
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
        return {}  

    # Random User-Agent
    def get_html(self):        
        ua = fake_useragent.UserAgent() 
        user = ua.random
        header = {'User-Agent':str(user)}
        try:
            page = requests.get(self.url, headers = header, timeout = 10)
            return page.text
        except Exception as e:
            print(sys.exc_info()[1])
            return False

    def get_all_links(self, html):
        if html is False:
            return False
        soup = BeautifulSoup(html, 'lxml')
        teg_ = soup.find('body').find_all('div', class_='container')
        
        # ---- the Header for Russia
        h = []
        for h_ in soup.find('body').find_all('h1', class_='h2 font-weight-bold'):
            p_ = h_.parent	
            l_ = []
            for ht_ in p_.find('div', class_='row justify-content-md-center').find_all('div', class_='col col-6 col-md-3 pt-4'):			
                l_.append([x.text.strip() for x in ht_.find_all('div')])			
            h.append({'h1':[p_.find('h1').text.strip(), p_.find('h6').text.strip().replace('Обновление через','')], 'body':l_})
        
        # ---- the statistics for Russia
        links = []
        for row_ in teg_[1].find_all('div',class_='c_search_row'):
            sity_ = row_.find('div',class_='p-1 col-5').find('span', class_='small')
            name_ = sity_.text.strip()
            a_ = sity_.find('a').get('href')

            row = []
            row.append(a_)
            row.append(name_)

            # ---- the table select ----
            num_ = row_.find('div',class_='p-1 col-7 row m-0')          
            for d_ in num_.find_all('div', class_='p-1'):                
                ns_ = d_.find('div', class_='small text-muted').text.strip()
                h6_ = self.dntr(d_.find('div', class_='h6').text.strip())
                row.append([ns_, h6_])

            links.append(row)
        
        # ---- the statistics for world
        worlds_ = []
        for country in teg_[1].find_all('div',class_='c_search2_row'):
            country_name_ = country.find('div', class_='p-2 col-4').find('span', class_='h6')
            country_name_text_ = country_name_.text.strip()
            country_name_url_ = country_name_.find('a').get('href')
            #
            country_description_ = country.find('div', class_='p-2 col-4').find('div', class_='small text-muted')
            country_description_.find('span').extract()
         
            # ---- the country from world
            w_ = []
            w_.append(country_name_url_)
            w_.append(country_name_text_)
            w_.append(country_description_.text.strip())

            # ---- the table select
            table_ = country.find('div', class_='p-1 col-8 row')
            for t_ in table_.find_all('div', class_='p-1'):
                ts_ = t_.find('div', class_='small text-muted').text.strip()
                th_ = self.dntr(t_.find('div', class_='h6').text.strip())
                w_.append([ts_, th_])

            worlds_.append(w_)
        
        return {'header':h, 'links':links, 'worlds':worlds_}

    # the return country URL links
    def get_country_links(self, html):
        if html is False:
            return False
        soup = BeautifulSoup(html, 'lxml')
        teg_ = soup.find('body').find_all('div', class_='container')
        
        worlds_ = []
        for country in teg_[1].find_all('div',class_='c_search2_row'):
            country_name_ = country.find('div', class_='p-2 col-4').find('span', class_='h6')
            country_name_text_ = country_name_.text.strip()
            country_name_url_ = country_name_.find('a').get('href')
            #
            country_description_ = country.find('div', class_='p-2 col-4').find('div', class_='small text-muted')
            country_description_.find('span').extract()

            # ---- the country from world
            w_ = []
            w_.append(country_name_url_)
            w_.append(country_name_text_)
            w_.append(country_description_.text.strip())

            worlds_.append(w_)

        return worlds_

    # the return region links
    def get_region_links(self, html):
        if html is False:
            return False
        soup = BeautifulSoup(html, 'lxml')
        teg_ = soup.find('body').find_all('div', class_='container')

        region_ = [] 
        for row_ in teg_[1].find_all('div',class_='c_search_row'):
            sity_ = row_.find('div',class_='p-1 col-5').find('span', class_='small')
            name_ = sity_.text.strip()
            a_ = sity_.find('a').get('href')

            row = []
            row.append(a_)
            row.append(name_)
            
            region_.append(row)

        return region_
