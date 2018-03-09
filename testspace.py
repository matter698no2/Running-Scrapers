from meet_scraper import meet_data_scraper
from meet_scraper import write_to_csv

scraped_data = meet_data_scraper('https://www.athletic.net/CrossCountry/Results/Meet.aspx?Meet=34300', verbose = True)

write_to_csv(scraped_data, 5000, 'C:\\Users\\Matthew\\Documents\\meetdata.csv', 'C:\\Users\\Matthew\\Documents\\runners.csv', 'C:\\Users\\Matthew\\Documents\\timedata', 'w')