document.addEventListener('DOMContentLoaded', () => {
    const playerInfo = fetch('/api/player-info?screen_name=player_name')  // Replace 'player_name' with the actual player name
        .then(response => response.json())
        .then(playerInfo => {
            const startBanner = document.getElementById('start-banner');
            const playBanner = document.getElementById('play-banner');

            if (playerInfo.type === 0 && !playerInfo.location) {
                startBanner.style.display = 'table';
                playBanner.style.display = 'none';
            } else {
                startBanner.style.display = 'none';
                playBanner.style.display = 'table';
            }
        });
});