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
	finish_place = []
	runner_year = []
	runner_name = []
	runner_school = []
	runner_gender = []
	finish_time = []
	
	#get the meet name as a text file
	n_o_meet = str(page_source.find('h2', class_='mBottom0 mTop0').text)
	
	vhsl_level = vhsl_level_finder(n_o_meet)
	
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
		if str(m.h4.text).split(' ')[0] == '5,000' or '8,000':
			m_runners += m.find_all('tr', class_="A")
		if str(f.h4.text).split(' ')[0] == '5,000' or '8,000':
			f_runners += f.find_all('tr', class_="A")
	
	#iterate through the male runners
	athlete = []
	pos = 0
	while pos < len(m_runners):
		try:
			if len(m_runners[pos].find_all('a')) == 3:
				athlete = m_runners[pos].find_all('a')
				year_placeholder = m_runners[pos].find_all('td')
				finish_place.append(place_to_int(year_placeholder[0].text))
				runner_year.append(str(year_placeholder[1].text))
				runner_name.append(str(athlete[0].text))
				scrubbed_time = pr_scrubber(str(athlete[1].text))
				finish_time.append(scrubbed_time)
				runner_school.append(str(athlete[2].text))
				runner_gender.append('M')
			else: 
				pass
		except IndexError:
			pass
		pos +=1
		
	#iterate through the female runners
	athlete = []
	pos = 0
	while pos < len(f_runners):
		try:
			if len(f_runners[pos].find_all('a')) == 3:
				athlete = f_runners[pos].find_all('a')
				year_placeholder = f_runners[pos].find_all('td')
				finish_place.append(place_to_int(year_placeholder[0].text))
				runner_year.append(str(year_placeholder[1].text))
				runner_name.append(str(athlete[0].text))
				scrubbed_time = pr_scrubber(str(athlete[1].text))
				finish_time.append(scrubbed_time)
				runner_school.append(str(athlete[2].text))
				runner_gender.append('F')
			else:
				pass
		except IndexError:
			pass
		pos +=1
	#generate a list of ids for each runner
	runner_ids = runner_id_generator(runner_name, runner_school)

	data_dict = {'finish_place': finish_place, 'runner_ids': runner_ids, 'runner_name': runner_name, 'runner_year': runner_year, 'runner_school': runner_school, 'finish_time': finish_time, 'runner_gender': runner_gender,
	'vhsl_group': [], 'meet_id': []}
	
	for x in range(1, len(data_dict['runner_name'])):
		data_dict['vhsl_group'].append(vhsl_level)
		data_dict['meet_id'].append(meet_id)
	
	if verbose == True:
		print "Race Scraper summary for: "
		print meet_name, ' meet id: ', meet_id,
		if vhsl_level != '':
			print '\t VHSL group: ', vhsl_level
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
	if vhsl_level != '':
		race_data['VHSL_group'] = vhsl_level
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
		
		if len(split_school) != 1 and split_school[1][0] != '(':
			try:
				id += split_school[1][0].upper()
			except IndexError:
				pass

		generated_ids.append(id)
		
	return generated_ids

def write_to_csv(data, distance, permission, meetcsv = '', runnercsv = '', timecsv = ''):
	'''
	Takes in the dictionary returned in meet scraper, and the distance run in the races
	specify the paths of the csv files in meet, runner, and time csv
	permission lets you determine if you want to write over existing info ('w'), or append an existing file ('a')
	'''
	#get the required library
	import csv
	#write meet info if specified
	if meetcsv != '':
		with open(meetcsv, permission) as meet_info:
			meet_writer = csv.DictWriter(meet_info, fieldnames = ['meet_id', 'meet_name', 'day_temperature', 'date_of_race', 'total_finishers', 'total_races', 'race_level'])
			if permission == 'wb':
				meet_writer.writeheader()
			
			meet_writer.writerow({'meet_id': data['meet_id'], 'meet_name': data['meet_name'], 'date_of_race': data['date_of_race'],
			'day_temperature': ' ', 'total_finishers': len(data['data']['runner_name']), 'total_races': ' ', 'race_level': data['race_level']})
			
	#write runner data if needed
	if runnercsv != '':
		run_keys = sorted(data['data'].keys())
		with open(runnercsv, permission) as runner_info:
			runner_writer = csv.writer(runner_info)
			if permission == 'wb':
				runner_writer.writerow(run_keys)
			runner_writer.writerows(zip(*[data['data'][key] for key in run_keys]))
		
	if timecsv != '':
		#create the data for time info
		runids = data['data']['runner_ids']
		totalmeetids = []
		totaldist = []
		totallevel = []
		x = 0
		while x < len(runids):
			totalmeetids.append(data['meet_id'])
			totaldist.append(distance)
			totallevel.append(data['VHSL_group'])
			x+=1
		
		finishtime = data['data']['finish_time']
		with open(timecsv, permission) as time_info:
			time_writer = csv.writer(time_info)

			if permission == 'wb':
				time_writer.writerow(['runner_id', 'VHSL_group', 'meet_id', 'race_distance', 'finish_time'])
	
			time_writer.writerows(zip(runids,totallevel,totalmeetids,totaldist,finishtime))
		


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
	if len(split_name) == 1:
		raceid += split_name[0].lower()
	elif len(split_name) >= 2:
		raceid += split_name[0].lower()
		raceid += split_name[1].lower()	
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
	cleanedname = ' '.join(split_name)

	return cleanedname, racelevel, raceid

def vhsl_level_finder(meet):
	'''
	Will check if any of the VHSL groups are labeled in the race name
	return the group
	'''
	group_index = ['1A','2A','3A','4A','5A','6A'] 
	split_meet = meet.split(' ')
	
	for x in split_meet:
		if x in group_index:
			group = x
		else:
			pass
	return group

def place_to_int(place):
	finish_place = int(place.split('.')[0])
	return finish_place
	
	
'''
def format_for_JSON(data, file, permission):
	
	#Takes the dictionary from meet_data_scraper and formats it for JSON export
	
	#returns a JSON compatible dictionary
	
	#make the initial levels of data
	db = {}
	db['meets'] = {}
	db['runners'] = {}
	
	db['meets'].append({
	'meet_id': data['meet_id'],
	'meet_name': data['meet_name'],
	'race_level': data['race_level'],
	'date_of_race': data['date_of_race']})
	
	dat = data['data']
	x = 0
	while x < len(dat['runner_ids']):
		db['runners'].append({
		'id': dat['runner_ids'][x],
		'name': dat['runner_name'][x],
		'school': dat['runner_school'][x],
		'gender': dat['runner_gender'][x],
		'times': {}})
		
		
		db['runners'][x]['times'].append({
		x+=1
	
	return db
'''	
	
	
	