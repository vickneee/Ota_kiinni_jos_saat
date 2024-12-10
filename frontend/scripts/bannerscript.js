// Banner script for displaying the start banner and play banner
function bannerFunc() {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    const startGame = document.getElementById('karkuri');

    const players = playerData();
    const firstPlayer = players ? players[0] : null;

    const continueG = Resume()

    if (firstPlayer && firstPlayer.type === 0 && firstPlayer.is_computer === 0 && continueG === 'false') {
        displayBanner(firstPlayer);
    } else {
        console.error('No player data available. Ensure localStorage is populated.');
        startBanner.style.display = 'none'
    }
}

// Run the banner script when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    bannerFunc();
});

// Fetch player data from localStorage
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

// Fetch resume data from localStorage
function Resume() {
  const resume = localStorage.getItem('resume');
  return resume;
}

// Display the start banner
export function displayBanner(firstPlayer) {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    const startGame = document.getElementById('karkuri');
    startGame.textContent = `${firstPlayer.name}`;
    startBanner.style.display = 'table';
    playBanner.style.display = 'none'
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

// Fetch continue round
export async function fetchContinueRound(gameId) {
    const response = await fetch(`http://127.0.0.1:3000/api/round/${gameId}`);
    const data = await response.json()
    return data.round
}

// Fetch round
export function fetchRound(gameId, ticket_type) {
    const roundElement = document.getElementById('kierrokset');
    const ticket = document.getElementById('ticket-type')

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
    if(ticket_type){
        if(ticket_type === 'potkurikone'){
            ticket.className = 'color-red'
        }
        else if(ticket_type === 'matkustajakone'){
            ticket.className = 'color-blue'
        }else{
            ticket.className = 'color-green'
        }
        ticket.textContent = `${ticket_type}`
    }
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

// Show player info
export async function showPlayerInfo(playerId, gameId,screen_name,index,ticket_type){
      await fetchPlayerTickets(playerId);
      await fetchRound(gameId,ticket_type);
      await fetchGameScreenNames(index,screen_name);
}