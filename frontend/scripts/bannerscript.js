document.addEventListener('DOMContentLoaded', () => {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    const startGame = document.getElementById('karkuri');
    const roundElement = document.getElementById('kierrokset');
    const potkurikone = document.getElementById('potkurikone');
    const matkustajakone = document.getElementById('matkustajakone');
    const yksityiskone = document.getElementById('yksityiskone');
    const playerInfoElement = document.getElementById('pelaaja');

    // Get player data
    function playerData() {
        const players = JSON.parse(localStorage.getItem('players'));
        return players;
    }

    const players = playerData();
    const firstPlayer = players ? players[0] : null;

    // Test if player is criminal and not computer
    // Then the start banner is displayed
    if (firstPlayer && firstPlayer.type === 0 && firstPlayer.is_computer === 0) {
        startGame.textContent = `${firstPlayer.name}`;

        startBanner.style.display = 'table';
        playBanner.style.display = 'none';
        // Else if criminal is selected to be AI, then skip start banner
        // And show play banner for the etsivä
    } else {
        startBanner.style.display = 'none';
        playBanner.style.display = 'table';
    }

    // Fetch player tickets
    function fetchPlayerTickets(playerId) {
        fetch(`http://127.0.0.1:3000/api/player-tickets/${gameId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    potkurikone.textContent = `Potkurikone: ${data.tickets.potkurikone || 0} kpl`;
                    matkustajakone.textContent = `Matkustajakone: ${data.tickets.matkustajakone || 0} kpl`;
                    yksityiskone.textContent = `Yksityiskone: ${data.tickets.yksityiskone || 0} kpl`;
                } else {
                    console.error('Error fetching player tickets:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Fetch round
    function fetchRound(gameId) {
        fetch(`http://127.0.0.1:3000/api/round/${gameId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    roundElement.textContent = `Round: ${data.round} / 10`;
                } else {
                    console.error('Error fetching round:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

function fetchGameScreenNames(gameId) {
    fetch(`http://127.0.0.1:3000/api/game-screen-names/${gameId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const screenNames = data.screen_names.map(name => {
                    const player = players.find(p => p.name === name);
                    return player.type === 0 ? `Rikollisen ${name} vuoro` : `Etsivän ${name} vuoro`;
                });
                playerInfoElement.textContent = screenNames.join(', ');
            } else {
                console.error('Error fetching game screen names:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

    // Example usage
    if (firstPlayer) {
        fetchPlayerTickets(firstPlayer.id);
        fetchRound(firstPlayer.game_id); // Assuming game_id is available in player data
        fetchGameScreenNames(firstPlayer.game_id); // Assuming game_id is available in player data
    }
});