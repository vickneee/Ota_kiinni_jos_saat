document.addEventListener('DOMContentLoaded', () => {
    const startBanner = document.getElementById('start-banner');
    const playBanner = document.getElementById('play-banner');
    const players = playerData();
    const firstPlayer = players ? players[0] : null;
    startBanner.textContent = `${firstPlayer.name} choose starting position`;
        if (firstPlayer && firstPlayer.type === 0) {
            startBanner.style.display = 'table';
            playBanner.style.display = 'none';
    } else {
        startBanner.style.display = 'none';
        playBanner.style.display = 'table';
    }
});