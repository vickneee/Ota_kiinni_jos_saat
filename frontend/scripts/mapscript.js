'use strict';

import {
  fetchPlayerTickets,
  fetchRound,
  fetchGameScreenNames,
  playbanner,
  showPlayerInfo
} from './bannerscript.js';

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

// Create and add the criminal marker
async function createCriminalMarker(map, lat, lng) {
  try {
    const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
    const {PinElement} = await google.maps.importLibrary('marker');

    if (!PinElement) {
      throw new Error('PinElement is not available.');
    }

    const glyphImg1 = document.createElement('img');
    glyphImg1.src = '../assets/Karkuri.png';
    glyphImg1.style.width = '30px';
    glyphImg1.style.height = '30px';
    glyphImg1.classList.add('highlighted-image');
    glyphImg1.title = 'Rikollinen';

    const glyphSvgPinElement1 = new PinElement({
      background: '#ffffff',
      glyph: glyphImg1,
      borderColor: '#C49339',
    });

    const glyphMarkerView1 = new AdvancedMarkerElement({
      map,
      position: {lat: lat, lng: lng},
      content: glyphSvgPinElement1.element,
      title: 'Rikollinen',
    });

    return glyphMarkerView1;
  } catch (error) {
    // console.error('Error creating criminal marker:', error);
  }
}

// Create and add the etsiva 1 marker
async function createEtsijaMarker(map, lat, lng) {
  try {
    const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
    const {PinElement} = await google.maps.importLibrary('marker');
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

    const glyphMarkerView2 = new AdvancedMarkerElement({
      map,
      position: {lat: lat, lng: lng},
      content: glyphSvgPinElement2.element,
      title: 'Etsivä 1',
    });
    return glyphMarkerView2;
  } catch (error) {
    // console.error('Error creating etsiva 2 marker:', error);
  }
}

// Create and add the etsiva 2 marker
async function createEtsija2Marker(map, lat, lng) {
  try {

    const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
    const {PinElement} = await google.maps.importLibrary('marker');
    const glyphImg2 = document.createElement('img');
    glyphImg2.src = '../assets/Etsiva_2.png';
    glyphImg2.style.width = '30px';  // Set the desired width
    glyphImg2.style.height = '30px';  // Set the desired height
    glyphImg2.classList.add('highlighted-image');  // Add a class to the element
    glyphImg2.classList.add('hl-2');  // Add a class to the element
    glyphImg2.title = 'Etsivä 2';

    const glyphPinElement3 = new PinElement({
      background: '#ffffff',
      glyph: glyphImg2,
      borderColor: '#C49339',
    });

    const glyphMarkerView3 = new AdvancedMarkerElement({
      map,
      position: {lat: lat, lng: lng},
      content: glyphPinElement3.element,
      title: 'Etsivä 2',
    });
    return glyphMarkerView3;
  } catch (error) {
    // console.error('Error creating etsiva 2 marker:', error);
  }
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
    mapTypeId: 'roadmap', // Set the initial map type
    disableDefaultUI: true, // Disable all default UI controls (optional)
    mapTypeControl: false, // Disable the map/satellite switcher
    streetViewControl: false, // Disable the Street View Pegman
    fullscreenControl: false, // Disable fullscreen control
    zoomControl: true, // Enable zoom control (optional)
  });

  // Fetch JSON data and add markers
  const data = await fetchJSONData();
  data.locations = data.locations || {};
  const locations = data.locations;

  const markers = [];

  for (const [ticketType, coords] of Object.entries(locations)) {
    const pinType = determinePinType(ticketType);// Determine the pin type based on the ticket type
    const pinElement = getPinElement(PinElement, pinType);

    const marker = new AdvancedMarkerElement({
      map: map,
      position: {lat: coords[0], lng: coords[1]},
      content: pinElement.element,
      title: ticketType,
    });
    markers.push(marker);
    let players = playerData();
    if (players[0].is_computer === 1) {
      await sendIfComp(players);
    } else {
      await startingPoint(marker, markers);
    }
  }

  // Add a hardcoded marker to test addMarkersToMap
  const hardcodedAirports = [
    {
      latitude: 42.7128,
      longitude: 34.0060,
      name: 'Test Airport Potkurikone',
      ticketType: 'potkurikone',
    },
    {
      latitude: 34.0522,
      longitude: 18.2437,
      name: 'Test Airport Matkustajakone',
      ticketType: 'matkustajakone',
    },
    {
      latitude: 60.5074,
      longitude: -0.1278,
      name: 'Test Airport Yksityiskone',
      ticketType: 'yksityiskone',
    },
    {
      latitude: 55.8566,
      longitude: 20.3522,
      name: 'Test Airport Default Unknown',
      ticketType: 'unknown',
    },
  ];

  const gameData = await gamedata(); // Fetch game data here
  //const playerId = gameData.players[0].id;
  //console.log(`Player id in line 187 ${playerId}`);
  //const recommendedAirports = await fetchRecommendedAirports(playerId);
  addMarkersToMap(hardcodedAirports);  // Change back to recommendedAirports

  return map;
}

async function fetchRecommendedAirports(playerId) {
  try {
    const response = await fetch(
        `http://127.0.0.1:3000/api/get-recommended-airports/${playerId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.recommended_airports;
  } catch (error) {
    console.error('Error fetching recommended airports:', error);
    return [];
  }
}

function addMarkersToMap(recommendedAirports) {
  recommendedAirports.forEach(async (airport) => {
    const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
    const {PinElement} = await google.maps.importLibrary('marker');

    const pinType = determinePinType(airport.ticketType);

    const pinElement = new PinElement({
      background: pinType, // Customize the pin color as needed
      glyphColor: airport.ticketType === 'unknown' ? '#23245c' : '#C49339',
      borderColor: '#C49339',
    });

    const marker = new AdvancedMarkerElement({
      map: map,
      position: {lat: airport.latitude, lng: airport.longitude},
      content: pinElement.element,
      title: airport.name,
    });
  });
}

function determinePinType(ticketType) {
  // Define your criteria to determine the pin type based on the ticket type
  if (ticketType === 'potkurikone') {
    return 'red';
  } else if (ticketType === 'matkustajakone') {
    return 'blue';
  } else if (ticketType === 'yksityiskone') {
    return 'green';
  } else {
    return 'white';
  }
}

function getPinElement(PinElement, type) {
  switch (type) {
    case 'green':
      return new PinElement({
        background: 'green',
        glyphColor: '#C49339',
        borderColor: '#C49339',
      });
    case 'red':
      return new PinElement({
        background: 'red',
        glyphColor: '#C49339',
        borderColor: '#C49339',
      });
    case 'blue':
      return new PinElement({
        background: 'blue',
        glyphColor: '#C49339',
        borderColor: '#C49339',
      });
    case 'white':
      return new PinElement({
        background: '#ffffff',
        glyphColor: '#23245c',
        borderColor: '#C49339',
      });
    default:
      return new PinElement({
        background: '#ffffff',
        glyphColor: '#23245c',
        borderColor: '#C49339',
      });
  }
}

async function startingPoint(marker, markers) {
  const {event} = await google.maps.importLibrary('core');
  google.maps.event.addListener(marker, 'click', async () => {
    let coordinates = {
      'latitude': marker.position.lat,
      'longitude': marker.position.lng,
    };
    let selected = marker.title;
    let players = playerData();
    console.log('Sending data:', {players, coordinates, selected});
    const res = await sendPlayers(players, coordinates, selected);
    console.log(res.detective1_location[0].latitude);

    await createCriminalMarker(map, marker.position.lat, marker.position.lng);
    await createEtsijaMarker(map, res.detective1_location[0].latitude,
        res.detective1_location[0].longitude);
    await createEtsija2Marker(map, res.detective2_location[0].latitude,
        res.detective2_location[0].longitude);

    markers.forEach((m) => google.maps.event.clearListeners(m, 'click'));
    await gameRounds();

  });
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
    return json;
  } catch (error) {
    console.error('Error sending players:', error);
  }

}

function resumeData() {
  document.addEventListener('DOMContentLoaded', () => {
    const gameData = JSON.parse(localStorage.getItem('gameData'));

    if (gameData) {
      console.log('Game Data:', gameData);
      // Use the game data to initialize the map or players
      // For example:
      // initializeMap(gameData);
    } else {
      console.error('No game data found in localStorage');
    }
  });
  return resumeData()
}

async function sendIfComp(players) {
  try {
    const response = await fetch('http://127.0.0.1:3000/api/start_game_ai', {
      method: 'POST',
      body: JSON.stringify({
        'players': players,
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
    const players = JSON.parse(localStorage.getItem('players'));
    return players;
}

async function gamedata() {
  const response = await fetch('http://127.0.0.1:3000/api/getdata');
  const data = await response.json();
  return data;
}

async function gameRounds() {

  playbanner();

  for (let i = 1; i < 11; i++) {
    const gameData = await gamedata();
    const players = gameData.players
    for (let i = 0; i < 2; i++) {
      if(players[i].type === 1){
        await showPlayerInfo(players[i].id, gameData.game_id, players[i].screen_name)

      }
    }
    }
  //await fetchPlayerTickets(gameData.players[0].id);
  //await fetchRound(gameData.game_id);
  //await fetchGameScreenNames(gameData.players[0].screen_name);
  console.log(`Player id ${gameData.players[0].id}`);
  console.log(`Game id ${gameData.game_id}`);
  console.log(`Player screen name ${gameData.players[0].screen_name}`);
}


// Get the players id thats turn it is
async function fetchCurrentTurn(game_id) {
  const response = await fetch(`http://127.0.0.1:3000/api/current-turn/${game_id}`);
  const data = await response.json();
  return data.current_player_id;
}

// Loop when continue game is selected
async function continueGameLoop() {
  const gameData = JSON.parse(localStorage.getItem('gameData'));



  playbanner()



}


async function send_move(player, new_location, ticket_id) {
  try {
    const response = await fetch('http://127.0.0.1:3000/api/play_round', {
      method: 'POST',
      body: JSON.stringify({
        'player': player,
        'new_location': new_location,
        'ticket_id': ticket_id,
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

async function game_rounds(map, players) {
  const p_list = [];
  for (let p of players) {
    p_list.push(p);
  }
  console.log(p_list);
}

// To test gamedata

/* // Call the animation function
        await playVideoWithAnimation();
*/
async function playVideoWithAnimation() {
  const videoContainer = document.getElementById('video-container');
  const video = document.getElementById('animation-video');

  // Show and animate the video container (rising up)
  videoContainer.style.display = 'block';
  videoContainer.classList.add('active'); // Add rising animation
  video.play();

  // Wait for the video to finish
  await new Promise((resolve) => {
    video.onended = () => {
      // Add the exit animation
      videoContainer.classList.remove('active');
      videoContainer.classList.add('exit'); // Start falling animation

      // Wait for the animation to complete
      setTimeout(() => {
        videoContainer.classList.remove('exit'); // Clean up the exit class
        videoContainer.style.display = 'none'; // Hide the video
        resolve(); // Resolve the promise after animation
      }, 1500); // Match this duration to the CSS transition time (1.5s)
    };
  });
}
