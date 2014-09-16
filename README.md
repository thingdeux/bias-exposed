# Bias.Exposed #

A web app that will analyze the way news networks separately report top headlines.

<img src="https://raw.github.com/thingdeux/bias-exposed/master/templates/static/screenshots/IndexV0-5.jpg"></img>


* Update: September 1st (Labor Day) - Just about done functionally, need to write user auth. into the custom admin form, continue creating unit tests and finalize the front-end.

* Update: August 24th - Most of the back-end functionality completed, moving to front end and unit tests!

* Update: August 22nd - I've implemented a great deal of the core functionality.  It can spin up celery tasks to crawl RSS feeds, pull the top stories, parse the pages by following custom rules I've set, and compare all of the stories against each other to find like stories (harder than it seemed at the outset).  If a number of news outlets have articles that match a potentialstory is created in the DB and the relevant data from each of the articles is related and passed along for approval. 

#### Tech ####
* Django
* Celery
* Redis
* BeautifulSoup
* feedparser
* nltk (natural language toolkit)

#### nltk language corpus requirements ####
* wordnet
