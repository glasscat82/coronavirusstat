# parsing coronavirusstat.ru statistics for Russia
from datetime import datetime
from prettytable import PrettyTable
from coronavirus import CoronaVirus

def main():
	start = datetime.now()
	cv = CoronaVirus(url="https://coronavirusstat.ru", filename='coronavirus.json')
	
	#----
	html_ = cv.get_html()
	teg_ = cv.get_all_links(html_)
	teg_header_ = ', '.join(teg_['header'][0]['h1'])
	
	#----
	b_ = teg_['header'][0]['body']
	column_names = [c_[len(c_)-1] for c_ in b_]
	x = PrettyTable()
	for index, t_ in enumerate(b_, 0):
		tl_ = [s_ for index, s_ in enumerate(t_, 0) if index < len(t_)-1 ]
		x.add_column(column_names[index], tl_)
	print(x.get_string(title = teg_header_))
	
	# ---
	x = PrettyTable()
	x.field_names = ["№", "Регион", "Случаев", "Активных", "Вылечено", "Умерло", "Летальность*"]
	x.align["Регион"] = "l"
	for index, r_ in enumerate(teg_['links'], 1):
		x.add_row([index, r_[1], r_[2][1], r_[3][1], r_[4][1], r_[5][1], r_[6][1]])
	# # x.sortby = "Умерло"
	# # x.reversesort = True
	print(x.get_string(title = teg_header_))

	# end
	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()	