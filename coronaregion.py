# parsing coronavirusstat.ru statistics for Russia
from datetime import datetime
from prettytable import PrettyTable
from coronavirus import CoronaVirus

def main():
	start = datetime.now()
	cv = CoronaVirus(url="https://coronavirusstat.ru", filename='coronavirus.json')
	
	# ---- write region json 
	html_ = cv.get_html()
	region_links_ = cv.get_region_links(html_)
	if region_links_ is not False and len(region_links_) > 0:
		cv.write_json(data = region_links_, path = 'links_region.json')
		# ---- return print
		for index, region_ in enumerate(region_links_, 1):
			cv.p(index, region_)
	
	# ---- load json
	rl_ = cv.load_json(path = 'links_region.json')
	if rl_ is not False and len(rl_) > 0:
		for index, region_ in enumerate(rl_, 1):
			cv.p(index, region_)

	# end
	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()	