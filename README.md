# Running Scrapers
meet-scraper.py contains the master list of functions

### Quick Note
This is taylor made for the results page of Athletic.net, it will work on any meet from their site, but not outside of it. The VHSL 

## List of functions
1. meet_data_scraper(url, verbose)
takes a url as a string and gathers:
- Runner name, time, and school
- meet name and date
- generates a meet id
returns a dictionary with all the above information
if verbose is set to true, a readout of the basic information will be
printed

2. runner_id_generator(name, school)
takes two lists representing a runner's name and school
will return a list of ids for the runners
ids are formatted like:
Matthew Rogers, Hidden Valley => matrogHV
Jen Flemming, Blacksburg => jenflemB

3. write_to_csv(data, distance, permission, meetcsv, runnercsv, timecsv)
Takes a dictionary formatted like the one returned in meet_data_scraper and writes the information to csvs as specified
 - distance should either be 5000 or 8000, the scraper automatically ignores anything other than that
 - meetcsv, runnercsv, and timecsv are paths ('C:\\path...) you MUST define the path as meetcsv = 'C:\\path...' or it wont work. The order of the csv paths don't matter
 - permission is a string ('w', 'a')

4. pr_scrubber(time)
on Athletic.net, if a runner runs a PR, it's included in the time string. That's annoying and messes up my dataset rn, I don't want it. This simply takes the time as a string, checks to see if 'PR' is there, and if it is, remove it. 

5. meet_id_generator(meet, date)
This was supposed to me simple, but sort of ballooned a bit. This makes the meet id, so if the meet was Clash with the Titans 2014, the id is cwtt14. 
This returns:
 - a cleaned version of the meet name
 - the race level (HS or Collegiate)
 - the race id

## Planned Features
Just to keep track of the stuff I want to add or improve
 - Mark whether a runner ran a PR at the meet
 - General debugging and scenario checking
