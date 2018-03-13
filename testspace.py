import meet_scraper as ms
from time import sleep
from time import time
from random import randint

#define paths to data here
meet = 'C:\\Users\\matte\\Desktop\\Project Footrace\\Data\\meet_info.csv'
runners = 'C:\\Users\\matte\\Desktop\\Project Footrace\\Data\\runner_info.csv'
times = 'C:\\Users\\matte\\Desktop\\Project Footrace\\Data\\time_info.csv'

#every url index for the VHSL state meet 2013-2017
urls = [89473, 89472, 89471, 89476, 89475, 89474, 89482, 89481,
89480, 89479, 89478, 89477, 115718, 115719, 115720, 115723, 115722, 115721,
129756, 129755, 129754, 129759, 129758, 129757, 143636, 143637, 143638, 143656, 143682]        

start_time = time()
requests = 0


#call the function
scraped_data = ms.meet_data_scraper('https://www.athletic.net/CrossCountry/Results/Meet.aspx?Meet=143681', verbose = True)
ms.write_to_csv(scraped_data, 5000, 'w', meet, runners, times)

sleep(randint(2,5))
requests += 1
elapsed_time = time() - start_time

print 'Request no: ', requests, '\telapsed time: ', elapsed_time
for year_url in urls:
	url = 'https://www.athletic.net/CrossCountry/Results/Meet.aspx?Meet=' + str(year_url)
	
	scraped_data = ms.meet_data_scraper(url, verbose = True)
	ms.write_to_csv(scraped_data, 5000, 'a', meet, runners, times)
	
	sleep(randint(2,5))
	requests += 1
	elapsed_time = time() - start_time

	print 'Request no: ', requests, '\telapsed time: ', elapsed_time