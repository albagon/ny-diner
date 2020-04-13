/**
 * Common database helper functions.
 */
const PORT = 5000 // Change this to your server port

class DBHelper {

  /**
   * Database URL.
   * Change this to restaurants.json file location on your server.
   */
  static get DATABASE_URL() {
    return `http://localhost:${PORT}/static/data/restaurants.json`;
  }

  static get DATABASE_URL_FILTERS() {
    return `http://localhost:${PORT}/static/data/filters.json`;
  }

  /**
   * Fetch all restaurants.
   */
  static fetchRestaurants(callback) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', DBHelper.DATABASE_URL);
    xhr.onload = () => {
      if (xhr.status === 200) { // Got a success response from server!
        const json = JSON.parse(xhr.responseText);
        const restaurants = json.restaurants;
        callback(null, restaurants);
      } else { // Oops!. Got an error from server.
        const error = (`Request failed. Returned status of ${xhr.status}`);
        callback(error, null);
      }
    };
    xhr.send();
  }

  /**
   * Fetch restaurants by a cuisine and a borough with error handling.
   */

  static fetchRestaurantByCuisineAndBorough(restaurants, cuisine, borough, callback) {
    if (restaurants.length == 0) {
      callback('No restaurants to display', null);
    } else {
      let results = restaurants
      if (cuisine != 'all') { // filter by cuisine
        results = results.filter(r => r.cuisine == cuisine);
      }
      if (borough != 'all') { // filter by borough
        results = results.filter(r => r.borough == borough);
      }
      callback(null, results);
    }
  }

  /**
   * Fetch list of boroughs and cuisines
   */
  static fetchFilters(callback) {
     // Fetch filters from json file
     let xhr = new XMLHttpRequest();
     xhr.open('GET', DBHelper.DATABASE_URL_FILTERS);
     xhr.onload = () => {
       if (xhr.status === 200) { // Got a success response from server!
         const json = JSON.parse(xhr.responseText);
         const boroughs = json.boroughs;
         const cuisines = json.cuisines;
         callback(null, boroughs, cuisines);
       } else { // Oops!. Got an error from server.
         const error = (`Request failed. Returned status of ${xhr.status}`);
         callback(error, null, null);
       }
     };
     xhr.send();
  }

  /**
   * Restaurant page URL.
   */
  static urlForRestaurant(restaurant) {
    return (`/restaurants/${restaurant.id}`);
  }

  /**
   * Restaurant image URL.
   */
  static imageUrlForRestaurant(restaurant) {
    return (`/static/img/${restaurant.photograph}`);
  }

  /**
   * Map marker for a restaurant.
   */
   static mapMarkerForRestaurant(restaurant, map) {
    // https://leafletjs.com/reference-1.3.0.html#marker
    const marker = new L.marker([restaurant.latlng[0], restaurant.latlng[1]],
      {title: restaurant.name,
      alt: restaurant.name,
      url: DBHelper.urlForRestaurant(restaurant)
      })
      marker.addTo(newMap);
    return marker;
  }
  /* static mapMarkerForRestaurant(restaurant, map) {
    const marker = new google.maps.Marker({
      position: restaurant.latlng,
      title: restaurant.name,
      url: DBHelper.urlForRestaurant(restaurant),
      map: map,
      animation: google.maps.Animation.DROP}
    );
    return marker;
  } */

}
