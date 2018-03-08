# Running Scrapers
meet-scraper.py contains the master list of functions

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

3. write_to_csv(data, distance)
Still a wip, but will take the dictionary returned in #1 and print the info to
csv files. 