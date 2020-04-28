let restaurants,
  currentRestaurants,
  boroughs,
  cuisines
var newMap
var markers = []


/**
 * As soon as the page is loaded:
 * 1. Register the service worker
 * 2. Initialize the map
 * 3. Fetch list of Boroughs and Cuisines
 */
document.addEventListener('DOMContentLoaded', (event) => {
  //registerServiceWorker();
  // restaurants variable contains the list of all the restaurants stored
  // in the db.
  self.restaurants = JSON.parse(document.getElementById("map").dataset.restaurants);
  fetchFilters();
  initMap();
});

/**
 * Register a Service Worker to make the site work offline.
 */
registerServiceWorker = () => {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js', {scope: '/'}).then(function() {
      console.log('Registration worked!');
    }).catch(function() {
      console.log('Registration failed!');
    });
  }
}

/**
 * Fetch filters (boroughs and cuisines) and set their HTML.
 */
fetchFilters = () => {
  DBHelper.fetchFilters((error, boroughs, cuisines) => {
    if (error) { // Got an error
      console.error(error);
    } else {
      self.boroughs = boroughs;
      self.cuisines = cuisines;
      fillBoroughsHTML();
      fillCuisinesHTML();
    }
  });
}

/**
 * Set boroughs HTML.
 */
fillBoroughsHTML = (boroughs = self.boroughs) => {
  const select = document.getElementById('boroughs-select');
  boroughs.forEach(borough => {
    const option = document.createElement('option');
    option.innerHTML = borough;
    option.value = borough;
    select.append(option);
  });
}

/**
 * Set cuisines HTML.
 */
fillCuisinesHTML = (cuisines = self.cuisines) => {
  const select = document.getElementById('cuisines-select');
  cuisines.forEach(cuisine => {
    const option = document.createElement('option');
    option.innerHTML = cuisine;
    option.value = cuisine;
    select.append(option);
  });
}

/**
 * Initialize leaflet map, called from HTML.
 */
initMap = () => {
  self.newMap = L.map('map', {
        center: [40.722216, -73.987501],
        zoom: 10,
        scrollWheelZoom: false
      });
  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.jpg70?access_token={mapboxToken}', {
    mapboxToken: 'pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
      '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
  }).addTo(newMap);

  updateRestaurants();
}
/*
 * This is an example on how to use a Google maps Map instead of using Mapbox

  window.initMap = () => {
    let loc = {
      lat: 40.722216,
      lng: -73.987501
    };
    self.map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12,
      center: loc,
      scrollwheel: false
    });
    updateRestaurants();
  }
 */

/**
 * Update page and map for current restaurants.
 */
updateRestaurants = () => {
  const cSelect = document.getElementById('cuisines-select');
  const bSelect = document.getElementById('boroughs-select');

  const cIndex = cSelect.selectedIndex;
  const bIndex = bSelect.selectedIndex;

  const cuisine = cSelect[cIndex].value;
  const borough = bSelect[bIndex].value;

  DBHelper.fetchRestaurantByCuisineAndBorough(self.restaurants, cuisine, borough, (error, currentRestaurants) => {
    if (error) { // Got an error!
      console.error(error);
    } else {
      resetRestaurants(currentRestaurants);
      fillRestaurantsHTML();
    }
  })
}

/**
 * Clear current restaurants, their HTML and remove their map markers.
 */
resetRestaurants = (restaurants) => {
  // Remove all restaurants
  self.currentRestaurants = [];
  const ul = document.getElementById('restaurants-list');
  ul.innerHTML = '';

  // Remove all map markers
  if (self.markers) {
    self.markers.forEach(marker => marker.remove());
  }
  self.markers = [];
  self.currentRestaurants = restaurants;
}

/**
 * Create all restaurants HTML and add them to the webpage.
 */
fillRestaurantsHTML = (restaurants = self.currentRestaurants) => {
  const ul = document.getElementById('restaurants-list');
  ul.setAttribute('aria-label', 'restaurants list');
  restaurants.forEach(restaurant => {
    ul.append(createRestaurantHTML(restaurant));
  });
  addMarkersToMap();
}

/**
 * Create restaurant HTML.
 */
createRestaurantHTML = (restaurant = self.restaurant) => {
  const li = document.createElement('li');
  li.setAttribute('aria-label', restaurant.name);

  const image = document.createElement('img');
  image.className = 'restaurant-img';
  image.src = restaurant.photograph;
  image.alt = 'Image of ' + restaurant.name + ' Restaurant';
  li.append(image);

  const name = document.createElement('h3');
  name.innerHTML = restaurant.name;
  li.append(name);

  const borough = document.createElement('p');
  borough.innerHTML = restaurant.borough;
  li.append(borough);

  const more = document.createElement('button');
  more.setAttribute('aria-label', restaurant.name+' view details');
  more.innerHTML = 'View Details';
  more.onclick = function() {getRestaurantDetails(restaurant.id)};
  li.append(more)

  return li
}

/**
 * Add markers for current restaurants to the map.
 */
addMarkersToMap = (restaurants = self.currentRestaurants) => {
  restaurants.forEach(restaurant => {
    // Add marker to the map
    const marker = DBHelper.mapMarkerForRestaurant(restaurant, self.newMap);
    marker.on("click", onClick);
    function onClick() {
      window.location.href = marker.options.url;
    }
    self.markers.push(marker);
  });

}

/*
 * This is an example on how to add markers to a Google maps Map

addMarkersToMap = (restaurants = self.restaurants) => {
  restaurants.forEach(restaurant => {
    // Add marker to the map
    const marker = DBHelper.mapMarkerForRestaurant(restaurant, self.map);
    google.maps.event.addListener(marker, 'click', () => {
      window.location.href = marker.url
    });
    self.markers.push(marker);
  });
} */

getRestaurantDetails = (id) => {
  jwt = localStorage.getItem("JWTS_LOCAL_KEY");
  alert('Well done number ' + id + '! Now we need to make XMLHttpRequest' + jwt);

  const XHR = new XMLHttpRequest();

  // Define what happens on successful data submission
  XHR.addEventListener("load", function(event) {
    //window.location.href = "/restaurants/" + id.toString();
    alert('Success: ' + event.target.responseText);
  } );

  // Define what happens in case of error
  XHR.addEventListener("error", function(event) {
    alert('Oops! Something went wrong.');
  } );

  // Set up our request
  XHR.open("GET", "/restaurants/" + id.toString());

  // Add Authorization header
  XHR.setRequestHeader("Authorization", "bearer " + jwt);

  // Send the request without data
  XHR.send();
}
