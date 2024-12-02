document.addEventListener('DOMContentLoaded', () => {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    const startGame = document.getElementById('karkuri');
    const roundElement = document.getElementById('kierrokset')
    const potkurikone = document.getElementById('potkurikone')
    const matkustajakone = document.getElementById('matkustajakone')
    const yksityiskone = document.getElementById('matkustajakone')

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
})