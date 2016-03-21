**Fetch**
=======
 
Want to grab a bite during an outing with your dog? Fetch helps you choose from 300+ dog-friendly restaurants in 30+ cities. **Natural language processing** extracts content from reviews in **Yelp's Challenge Database** regarding restaurants' dog-friendliness and food quality. Then, scores from 0 (negative) to 5 (positive) are computed based on the **sentiment** for each category. **Dynamic visualizations** allow users to seamlessly compare individual restaurants, cities, and states. Restaurants are displayed on an interactive map using the **Google Maps and Yelp APIs**.

## Table of Contents
* [Technologies Used](#technologies)
* [Data](#data)
    * [Sources](#sources)
    * [Classification](#classification)
    * [Sentiment Analysis](#sentiment-analysis)
* [How to Use Fetch](#how-to-use)
    * [Homepage](#homepage)
    * [Register for an account](#register)
    * [Browse dog-friendly restaurants by map](#browse-by-map)
    * [Browse dog-friendly restaurants by sentiment analysis](#browse-by-sentiment)

## <a name="technologies"></a>Technologies Used
* **Back-end**: [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/)
* **Front-end**: [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [jQuery](https://jquery.com/), [AJAX](http://api.jquery.com/jquery.ajax/), [Jinja2](http://jinja.pocoo.org/docs/dev/), [D3.js](https://d3js.org/), [Bootstrap](http://getbootstrap.com/2.3.2/), [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3)
* **Libraries**: [NLTK](http://www.nltk.org/), [TextBlob](https://textblob.readthedocs.org/)
* **Database**: [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/), [PostgreSQL](http://www.postgresql.org/)
* **APIs**: [Google Maps](https://developers.google.com/maps/documentation/javascript/), [Yelp](https://www.yelp.com/developers/documentation/v2/overview)

Dependencies are listed in [requirements.txt](requirements.txt).

## <a name="data"></a>Data
#### <a name="sources"></a>Sources
The **[Yelp Challenge Dataset](https://www.yelp.com/dataset_challenge)** contains 2.2 million full-length reviews for 77,000 businesses. From this dataset, I was able to extract a list of 300+ dog-friendly restaurants from 30+ cities and their respective reviews (46,000+ total). Then, Yelp API calls were used to gather additional restaurant information.

As a dog-lover who lives in San Francisco, I was disappointed to see that San Francisco was included in Yelp's Challenge Dataset so I hardcoded a list of its dog-friendly restaurants in [restaurants.txt](data/restaurants.txt). As with the Dataset restaurants, Yelp API calls were used to get more information about San Francisco restaurants.

#### <a name="classification"></a>Classification
I generate two different scores for each restaurant to provide information regarding its dog-friendliness and food quality. Because reviews can describe different characteristics, each sentence in a restaurant's reviews is classified as dog-friendliness, food quality, or disregarded as neiher.

This is done using the Naive Bayes Classifier in the Textblob wrapper for the Natural Language Toolkit (NLTK) library. Prior to classifying each sentence, the classifier was trained following the 80:20 rule of thumb split. Based on the test set, the classifier was 75% accurate.

After each sentence is classified as describing dog-friendliness or food quality, a list of each category is generated per restaurant.

#### <a name="sentiment-analysis"></a>Sentiment Analysis
The Textblob wrapper includes a sentiment analyzer that was pre-trained on movie ratings. After two lists of sentences are generated per restaurant, sentiment analysis is performed on each sentence and then an average score for each category is computed for each restaurant.

## <a name="how-to-use"></a>How to Use Fetch
#### <a name="homepage"></a>Homepage
![image of homepage](/static/img/homepage.png)

#### <a name="register"></a>Register for an account
Upon succesful registration, the user is redirected to the homepage.

###### User profile
The user can view all the restaurants he/she has favorited or reviewed on the profile page.

![image of user profile](/static/img/user-profile.png)

#### <a name="browse-by-map"></a>Browse dog-friendly restaurants by map

###### Center on Current Location
If the browser is allowed to access the user's location, the user can center the map on the user's current location.

![gif of centering on current location](/static/img/geolocation.gif)

###### Filter by Category

![gif of category filtering](/static/img/filter-by-category.gif)

###### Select Restaurant
The user can then hover over a marker to see that restaurant's name. If the user clicks on the marker, an AJAX request is sent to the Google Maps API to generate an info window and its data is retrieved from the PostgreSQL database via another AJAX request.

![gif of restaurant selection](/static/img/select-restaurant.gif)

###### Review a Restaurant
Once a restaurant's info window is open, the user can submit a rating and review, which are stored in the PostgreSQL database.

![gif of review form](/static/img/review.gif)

###### Favorite a Restaurant
The user can also favorite or unfavorite a restaurant, which will update the database through an AJAX request.

![gif of (un)favoriting restaurant](/static/img/favorite.gif)

###### Center on City
The user can select a city (separated by state/province) in the dropdown menu. Then AJAX requests are made to **1)** the Google Maps API's Geocoding service to recenter the map on that location and **2)** the PostgreSQL database to populate Fetch's top 5 recommended restaurants in that city based on sentiment analysis scores.

![gif of city selection](/static/img/select-city.gif)

#### <a name="browse-by-sentiment"></a>Browse dog-friendly restaurants by sentiment analysis
On the initial analysis page, the average scores for restaurants in certain US states and Canadian provinces are displayed with a histogram and pie chart using the D3.js library. The user can hover over the restaurant and see which percentage of the total score each category makes up. Alternatively, the user can hover over a pie slice (dog-friendliness or food quality) and see only that individual score in the histogram. 

If the user wants more information, he/she can click on a bar in the histogram to see similar information for the cities in that state/province. Then, the city bar can be clicked to see the scores for restaurants in that city. Clicking on a restaurant will redirect the user to the homepage, where the Google map will automatically recenter on the appropriate restaurant.

![gif of analysis navigation](/static/img/analysis.gif)

## Features in Version 2.0
- [ ] Testing
- [ ] Train Textblob's sentiment analyzer with restaurant reviews instead of movie reviews
- [ ] Train/test enough data to add another category (i.e., service, ambiance, etc)
- [ ] Encrypt passwords in database OR implement OAuth 2.0
- [ ] Make mobile app version
- [ ] Incorporate Twilio API to text user when user is walking near a dog-friendly restaurant

## Author
**Florence Loi** is a software engineer in San Francisco, CA.  She lives with her partner along with their dog Zorro, and two cats.
