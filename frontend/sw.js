/* global self caches fetch */

let initialRequests = [
  '/',
  'https://unpkg.com/leaflet@1.3.1/dist/leaflet.css',
  'https://api.mapbox.com/mapbox-gl-js/v0.46.0/mapbox-gl.css',
  'css/styles.css',
  'https://unpkg.com/leaflet@1.3.1/dist/leaflet.js',
  'js/dbhelper.js',
  'js/main.js',
  'data/restaurants.json',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1205/1539.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1206/1539.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1205/1540.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1206/1540.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1207/1539.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1204/1539.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1203/1540.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1203/1539.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1204/1540.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1208/1540.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1207/1540.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://api.tiles.mapbox.com/v4/mapbox.streets/12/1208/1539.jpg70?access_token=pk.eyJ1IjoiYWxiYWdvbiIsImEiOiJjaml0N3g3NWMxeWtwM3dtcGF5anVhdmpqIn0.BdEnkNzS4lcOAzndfsaU3Q',
  'https://unpkg.com/leaflet@1.3.1/dist/images/marker-icon.png',
  'img/1.jpg',
  'img/2.jpg',
  'img/3.jpg',
  'img/4.jpg',
  'img/5.jpg',
  'img/6.jpg',
  'img/7.jpg',
  'img/8.jpg',
  'img/9.jpg',
  'img/10.jpg',
  'https://unpkg.com/leaflet@1.3.1/dist/images/marker-shadow.png'];

self.addEventListener('install', function(event) {
  event.waitUntil(
    // Open a cache named 'restaurant-reviews-v1'
    // Add the initial URLs to the cache
    caches.open('restaurant-reviews-v1').then(function(cache) {
        return cache.addAll(initialRequests);
    }).catch(function(e) {
      console.log('Cache open failed with ' + e);
    })
  );
});

self.addEventListener('fetch', function(event) {
  caches.open('restaurant-reviews-v1').then(function(cache) {
    return cache.add(event.request.url);
  });
  event.respondWith(
    fetch(event.request)
    .catch(function(e) {
      console.error('Fetch failed. Returning offline page instead.', e);
      return caches.open('restaurant-reviews-v1').then(function(cache) {
        return cache.match(event.request);
      });
    })
  );
});

// The claim() method causes pages to be controlled immediately.
// self.addEventListener('activate', function(event) {
//   event.waitUntil(clients.claim());
// });

// This is to delete cache before the sw gets activated
// self.addEventListener('activate', function(event) {
//   event.waitUntil(
//     caches.delete('old-cache')
//   );
// });
