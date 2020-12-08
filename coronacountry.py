# parsing coronavirusstat.ru statistics for Russia
from datetime import datetime
from prettytable import PrettyTable
from coronavirus import CoronaVirus

def main():
	start = datetime.now()
	cv = CoronaVirus(url="https://coronavirusstat.ru", filename='coronavirus.json')
	
	# ---- write coutry json 
	html_ = cv.get_html()
	country_links_ = cv.get_country_links(html_)
	if country_links_ is not False and len(country_links_) > 0:
		cv.write_json(data = country_links_, path = 'links_country.json')
		# ---- return print
		for index, country_ in enumerate(country_links_, 1):
			cv.p(index, country_)
	
	# ---- load json
	cl_ = cv.load_json(path = 'links_country.json')
	if cl_ is not False and len(cl_) > 0:
		for index, country_ in enumerate(cl_, 1):
			cv.p(index, country_)

	# end
	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()	