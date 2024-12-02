'use strict';

let map;

async function fetchEnv() {
  const response = await fetch('http://127.0.0.1:3000/api/env');
  const env = await response.json();
  return env;
}

async function loadGoogleMapsAPI(apiKey) {

  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initMap`;
    script.async = true;
    script.defer = true;
    script.onerror = () => reject(new Error('Google Maps API failed to load.'));
    window.initMap = () => resolve();
    document.head.appendChild(script);
  });
}

async function fetchJSONData() {
  const response = await fetch('http://localhost:3000/api/airports'); // Replace with the actual path to your JSON file
  const data = await response.json();
  return data;
}

async function initMap() {
  // The location of Center of Europe
  const position = {lat: 54.5260, lng: 15.2551};
  // Request needed libraries.
  //@ts-ignore
  const {Map} = await google.maps.importLibrary('maps');
  const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
  const {PinElement} = await google.maps.importLibrary('marker');
  const {event} = await google.maps.importLibrary('core');
  // The map, centered at Center of Europe
  map = new Map(document.getElementById('map'), {
    zoom: 4,
    center: position,
    mapId: 'DEMO_MAP_ID',
  });

  // Fetch JSON data and add markers
  let selected;
  const data = await fetchJSONData();
  data.locations = data.locations || {};
  const locations = data.locations;
  const pin = new PinElement({
    background: '#ffffff',
  });
  const markers = [];
  for (const [code, coords] of Object.entries(locations)) {
    const pin1 = new PinElement({
      background: '#ffffff',
      glyphColor: '#23245c',
      borderColor: '#C49339',
    });
    const pin2 = new PinElement({
      background: 'green',
      glyphColor: '#C49339',
      borderColor: '#C49339',
    });
    const pin3 = new PinElement({
      background: 'red',
      glyphColor: '#C49339',
      borderColor: '#C49339',
    });
    const pin4 = new PinElement({
      background: 'blue',
      glyphColor: '#C49339',
      borderColor: '#C49339',
    });

    // Add a marker for each location
    const marker = new AdvancedMarkerElement({
      map: map,
      position: {lat: coords[0], lng: coords[1]},
      content: pin1.element,
      title: code,
    });

    // Create a marker for the criminal
    const glyphImg1 = document.createElement('img');
    glyphImg1.src = '../assets/Karkuri.png';
    glyphImg1.style.width = '30px';  // Set the desired width
    glyphImg1.style.height = '30px';  // Set the desired height
    glyphImg1.classList.add('highlighted-image');  // Add a class to the element
    glyphImg1.title = 'Rikollinen';

    const glyphSvgPinElement1 = new PinElement({
      background: '#ffffff',
      glyph: glyphImg1,
      borderColor: '#C49339',
    });

    const glyphSvgMarkerView1 = new AdvancedMarkerElement({
      map,
      position: {lat: 58.5953, lng: 25.01136},
      content: glyphSvgPinElement1.element,
      title: 'Rikollinen',
    });


    // Create a marker for the Etsivä 1
    const glyphImg2 = document.createElement('img');
    glyphImg2.src = '../assets/Etsiva_1.png';
    glyphImg2.style.width = '30px';  // Set the desired width
    glyphImg2.style.height = '30px';  // Set the desired height
    glyphImg2.classList.add('highlighted-image');  // Add a class to the element
    glyphImg2.classList.add('hl-1');  // Add a class to the element
    glyphImg2.title = 'Etsivä 1';

    const glyphSvgPinElement2 = new PinElement({
      background: '#ffffff',
      glyph: glyphImg2,
      borderColor: '#C49339',
    });

    const glyphSvgMarkerView2 = new AdvancedMarkerElement({
      map,
      position: {lat: 56.8796, lng: 24.6032},
      content: glyphSvgPinElement2.element,
      title: 'Etsivä 1',
    });

    // Create a marker for the Etsivä 2
    const glyphImg3 = document.createElement('img');
    glyphImg3.src = '../assets/Etsiva_2.png';
    glyphImg3.style.width = '30px';  // Set the desired width
    glyphImg3.style.height = '30px';  // Set the desired height
    glyphImg3.classList.add('highlighted-image');  // Add a class to the element
    glyphImg3.classList.add('hl-2');  // Add a class to the element
    glyphImg3.title = 'Etsivä 2';

    const glyphSvgPinElement3 = new PinElement({
      background: '#ffffff',
      glyph: glyphImg3,
      borderColor: '#C49339',
    });

    const glyphSvgMarkerView3 = new AdvancedMarkerElement({
      map,
      position: {lat: 55.16994, lng: 23.8813},
      content: glyphSvgPinElement3.element,
      title: 'Etsivä 2',
    });



    markers.push(marker);
    google.maps.event.addListener(marker, 'click', async () => {
      let coordinates = {
        'latitude': marker.position.lat,
        'longitude': marker.position.lng,
      };
      let selected = marker.title;
      let players = playerData();
      console.log('Sending data:', {players, coordinates, selected});
      await sendPlayers(players, coordinates, selected);
      markers.forEach((m) => google.maps.event.clearListeners(m, 'click'));

    });

  }

}

fetchEnv().then(env => {
  const mapKey = env.MAP_KEY;
  loadGoogleMapsAPI(mapKey).then(() => {
    initMap();
  }).catch(error => {
    console.error(error);
  });
});

async function sendPlayers(players, coord, icao) {
  try {
    const response = await fetch('http://127.0.0.1:3000/api/start_game', {
      method: 'POST',
      body: JSON.stringify({
        'players': players,
        'criminal_location': coord,
        'criminal_icao': icao,
      }),
      headers: {
        'Content-type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const json = await response.json();
    console.log(json);
  } catch (error) {
    console.error('Error sending players:', error);
  }

}

function playerData() {
  //document.addEventListener('DOMContentLoaded', async () => {
  const players = JSON.parse(localStorage.getItem('players'));
  return players;
  //if (players) {
  //  await sendPlayers(players);
  //  localStorage.removeItem('players'); // Clear the stored data
  //}
  //});
}

document.getElementById('menu').addEventListener('change', function() {
  const value = this.value;
  if (value) {
    window.location.href = value;
  }
});
