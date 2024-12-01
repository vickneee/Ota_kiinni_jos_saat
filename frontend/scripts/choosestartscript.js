document.addEventListener('DOMContentLoaded', () => {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    const startGame = document.getElementById('karkuri');

    function playerData() {
        const players = JSON.parse(localStorage.getItem('players'));
        return players;
    }

    const players = playerData();
    const firstPlayer = players ? players[0] : null;

    if (firstPlayer && firstPlayer.type === 0) {
        startGame.textContent = `${firstPlayer.name}`;
        // startBanner.textContent = `Rikollinen: ${firstPlayer.name} valitse aloituspaikka.`;

        startBanner.style.display = 'table';
        playBanner.style.display = 'none';
    } else {
        startBanner.style.display = 'none';
        playBanner.style.display = 'table';
    }

    // Function to manually set which banner is displayed
    function setBannerDisplay(showStartBanner) {
        if (showStartBanner) {
            startBanner.style.display = 'table';
            playBanner.style.display = 'none';
        } else {
            startBanner.style.display = 'none';
            playBanner.style.display = 'table';
        }
    }

    // For testing. Set value to: true to see the start banner
    // Set value to: false to see the play banner
    setBannerDisplay(true);

});