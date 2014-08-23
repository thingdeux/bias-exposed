# Bias.Exposed #

A web app that will analyze the way news networks separately report top headlines.






* Update: August 22nd - I've implemented a great deal of the core functionality.  It can spin up celery tasks to crawl RSS feeds, pull the top stories, parse the pages by following custom rules I've set, and compare all of the stories against each other to find like stories (harder than it seemed at the outset).  If a number of news outlets have articles that match a potentialstory is created in the DB and the relevant data from each of the articles is related and passed along for approval. 

#### Tech ####
* Django
* Celery
* Redis
* BeautifulSoup
* feedparser
* nltk (natural language toolkit)

#### nltk language corpus requirements ####
* stopwords
