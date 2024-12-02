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
  const {PinElement} =  await google.maps.importLibrary("marker");
  const {event} = await google.maps.importLibrary("core");
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

  const markers = []
  for (const [code, coords] of Object.entries(locations)) {
    const pin = new PinElement({
      background:'#ffffff',
      glyphColor:'#23245c',
      borderColor:'#C49339'
    });
    const marker = new AdvancedMarkerElement({
      map: map,
      position: { lat: coords[0], lng: coords[1] },
      content:pin.element,
      title: code,
    });
    markers.push(marker)
    await startingPoint(marker,markers)


  }
  return map

}

async function startingPoint(marker,markers){
  const {event} = await google.maps.importLibrary("core");
  google.maps.event.addListener(marker, 'click', async () => {
      let coordinates = { 'latitude': marker.position.lat, 'longitude': marker.position.lng };
      let selected = marker.title;
      let players = playerData();
      console.log('Sending data:', { players, coordinates, selected });
      await sendPlayers(players, coordinates, selected);
      markers.forEach((m)=>google.maps.event.clearListeners(m, 'click'));

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


async function sendPlayers(players,coord, icao) {
    try {
    const response = await fetch('http://127.0.0.1:3000/api/start_game', {
      method: "POST",
      body: JSON.stringify({
        'players': players,
        'criminal_location': coord,
        'criminal_icao': icao,
      }),
      headers: {
        "Content-type": "application/json",
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

function playerData(){

  const players = JSON.parse(localStorage.getItem('players'));
  return players

}

async function gameRounds(map,players){
  let round = 1
  const p_list = []
  for(let p of players){
    p_list.push(p.name)
  }
  for(let i = 1; i < 11; i++){
    for(let i = 0; i<2; i++){
      await send_move(player,new_location,ticket_id)
    }
  }
}

async function send_move(player,new_location,ticket_id){
  try {
    const response = await fetch('http://127.0.0.1:3000/api/play_round', {
      method: "POST",
      body: JSON.stringify({
        'player': player,
        'new_location': new_location,
        'ticket_id': ticket_id,
      }),
      headers: {
        "Content-type": "application/json",
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


async function game_rounds(map,players){
  const p_list = []
  for (let p of players){
    p_list.push(p)
  }
  console.log(p_list)
}

document.getElementById('menu').addEventListener('change', function() {
  const value = this.value;
  if (value) {
    window.location.href = value;
  }
});
