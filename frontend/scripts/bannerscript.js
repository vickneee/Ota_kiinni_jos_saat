function bannerFunc() {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    const startGame = document.getElementById('karkuri');

    const players = playerData();
    const firstPlayer = players ? players[0] : null;

    console.log('Players fetched:', players); // Debugging
    console.log('First player:', firstPlayer); // Debugging

    if (firstPlayer && firstPlayer.type === 0 && firstPlayer.is_computer === 0) {
        displayBanner(firstPlayer);
    } else {
        console.error('No player data available. Ensure localStorage is populated.');
        startBanner.style.display = 'none'

    }
}

document.addEventListener('DOMContentLoaded', () => {
    bannerFunc();
});


function playerData() {
    const players = JSON.parse(localStorage.getItem('players'));
    return players;
}

export function playbanner() {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    playBanner.style.display = 'table';
    startBanner.style.display = 'none'
}


export function displayBanner(firstPlayer) {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    const startGame = document.getElementById('karkuri');
    startGame.textContent = `${firstPlayer.name}`;
    startBanner.style.display = 'table';
    playBanner.style.display = 'none'
//h
}

// Fetch player tickets
export function fetchPlayerTickets(playerId) {
    const potkurikone = document.getElementById('potkurikone');
    const matkustajakone = document.getElementById('matkustajakone');
    const yksityiskone = document.getElementById('yksityiskone');

    fetch(`http://127.0.0.1:3000/api/player-tickets/${playerId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                potkurikone.textContent = `${data.tickets.potkurikone || 0}`;
                matkustajakone.textContent = `${data.tickets.matkustajakone || 0}`;
                yksityiskone.textContent = `${data.tickets.yksityiskone || 0} kpl`;
            } else {
                console.error('Error fetching player tickets:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Fetch round
export function fetchRound(gameId) {
    const roundElement = document.getElementById('kierrokset');

    fetch(`http://127.0.0.1:3000/api/round/${gameId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                roundElement.textContent = `${data.round}`;
            } else {
                console.error('Error fetching round:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Fetch game screen names
export function fetchGameScreenNames(index,screen_name) {
    const playerInfoElement = document.getElementById('pelaaja');
    const playerNameElement = document.getElementById('nimi')
    if(index === 0){
        playerInfoElement.className = 'rikollinen'
        playerInfoElement.textContent = "Rikollinen: "
    }else if (index === 1){
        playerInfoElement.className = 'etsiva1'
        playerInfoElement.textContent = "Etsivä1: "
    }else{
        playerInfoElement.className = 'etsiva2'
        playerInfoElement.textContent = "Etsivä 2: "
    }
    playerNameElement.textContent = screen_name
}

export async function showPlayerInfo(playerId, gameId,screen_name,index){
      await fetchPlayerTickets(playerId);
      await fetchRound(gameId);
      await fetchGameScreenNames(index,screen_name);
}

    /*
    fetch(`http://127.0.0.1:3000/api/game-screen-names/${gameId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const screenNames = data.screen_names.map(name => {
                    const player = data.players.find(p => p.name === name);
                    if (!player) {
                        console.error(`Player with name ${name} not found`);
                        return `Unknown player ${name}`;
                    }
                    return player.type === 0 ? `Rikollisen ${name} vuoro` : `Etsivän ${name} vuoro`;
                });
            } else {
                console.error('Error fetching game screen names:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        */


