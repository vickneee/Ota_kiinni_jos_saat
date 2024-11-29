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
  const {PinElement} = await await google.maps.importLibrary("marker");
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
    background:'#ffffff' ,
  });
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
    marker.addListener('click',()=>{
      selected = marker.title
      let players = playerData()
      console.log(players, selected)
    })

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


async function sendPlayers(players) {
  fetch('http://127.0.0.1:3000/api/start_game',
      {
        method: "POST",
        body: JSON
            .stringify
            ({
              players: players
            }),
        headers: {
          "Content-type": "application/json",
        },
      })
      .then((response) => response.json())
      .then((json) => console.log(json))


}

function playerData(){
  //document.addEventListener('DOMContentLoaded', async () => {
  const players = JSON.parse(localStorage.getItem('players'));
  return players
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
