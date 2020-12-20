# parsing coronavirusstat.ru statistics for Russia
from datetime import datetime
from prettytable import PrettyTable
from coronavirus import CoronaVirus

def main():
	start = datetime.now()
	cv = CoronaVirus(url="https://coronavirusstat.ru", filename='coronavirus.json')
	
	# ---- write news json 
	html_news = cv.get_html(url_page = "https://coronavirusstat.ru/news/")
	news_links_ = cv.get_news_links(html_news)
	for n in news_links_:
		cv.p(n)

	# end
	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()	