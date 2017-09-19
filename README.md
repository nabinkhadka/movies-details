# Movie Details Scraper with Login feature

This scraper can give you CSV file that contains hundred of movies and their details along with IMBD details. I have scraped http://gomo.to/ just for showing purpose. This is very simple example of how to scrape website that needs login at first. :)

  - Uses Request, FormRequest
  - JsonFinder package https://pypi.org/project/jsonfinder/ This is really cool package. It can parse JS snippet from python code

### How to run

I really love to create virtual environment for each and every projects and supply requirements.txt file for them. This way my system is always fresh and clean.

```sh
# Create a virtual environment for this scraper
$ virtualenv projectenv
# Activate the scraper's virtual environment
$ source projectenv/bin/activate
$ cd moviescraper
# Then install all dependencies using 
# requirements.txt file included with the project
$ pip install -r requirements.txt
# Run and get output csv file
$ scrapy crawl gomo -o items.csv -t csv
```

Please try this out and let me know.
### Thank You!!

