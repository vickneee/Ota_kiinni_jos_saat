'use strict';

import {
  fetchRound,
  playbanner,
  showPlayerInfo,
} from './bannerscript.js';

import {
  createCriminalMarker,
  createEtsijaMarker,
  createEtsija2Marker,
  addMarkersToMap,
  determinePinType,
  getPinElement,
} from './markers.js';

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

  let resumegame = Resume();
  if (resumegame === true) {
    await resumeGame();

  } else {
    let players = playerData();
    if (players[0].is_computer === 1 && !playersSent) {
      await aistart(players);
      await gameRounds();
      playersSent = true;

    } else {
      await startingPoint(markersdata, markers);
      await gameRounds();
    }

    return map;
  }
}

  async function fetchRecommendedAirports(name, round) {
    try {
      const cacheBuster = new Date().getTime(); // Generate a unique timestamp
      const response = await fetch(
          `http://127.0.0.1:3000/api/get-recommended-airports/${name}/${round}?cb=${cacheBuster}`,
      );
      console.log(`Fetching recommended airports for: ${name}`);

      console.log(
          `Request URL: http://127.0.0.1:3000/api/get-recommended-airports/${name}/${round}?cb=${cacheBuster}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(`Response data: ${JSON.stringify(data)}`);

      if (data && data.recommended_airports) {
        console.log(
            `Recommended airports: ${JSON.stringify(
                data.recommended_airports)}`);
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

  async function gamedata() {
    const response = await fetch('http://127.0.0.1:3000/api/getdata');
    const data = await response.json();
    return data;
  }

  async function aistart(players) {
    return new Promise(async (resolve, reject) => {
      try {
        const res = await sendIfComp(players);
        console.log(res);
        criminalMarker = await createCriminalMarker(map,
            res.criminal_coord.latitude, res.criminal_coord.longitude);
        etsijaMarker1 = await createEtsijaMarker(map,
            res.detective1_location[0].latitude,
            res.detective1_location[0].longitude);
        etsijaMarker2 = await createEtsija2Marker(map,
            res.detective2_location[0].latitude,
            res.detective2_location[0].longitude);
        resolve(res);
      } catch (err) {
        reject(err);
      }
    });
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

            criminalMarker = await createCriminalMarker(map,
                markerData.position.lat, markerData.position.lng);
            etsijaMarker1 = await createEtsijaMarker(map,
                res.detective1_location[0].latitude,
                res.detective1_location[0].longitude);
            etsijaMarker2 = await createEtsija2Marker(map,
                res.detective2_location[0].latitude,
                res.detective2_location[0].longitude);

            markers.forEach(
                (m) => google.maps.event.clearListeners(m, 'click'));
            const gameData = await gamedata();
            const playersgame = gameData.players;
            playbanner();
            await showPlayerInfo(playersgame[0].id, gameData.game_id,
                playersgame[0].screen_name);
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

  function Resume() {
    document.addEventListener('DOMContentLoaded', () => {
      const resume = JSON.parse(localStorage.getItem('continue'));
      return resume;
    });

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
      return json;
    } catch (error) {
      console.error('Error sending players:', error);
    }

  }

  function playerData() {
    const players = JSON.parse(localStorage.getItem('players'));
    return players;
  }

  async function criminalMoves(id) {
    const response = await fetch(`http://127.0.0.1:3000/api/criminal/${id}`);
    const data = await response.json();
    return data.past_location
  }

  async function showCriminalOldLoc(id) {
    return new Promise(async (resolve, reject) => {
      try {
        const data = await criminalMoves(id)
        criminalMarker = removeMarker(criminalMarker);
        criminalMarker = await createCriminalMarker(map, data.latitude,
            data.longitude);
        console.log(data)
        resolve(data)
      } catch (err) {
        console.log(err)
        reject(err)
      }
    })
  }

  async function send_move(player, new_location, ticket_id, is_computer) {
    return new Promise(async (resolve, reject) => {
      try {
        const response = await fetch('http://127.0.0.1:3000/api/play_round', {
          method: 'POST',
          body: JSON.stringify({
            'player': player,
            'new_location': new_location,
            'ticket_id': ticket_id,
            'is_computer': is_computer,
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

  function criminal(players) {
    for (let player of players) {
      if (player.type === 0) {
        return player
      }
    }
  }

  async function moveListener(name, iscomp, round) {
    console.log('move');
    const gameData = await gamedata();
    const players = gameData.players;
    const recommended = await fetchRecommendedAirports(name, round);
    console.log(recommended);
    const {markers, markersdata} = await addMarkersToMap(map, recommended);
    const {event} = await google.maps.importLibrary('core');
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

          const move = await send_move(name, markerData.title, ticketid,
              iscomp);
          console.log(markerData);
          console.log(move);

          // Clear all recommended markers from the map
          markers.forEach((marker) => {
            google.maps.event.clearListeners(marker, 'click');
            marker.setMap(null);
          });

          // Play animation after move
          // await playVideoWithAnimation(); // Ensure animation finishes before proceeding

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

  async function gameover() {
    // Fetch game data
    const gameData = await gamedata();
    // Ensure gamedata() returns the required structure
    console.log('Line 395 Game data:', gameData);
    if (!gameData || !gameData.players) {
      console.error('Invalid game data:', gameData);
      return;
    }

    // const gameid = gameData.game_id;
    const players = gameData.players;

    // Check if the game is over after every move
    for (let j = 0; j < players.length; j++) {
      for (let k = 0; k < j; k++) {
        if (
            (players[k].type === 0 && players[j].type === 1) ||
            (players[k].type === 1 && players[j].type === 0)
        ) {
          if (
              players[k].location.lat === players[j].location.lat &&
              players[k].location.lng === players[j].location.lng
          ) {
            if (players[k].location.lat && players[k].location.lng ===
                players[j].location.lat && players[j].location.lng) {
              console.log(
                  `Criminal ${players[k].screen_name} and Detective ${players[j].screen_name} are at the same location!`
              );
              console.log('Game over!');

              // Update winner message
              const winnerMessage = `Pelaaja ${players[k].screen_name} sai kinnii pelaaja ${players[j].screen_name}!`;

              // Store the message in localStorage
              localStorage.setItem('winnerMessage', winnerMessage);

              // Redirect to gameover.html after a short delay
              setTimeout(() => {
                console.log('Redirecting to gameover.html...');
                window.location.href = '../pages/gameover.html';
              }, 2000);

              // Exit the loops
              return;
            }
          }
        }
      }
    }
  }

  async function gameRounds() {
    console.log('moi');
    const gameData = await gamedata();
    const gameid = gameData.game_id;
    const players = gameData.players;
    const criminalp = criminal(players)
    console.log(players);
    let move;

    for (let i = 1; i < 11; i++) {
      for (let j = 0; j < players.length; j++) {
        if (players[j].is_computer === 0) {
          console.log(players[j].screen_name);
          await showPlayerInfo(players[j].id, gameid, players[j].screen_name,
              j);
          if (players[j].type === 1) {
            const c_coord = await showCriminalOldLoc(criminalp.id)
            console.log(c_coord)
            move = await moveListener(players[j].screen_name,
                players[j].is_computer, i);
            if (j === 1) {
              etsijaMarker1 = removeMarker(etsijaMarker1);
              etsijaMarker1 = await createEtsijaMarker(map, move.position.lat,
                  move.position.lng);
            } else {
              etsijaMarker2 = removeMarker(etsijaMarker2);
              etsijaMarker2 = await createEtsija2Marker(map, move.position.lat,
                  move.position.lng);
            }
          } else {
            if (i >= 2) {
              criminalMarker = removeMarker(criminalMarker);
              criminalMarker = await createCriminalMarker(map,
                  players[j].latitude, players[j].longitude);
              move = await moveListener(players[j].screen_name,
                  players[j].is_computer, i);
              console.log(move);
              console.log('kierros on 2=>')
            } else {
              move = await moveListener(players[j].screen_name,
                  players[j].is_computer, i);
              console.log('kierros1')
            }

          }
          players[j].latitude = move.position.lat
          players[j].longitude = move.position.lng

        } else {
          console.log(players[j].screen_name);
          const aimove = await send_move(players[j].screen_name, 1, 1,
              players[j].is_computer);
          if (j === 0) {
            criminalMarker = removeMarker(criminalMarker);
            criminalMarker = await createCriminalMarker(map, aimove.coords[0],
                aimove.coords[1]);
          } else if (j === 1) {
            etsijaMarker1 = removeMarker(etsijaMarker1);
            etsijaMarker1 = await createEtsijaMarker(map, aimove.coords[0],
                aimove.coords[1]);
          } else {
            etsijaMarker2 = removeMarker(etsijaMarker2);
            etsijaMarker2 = await createEtsija2Marker(map, aimove.coords[0],
                aimove.coords[1]);
          }

          players[j].latitude = aimove.coords[0]
          players[j].longitude = aimove.coords[1]
        }

        // Check if the game is over after every move
        await gameover();

        // // Check if the game is over after every move
        // for (let k = 0; k < j; k++) {
        //   if (
        //       (players[k].type === 0 && players[j].type === 1) ||
        //       (players[k].type === 1 && players[j].type === 0)
        //   ) {
        //     if (
        //         players[k].location.lat === players[j].location.lat &&
        //         players[k].location.lng === players[j].location.lng
        //     ) {
        //       console.log(
        //           `Criminal ${players[k].screen_name} and Detective ${players[j].screen_name} are at the same location!`);
        //       console.log('Game over!');
        //
        //       // Update winner and redirect
        //       const winnerMessage = `Pelaaja ${players[k].screen_name} sai kinnii pelaaja ${players[j].screen_name}!`;
        //
        //       localStorage.getItem('winnerMessage');
        //
        //       // Redirect immediately
        //       localStorage.setItem('winnerMessage',
        //           `Pelaaja ${players[k].screen_name} sai kinnii pelaaja ${players[j].screen_name}!`);
        //       setTimeout(() => {
        //         console.log('Redirecting to gameover.html...');
        //         window.location.href = '../pages/gameover.html';
        //       }, 2000);
        //
        //       return; // Stop further execution as the game is over
        //     }
        //   }
        // }
      }
    }
  }

//moi
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

    playbanner();

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
    try {
      playbanner();

      const gameData = await gamedata(); // Fetch game data
      const gameid = gameData.game_id;
      const players = gameData.players;
      let round = await fetchRound(gameid);

      // Fetch the current player ID whose turn it is
      let currentPlayerId = await fetchCurrentTurn(gameid);

      // Determine the current player's type (criminal or detective)
      const currentPlayer = players.find(
          player => player.id === currentPlayerId);
      if (!currentPlayer) {
        console.error("Error: Current player not found in players list.");
        return;
      }
      console.log(
          `Starting with player ${currentPlayer.screen_name}, type: ${currentPlayer.type}.`);

      // Initialize markers based on the current player's type
      if (currentPlayer.type === 0) {
        console.log("Initializing markers for all players (Criminal's turn).");
        for (let i = 0; i < players.length; i++) {
          const player = players[i];
          if (player.type === 0) {
            criminalMarker = await createCriminalMarker(map,
                player.location.lat, player.location.lng);
            console.log(
                `Criminal marker initialized at (${player.location.lat}, ${player.location.lng}).`);
          } else if (i === 1) {
            etsijaMarker1 = await createEtsijaMarker(map, player.location.lat,
                player.location.lng);
            console.log(
                `Detective 1 marker initialized at (${player.location.lat}, ${player.location.lng}).`);
          } else if (i === 2) {
            etsijaMarker2 = await createEtsija2Marker(map, player.location.lat,
                player.location.lng);
            console.log(
                `Detective 2 marker initialized at (${player.location.lat}, ${player.location.lng}).`);
          }
        }
      } else if (currentPlayer.type === 1) {
        console.log(
            "Initializing markers for detectives only (Detective's turn).");
        for (let i = 0; i < players.length; i++) {
          const player = players[i];
          if (player.type === 1) {
            if (i === 1) {
              etsijaMarker1 = await createEtsijaMarker(map, player.location.lat,
                  player.location.lng);
              console.log(
                  `Detective 1 marker initialized at (${player.location.lat}, ${player.location.lng}).`);
            } else if (i === 2) {
              etsijaMarker2 = await createEtsija2Marker(map,
                  player.location.lat, player.location.lng);
              console.log(
                  `Detective 2 marker initialized at (${player.location.lat}, ${player.location.lng}).`);
            }
          }
        }
      }

      // Find the current player's index
      let currentPlayerIndex = players.findIndex(
          player => player.id === currentPlayerId);
      if (currentPlayerIndex === -1) {
        console.error("Error: Current player ID not found in players list.");
        return;
      }

      console.log(
          `Resuming round ${round} from player ${players[currentPlayerIndex].screen_name}.`);

      // Complete the current round
      while (currentPlayerIndex < players.length) {
        const currentPlayer = players[currentPlayerIndex];

        if (currentPlayer.is_computer === 0) {
          console.log(
              `Processing turn for ${currentPlayer.screen_name} (Human).`);
          await showPlayerInfo(currentPlayer.id, gameid,
              currentPlayer.screen_name);
          const move = await moveListener(currentPlayer.screen_name);
          console.log(
              `Player ${currentPlayer.screen_name} moved to ${move.position.lat}, ${move.position.lng}.`);

          // Update marker and player location
          await updatePlayerMarker(currentPlayer, move, map);
        } else {
          console.log(`Processing turn for ${currentPlayer.screen_name} (AI).`);
          const aiMove = await send_move(currentPlayer.screen_name, 1, 1,
              currentPlayer.is_computer);
          await updatePlayerMarker(currentPlayer,
              {position: {lat: aiMove.coords[0], lng: aiMove.coords[1]}}, map);
        }

        // Check for game-over condition
        for (let k = 0; k < players.length; k++) {
          if (k !== currentPlayerIndex) {
            const otherPlayer = players[k];
            if (
                currentPlayer.location.lat === otherPlayer.location.lat &&
                currentPlayer.location.lng === otherPlayer.location.lng &&
                currentPlayer.type !== otherPlayer.type
            ) {
              console.log(
                  `Game over! ${currentPlayer.screen_name} and ${otherPlayer.screen_name} are at the same location.`);
              await endGame(currentPlayer, otherPlayer);
              return;
            }
          }
        }

        currentPlayerIndex++;
      }
      round = round + 1
      console.log("End of round reached. Proceeding to normal game loop.");

      // Resume normal game loop for remaining rounds
      for (let i = round; i <= 11; i++) {
        console.log(`Starting round ${i}`);
        for (let j = 0; j < players.length; j++) {
          const player = players[j];

          if (player.is_computer === 0) {
            console.log(`Processing turn for ${player.screen_name} (Human).`);
            await showPlayerInfo(player.id, gameid, player.screen_name);
            const move = await moveListener(player.screen_name);
            console.log(
                `Player ${player.screen_name} moved to ${move.position.lat}, ${move.position.lng}.`);
            await updatePlayerMarker(player, move, map);
          } else {
            console.log(`Processing turn for ${player.screen_name} (AI).`);
            const aiMove = await send_move(player.screen_name, 1, 1,
                player.is_computer);
            await updatePlayerMarker(player,
                {position: {lat: aiMove.coords[0], lng: aiMove.coords[1]}},
                map);
          }

          // Check for game-over condition
          for (let k = 0; k < players.length; k++) {
            if (k !== j) {
              const otherPlayer = players[k];
              if (
                  player.location.lat === otherPlayer.location.lat &&
                  player.location.lng === otherPlayer.location.lng &&
                  player.type !== otherPlayer.type
              ) {
                console.log(
                    `Game over! ${player.screen_name} and ${otherPlayer.screen_name} are at the same location.`);
                await endGame(player, otherPlayer);
                return;
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("Error during game resumption:", error);
    }
  }

// Helper function to update markers and locations
  async function updatePlayerMarker(index, move, map) {
    let marker;
    if (index === 0) {
      criminalMarker = removeMarker(criminalMarker);
      criminalMarker = await createCriminalMarker(map, move.position.lat,
          move.position.lng);
    } else if (index === 1) {
      etsijaMarker1 = removeMarker(etsijaMarker1);
      etsijaMarker1 = await createEtsijaMarker(map, move.position.lat,
          move.position.lng);
    } else {
      etsijaMarker2 = removeMarker(etsijaMarker2);
      etsijaMarker2 = await createEtsija2Marker(map, move.position.lat,
          move.position.lng);
    }
  }

// Helper function to handle the game-over logic
  async function endGame(player1, player2) {
    console.log(
        `Game Over! ${player1.screen_name} and ${player2.screen_name} collided.`);
    const winner = document.querySelector("#winner");
    if (winner) {
      winner.innerHTML = `Player ${player1.screen_name} caught Player ${player2.screen_name}!`;
    }
    setTimeout(() => {
      window.location.href = "../pages/gameover.html";
    }, 2000);}


