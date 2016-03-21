**Fetch**
=======
 
Want to grab a bite during an outing with your dog? Fetch helps you choose from 300+ dog-friendly restaurants in 30+ cities. **Natural language processing** extracts content from reviews in **Yelp's Challenge Database** regarding restaurants' dog-friendliness and food quality. Then, scores from 0 (negative) to 1 (positive) are computed based on the **sentiment** for each category. **Dynamic visualizations** allow users to seamlessly compare individual restaurants, cities, and states. Restaurants are displayed on an interactive map using the **Google Maps and Yelp APIs**.

## Table of Contents
* [Technologies Used](#technologies)
* [Data Sources](#data)
* [How to Use Fetch](#how-to-use)

## <a name="technologies"></a>Technologies Used
* **Back-end**: [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/)
* **Front-end**: JavaScript, [jQuery](https://jquery.com/), [AJAX](http://api.jquery.com/jquery.ajax/), [Jinja2](http://jinja.pocoo.org/docs/dev/), [D3.js](https://d3js.org/), [Bootstrap](http://getbootstrap.com/2.3.2/), [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3)
* **Libraries**: [NLTK](http://www.nltk.org/), [TextBlob](https://textblob.readthedocs.org/)
* **Database**: [Flask - SQLAlchemy](http://flask.pocoo.org/), [PostgreSQL](http://www.postgresql.org/)
* **APIs**: [Google Maps](https://developers.google.com/maps/documentation/javascript/), [Yelp](https://www.yelp.com/developers/documentation/v2/overview)

Dependencies are listed in [requirements.txt](requirements.txt).

## <a name="data"></a>Data Sources
The **[Yelp Challenge Dataset](https://www.yelp.com/dataset_challenge)** contains 2.2 million full-length reviews for 77,000 businesses. From this dataset, I was able to extract a list of 300+ dog-friendly restaurants from 30+ cities and their respective reviews (46,000+ total). Then, Yelp API calls were used to gather additional restaurant information.

As a dog-lover who lives in San Francisco, I was disappointed to see that San Francisco was included in Yelp's Challenge Dataset so I hardcoded a list of its dog-friendly restaurants in [restaurants.txt](data/restaurants.txt). As above, Yelp API calls were used to get more restaurant information.

## <a name="how-to-use"></a>How to Use Fetch
#### Homepage
![image of homepage](/static/img/homepage.png)

#### Register for an account
Upon succesful registration, the user is redirected to the homepage.
###### User profile
The user can view all the restaurants he/she has favorited or reviewed on the profile page.
![image of user profile](/static/img/user-profile.png)

#### Browse different dog-friendly restaurants by map

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

#### Browse different dog-friendly restaurants by sentiment analysis
Detailed description coming soon.
![gif of analysis navigation](/static/img/analysis.gif)

## Author
Florence Loi is a software engineer from San Francisco, CA.