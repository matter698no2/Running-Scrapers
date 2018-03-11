import meet_scraper as ms

#define paths to data here
meet = 'C:\\Users\\matte\\Desktop\\Project Footrace\\Data\\meet_info.csv'
runners = 'C:\\Users\\matte\\Desktop\\Project Footrace\\Data\\runner_info.csv'
times = 'C:\\Users\\matte\\Desktop\\Project Footrace\\Data\\time_info.csv'

#call the function
scraped_data = ms.meet_data_scraper('https://www.athletic.net/CrossCountry/Results/Meet.aspx?Meet=34300', verbose = True)

#csvs are in the order meetcsv, runnercsv, timecsv
ms.write_to_csv(scraped_data, 5000, 'w', meet, runners, times)