**Fetch**
=======

Want to grab a bite during an outing with your dog? Fetch helps you choose from 300+ dog-friendly restaurants in 30+ cities. Natural language processing extracts content from reviews in Yelp's Challenge Database regarding restaurants' dog-friendliness and food quality. Then, scores from 0 (negative) to 1 (positive) are computed based on the sentiment for each category. Dynamic visualizations allow users to seamlessly compare individual restaurants, cities, and states. Restaurants are displayed on an interactive map using the Google Maps and Yelp APIs.


## Technologies Used
PostgreSQL, SQLAlchemy, Python, NKLT, TextBlob, Flask, Jinja, Javascript, jQuery, AJAX, Boostrap, D3, HTML5/CSS, Google Maps API, Yelp API

## Features
*Current*
- [x] A list of 300+ dog-friendly restaurants from 30+ cities and their reviews was imported into a PostgreSQL database ([Yelp Challenge Dataset](https://www.yelp.com/dataset_challenge))
- [x] Additional Yelp information is called using [Yelp API](https://www.yelp.com/developers/documentation/v2/overview)
- [x] Naive Bayes Classifier was trained and tested with self-labelled data; achieved accuracy of 75% ([Textblob](http://textblob.readthedocs.org/en/dev/index.html#), a Python wrapper for [Natural Language Toolkit](http://www.nltk.org/) library)
- [x] Each sentence in each review for all restaurants was categorized as describing dog-friendliness or food quality use the Naive Bayes Classifier
- [x] Dog-friendliness and food quality scores were generated using Textblob's sentiment analyzer
- [x] Dog-friendly restaurants are displayed on a map rendered by [Google Maps API](https://developers.google.com/maps/)
- [x] FETCH scores and reviews, retrieved from PostgreSQL database via AJAX call, are displayed on Flask app 
- [x] Flask app and PostgreSQL database deployed and hosted (Digital Ocean, Heroku)

## Author
[Florence Loi](https://www.linkedin.com/in/florenceloi) is a software engineer from San Francisco, CA.