'use strict';

import {
  fetchPlayerTickets,
  fetchRound,
  fetchGameScreenNames,
  playbanner,
  showPlayerInfo
} from './bannerscript.js';
let criminalMarker, etsijaMarker1, etsijaMarker2;
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
let playersSent = false;
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
  const markersdata = [];
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
    markersdata.push({'position': marker.position, 'title': marker.title});
    /*
    let players = playerData();
    let playersSent = false;
    if (players[0].is_computer === 1 && !playersSent) {
      await sendIfComp(players);
      playersSent = true
    } else {
      await startingPoint(marker, markers);
    }*/
    await Promise.all(markers.map(marker => marker));

    //await game(markers[0],markers)

  }
  console.log(markersdata[0].position.lat);
  let players = playerData();

  if (players[0].is_computer === 1 && !playersSent) {
    await aistart(players)
    playersSent = true;
    await gameRounds()
  } else {
    await startingPoint(markersdata, markers);
    await gameRounds();
  }






  return map;
}

async function fetchRecommendedAirports(name) {
  try {
    const cacheBuster = new Date().getTime(); // Generate a unique timestamp
    const response = await fetch(
        `http://127.0.0.1:3000/api/get-recommended-airports/${name}?cb=${cacheBuster}`,
    );
    console.log(`Fetching recommended airports for: ${name}`);
    console.log(`Request URL: http://127.0.0.1:3000/api/get-recommended-airports/${name}?cb=${cacheBuster}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log(`Response data: ${JSON.stringify(data)}`);

    if (data && data.recommended_airports) {
      console.log(`Recommended airports: ${JSON.stringify(data.recommended_airports)}`);
      return data.recommended_airports;
    } else {
      console.warn('No recommended airports found in the response.');
      return [];
    }
  } catch (error) {
    console.error('Error fetching recommended airports:', error);
    return [];
  }
}

/*
async function fetchRecommendedAirports(name) {
  try {
    const response = await fetch(
        `http://127.0.0.1:3000/api/get-recommended-airports/${name}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data)
    console.log(name)
    return data.recommended_airports;

  } catch (error) {
    console.error('Error fetching recommended airports:', error);
    return [];
  }
}


 */
function addMarkersToMap(recommendedAirports) {
  return new Promise(async (resolve, reject) => {
    try {
      let markers = [];
      let markersdata = [];
      // fetch the player tickets
      const players = playerData();
      console.log(players);


      for (const airport of Object.values(recommendedAirports)) {
        const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
        const {PinElement} = await google.maps.importLibrary('marker');

        const pinType = determinePinType(airport.ticket_type);

        const pinElement = new PinElement({
          background: pinType, // Customize the pin color as needed
          glyphColor: airport.ticket_type === 'unknown' ? '#23245c' : '#C49339',
          borderColor: '#C49339',
        });

        const marker = new AdvancedMarkerElement({
          map: map,
          position: {lat: airport.latitude, lng: airport.longitude},
          content: pinElement.element,
          title: airport.icao,
        });

        marker.pinType = pinType;
        markers.push(marker);
        markersdata.push({'position': marker.position, 'title': marker.title});
      }
      console.log(markersdata);
      resolve({markers, markersdata});
    } catch (error) {
      reject(error);
    }
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

async function gamedata() {
  const response = await fetch('http://127.0.0.1:3000/api/getdata');
  const data = await response.json();
  return data;
}

async function aistart(players){
  return new Promise(async (resolve, reject) => {
    try {
      const res = await sendIfComp(players)
      console.log(res)
      criminalMarker = await createCriminalMarker(map, res.criminal_coord.latitude, res.criminal_coord.longitude);
      etsijaMarker1 = await createEtsijaMarker(map, res.detective1_location[0].latitude, res.detective1_location[0].longitude);
      etsijaMarker2 = await createEtsija2Marker(map, res.detective2_location[0].latitude, res.detective2_location[0].longitude);
    } catch (err) {
      reject(err)
    }
  })
}

async function startingPoint(markersdata, markers) {
  console.log(markersdata[0]);
  const {event} = await google.maps.importLibrary('core');
  return new Promise((resolve, reject) => {
    markers.forEach((marker, index) => {
      const markerData = markersdata[index];
      google.maps.event.addListener(marker, 'click', async () => {
        try {
          let coordinates = {
            'latitude': markerData.position.lat,
            'longitude': markerData.position.lng,
          };
          let selected = markerData.title;
          let players = playerData();
          console.log('Sending data:', {players, coordinates, selected});
          const res = await sendPlayers(players, coordinates, selected);
          console.log(res.detective1_location[0].latitude);

          criminalMarker = await createCriminalMarker(map, markerData.position.lat, markerData.position.lng);
          etsijaMarker1 = await createEtsijaMarker(map, res.detective1_location[0].latitude, res.detective1_location[0].longitude);
          etsijaMarker2 = await createEtsija2Marker(map, res.detective2_location[0].latitude, res.detective2_location[0].longitude);

          markers.forEach((m) => google.maps.event.clearListeners(m, 'click'));
          const gameData = await gamedata();
          const playersgame = gameData.players;
          playbanner();
          await showPlayerInfo(playersgame[0].id, gameData.game_id, playersgame[0].screen_name);
          resolve(gameData);
        } catch (error) {
          reject(error);
        }
      });
    });
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
  return resumeData();
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
    return json
  } catch (error) {
    console.error('Error sending players:', error);
  }

}

function playerData() {
  const players = JSON.parse(localStorage.getItem('players'));
  return players;
}

async function send_move(player, new_location, ticket_id,is_computer) {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await fetch('http://127.0.0.1:3000/api/play_round', {
        method: 'POST',
        body: JSON.stringify({
          'player': player,
          'new_location': new_location,
          'ticket_id': ticket_id,
          'is_computer':is_computer
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
      resolve(json); // Resolve the promise with the response data
    } catch (error) {
      console.error('Error sending players:', error);
      reject(error); // Reject the promise with the error
    }
  });
}
/*
async function moveListener(name,round,type){
  console.log('move')
  const recommended = await fetchRecommendedAirports(name)
  console.log(recommended)
  const {markers,markersdata} = await addMarkersToMap(recommended)
  const mdata = markersdata
  const {event} = await google.maps.importLibrary('core');
  let ticketid;
  let chosen = []
  console.log(markersdata[0])

  markers.forEach((marker,index) => {
    const markerData = markersdata[index];
    google.maps.event.addListener(marker, 'click', async () => {
      if (marker.pinType === 'red') {
        ticketid = 1
      } else if (marker.pinType === 'blue') {
        ticketid = 2
      } else {
        ticketid = 3
      }

      //await send_move(name, marker.icao, ticketid)
      chosen = markerData
      console.log(markerData)
      markers.forEach((m) => google.maps.event.clearListeners(m, 'click'));
      return markerData
    })
  })


  //return chosen

}
*/

async function moveListener(name,iscomp) {
  console.log('move');
  const gameData = await gamedata();
  const players = gameData.players;
  const recommended = await fetchRecommendedAirports(name);
  console.log(recommended);
  const { markers, markersdata } = await addMarkersToMap(recommended);
  const { event } = await google.maps.importLibrary('core');
  let ticketid;

  return new Promise((resolve, reject) => {
    if (markersdata.length === 0) {
      reject(new Error('No markers data available'));
      return;
    }

    console.log(markersdata[0]);

    markers.forEach((marker, index) => {
      const markerData = markersdata[index];
      google.maps.event.addListener(marker, 'click', async () => {
        if (marker.pinType === 'red') {
          ticketid = 1;
        } else if (marker.pinType === 'blue') {
          ticketid = 2;
        } else {
          ticketid = 3;
        }

        const move = await send_move(name, markerData.title, ticketid,iscomp);
        console.log(markerData);
        console.log(move);

        // Clear all recommended markers from the map
        markers.forEach((marker) => {
          google.maps.event.clearListeners(marker, 'click');
          marker.setMap(null);
        });

        // markers.forEach((m) => google.maps.event.clearListeners(m, 'click'));
        resolve(markerData); // Resolve with the clicked marker data
      });
    });
  });
}

// Add other function calls here that need to be executed in the loop
//
// Function to remove a marker from the map and return null
function removeMarker(marker) {
  if (marker) {
    marker.setMap(null); // Remove the marker from the map
    marker = null; // Clear the reference
  }
  return marker; // Return the cleared marker reference
}
/*
function isGameOver(players) {
  const criminal = players.find(player => player.type === 0);
  const detectives = players.filter(player => player.type === 1);

  if (!criminal) return false;

  console.log('Criminal Location:', criminal.location);
  console.log('Detective Location:', detectives.location);

  return detectives.some(detective => detective.location === criminal.location && detective.location.lng === criminal.location.lng);
}
*/
async function gameRounds() {

  const gameData = await gamedata();
  const gameid = gameData.game_id;
  const players = gameData.players;
  console.log(players);

  for (let i = 1; i < 11; i++) {
    for (let j = 0; j < players.length; j++) {
      if (players[j].is_computer === 0) {
        console.log(players[j].screen_name);
        await showPlayerInfo(players[j].id, gameid, players[j].screen_name);
        const move = await moveListener(players[j].screen_name,players[j].is_computer);
        console.log(move);

        if (j === 0) {
          criminalMarker = removeMarker(criminalMarker);
          criminalMarker = await createCriminalMarker(map, move.position.lat,
              move.position.lng);
        } else if (j === 1) {
          etsijaMarker1 = removeMarker(etsijaMarker1);
          etsijaMarker1 = await createEtsijaMarker(map, move.position.lat,
              move.position.lng);
        } else {
          etsijaMarker2 = removeMarker(etsijaMarker2);
          etsijaMarker2 = await createEtsija2Marker(map, move.position.lat,
              move.position.lng);
        }
          console.log(`Round ${i}, Player ${j}:`, players[j].location);
          // Update the player's location in the data
          players[j].location = {
          lat: move.position.lat,
          lng: move.position.lng,
          };

        // Check if the game is over after every move
        /*
        if (isGameOver(players)) {
          console.log('Game Over');
          return; // Exit the function as the game is over
        }*/

      } else {
        console.log(players[j].screen_name)
          const aimove = await send_move(players[j].screen_name, 1, 1,players[j].is_computer);
          if(j === 0){
            criminalMarker = removeMarker(criminalMarker);
            criminalMarker = await createCriminalMarker(map, aimove.coords[0],aimove.coords[1]);
          }
          else if (j === 1){
            etsijaMarker1 = removeMarker(etsijaMarker1);
            etsijaMarker1 = await createEtsijaMarker(map, aimove.coords[0],aimove.coords[1]);
          }
          else{
            etsijaMarker2 = removeMarker(etsijaMarker2);
            etsijaMarker2 = await createEtsija2Marker(map, aimove.coords[0],aimove.coords[1]);
          }

          players[j].location = {
          lat: aimove.coords[0],
          lng: aimove.coords[1],
          };
        }

      }
  }
}

// Get the players id that's turn it is
async function fetchCurrentTurn(game_id) {
  const response = await fetch(
      `http://127.0.0.1:3000/api/current-turn/${game_id}`);
  const data = await response.json();
  return data.current_player_id;
}

// Loop when continue game is selected
async function continueGameLoop() {
  const gameData = JSON.parse(localStorage.getItem('gameData'));


    playbanner()


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

async function resumeGame() {

  const gameData = await gamedata()
  const gameid = gameData.game_id
  const players = gameData.players
  const round = await fetchRound(gameid);
  const turn = await fetchCurrentTurn(gameid);
  /* etsi kenen vuoro listassa missä kohtaa.
  kierros pitää pelataloppuun ja lisätä yksi kierros. sitten jatkuu normaalisti <3
   */


  for (let i = round; i < 11; i++) {
    for (let j = 0; j < players.length; j++) {
      if (players[j].is_computer === 0) {
        await showPlayerInfo(players[j].id, gameid, players[j].screen_name);
        const move = await moveListener(players[j].screen_name)
        console.log(move)
      }
    }
  }
}