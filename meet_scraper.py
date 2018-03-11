'''
This is a general function that will read a url
and scrape all the related info from the said url

It will store all the wanted data in csv files as needed

Created by: Matthew Rogers
'''

def meet_data_scraper(url, verbose = False):
	'''
	See above for greater detail in functionality

	verbose will print a summary of the meet if set to true
	'''
	#import the required libraries
	from bs4 import BeautifulSoup as bs
	from requests import get
	import string

	#convert the url to text for parsing
	page_source = bs(get(url).text, 'html.parser')

	#create the dict/lists to be appended to the various csv documents
	runner_name = []
	runner_school = []
	runner_gender = []
	finish_time = []
	
	#get the meet name as a text file
	n_o_meet = str(page_source.find('h2', class_='mBottom0 mTop0').text)

	#get the date
	date_of_race = str(page_source.find('span', class_='text-info').b.text)
	dateorace = string.replace(date_of_race, ',', '')
	split_date = dateorace.split(' ')

	meet_name, race_level, meet_id = meet_id_generator(n_o_meet, dateorace)
	#split the data into M/F
	male_results = page_source.find('div', id ='gender_M')
	female_results = page_source.find('div', id ='gender_F')

	#get the number of races and race distance
	male_races = male_results.find_all('tbody', class_= 'DivBody')
	female_races = female_results.find_all('tbody', class_= 'DivBody')
	
	m_runners = []
	f_runners = []
	for m,f in zip(male_races, female_races):
		if str(m.h4.text).split(' ')[0] == '5,000':
			m_runners += m.find_all('tr', class_="A")
		if str(f.h4.text).split(' ')[0] == '5,000':
			f_runners += f.find_all('tr', class_="A")
	
	#iterate through the male runners
	athlete = []
	pos = 0
	while pos < len(m_runners):
		try:
			athlete = m_runners[pos].find_all('a')
			runner_name.append(str(athlete[0].text))
			scrubbed_time = pr_scrubber(str(athlete[1].text))
			finish_time.append(scrubbed_time)
			runner_school.append(str(athlete[2].text))
			runner_gender.append('M')
		except IndexError:
			pass
		pos +=1
		
	#iterate through the female runners
	athlete = []
	pos = 0
	while pos < len(f_runners):
		try:
			athlete = f_runners[pos].find_all('a')
			runner_name.append(str(athlete[0].text))
			scrubbed_time = pr_scrubber(str(athlete[1].text))
			finish_time.append(scrubbed_time)
			runner_school.append(str(athlete[2].text))
			runner_gender.append('F')
		except IndexError:
			pass
		pos +=1
	#generate a list of ids for each runner
	runner_ids = runner_id_generator(runner_name, runner_school)

	data_dict = {'runner_ids': runner_ids, 'runner_name': runner_name, 'runner_school': runner_school, 'finish_time': finish_time, 'runner_gender': runner_gender}
	
	if verbose == True:
		print "Race Scraper summary for: "
		print meet_name, ' meet id: ', meet_id
		print "-----------------------"
		print 'First Row: ', [item[0] for item in data_dict.values()]
		print "Number of Names\t", len(runner_name)
		print "Number of Times\t", len(finish_time)
	
	race_data = {'meet_name': meet_name, 
	'meet_id': meet_id,
	'race_level': race_level,
	'date_of_race': dateorace,
	'data': data_dict
	}
	return	race_data  

def runner_id_generator(name, school):
	'''
	Wiil take in a list of names and a list of schools
	Makes a unique id for the runner. 
	Id is first three letters of the first and last name + school
	EX: Matthew Rogers from Hidden Valley => matrogHV
	'''
	generated_ids = []
	
	for n,s in zip(name,school):
		id = ''
		split_name = n.split(' ')
		split_school = s.split(' ')
		id += split_name[0][0:3].lower()
		id += split_name[1][0:3].lower()
		id += split_school[0][0].upper()
		try:
			id += split_school[1][0].upper()
		except IndexError:
			pass
		
		generated_ids.append(id)
		
	return generated_ids

def write_to_csv(data, distance, meetcsv, runnercsv, timecsv, permission):
	'''
	Takes in the dictionary returned in meet scraper, and the distance run in the races
	specify the paths of the csv files in meet, runner, and time csv
	permission lets you determine if you want to write over existing info ('w'), or append an existing file ('a')
	'''
	#get the required library
	import csv
	
	#define and open the files
	meet_info = open(meetcsv, permission)
	runner_info = open(runnercsv, permission)
	time_info = open(timecsv, permission)
	
	#write to meet_info
	with meet_info:
		meet_writer = csv.DictWriter(meet_info, fieldnames = ['meet_id', 'meet_name', 'day_temperature', 'date_of_race', 'total_finishers', 'total_races', 'race_level'])
		if permission == 'w':
			meet_writer.writeheader()
		meet_writer.writerow({'meet_id': data['meet_id'], 'meet_name': data['meet_name'], 'date_of_race': data['date_of_race'],
		'day_temperature': ' ', 'total_finishers': len(data['data']['runner_name']), 'total_races': ' ', 'race_level': data['race_level']})
	
	run_keys = sorted(data['data'].keys())
	with runner_info:
		runner_writer = csv.writer(runner_info)
		if permission == 'w':
			runner_writer.writerow(run_keys)
		runner_writer.writerows(zip(*[data['data'][key] for key in run_keys]))
		
	
	#create the data for time info
	runids = data['data']['runner_ids']
	totalmeetids = []
	totaldist = []
	x = 0
	while x < len(runids):
		totalmeetids.append(data['meet_id'])
		totaldist.append(distance)
		x+=1
		
	finishtime = data['data']['finish_time']
	with time_info:
		time_writer = csv.writer(time_info)

		if permission == 'w':
			time_writer.writerow(['runner_id', 'meet_id', 'race_distance', 'finish_time'])

		time_writer.writerows(zip(runids,totalmeetids,totaldist,finishtime))
		


	return

def pr_scrubber(time):
	'''
	Will read a time and if 'PR' is on it, remove it and return the time without it 
	'''
	sTime = time.split(' ')
	try:
		del sTime[1]
	except IndexError:
		pass
	return sTime[0]

def meet_id_generator(meet, date):
	'''
	Takes the meet name as a string
	generates an id and identifies the race level
	returns the id 
	'''
	
	split_name = meet.split(' ')
	
	#create the race id
	raceid = ''
	#append the first letters of every word in the title
	for x in split_name:
			raceid += x[0].lower()
	#add the year
	#2-5 is the last two characters if the date string
	#get the date
	split_date = date.split(' ')
	raceid += split_date[len(split_date) - 1][2:5]

	#get the race level (HS or college)
	#there are only two levels, HS and collegiate
	#so the level can be identified from the last letter
	if meet[len(meet) - 1] == 'S':
		racelevel = 'HS'
	else:
		racelevel = 'Collegiate'
	
	#clean the race level off the race name string
	del split_name[len(split_name) - 1]
	meetname = ' '.join(split_name)

	return meetname, racelevel, raceid
