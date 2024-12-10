import {gamedata} from './mapscript.js';
import {criminal} from './mapscript.js';

// Function to check if the game is over
export async function gameover(round) {
  // Fetch game data
  const gameData = await gamedata();
  console.log('Line 395 Game data:', gameData);

  if (!gameData || !gameData.players) {
    console.error('Invalid game data:', gameData);
    return;
  }

  const players = gameData.players;

  // Get the criminal player
  const criminalPlayer = criminal(players);
  if (!criminalPlayer) {
    console.error('No criminal player found.');
    return;
  }

  console.log('Criminal player:', criminalPlayer);

  // Flag to determine if the game is over
  let gameEnded = false;

  // Check for detectives at the same airport as the criminal
  for (const player of players) {
    if (player.type === 1) { // Detectives only
      console.log(`Checking detective ${player.screen_name} at airport: ${player.latitude} ${player.longitude}`);
      console.log(`Comparing Detective with Criminal ${criminalPlayer.screen_name} at airport: ${criminalPlayer.latitude} ${criminalPlayer.longitude} and player ${player.latitude} ${player.longitude}`);

      // Compare airport IDs
      if (player.latitude && criminalPlayer.latitude &&
          player.longitude === criminalPlayer.longitude) {
        console.log(
          `Criminal ${criminalPlayer.screen_name} and Detective ${player.screen_name} are at the same airport!`
        );

        // Update winner message
        const winnerMessage = `Etsivä ${player.screen_name} sai kinnii karkurin ${criminalPlayer.screen_name}!`;

        // Store the message in localStorage
        localStorage.setItem('winnerMessage', winnerMessage);

        // Set game-ended flag
        gameEnded = true;

        // Exit loop as the game is over
        break;
      }
    }
  }

  if (gameEnded) {
    console.log('Game over!');
    // Redirect to gameover.html after a short delay
    setTimeout(() => {
      console.log('Redirecting to gameover.html...');
      window.location.href = '../pages/gameover.html';
    }, 2000);
  } else if (round === 10) {
    console.log('Round 10 reached. Game over due to time limit!');
    // Update the winner message for round 10
    const winnerMessage = `Rikollinen ${criminalPlayer.screen_name} pääsi karkuun.`;
    localStorage.setItem('winnerMessage', winnerMessage);

    // Redirect to gameover.html
    setTimeout(() => {
      console.log('Redirecting to gameover.html...');
      window.location.href = '../pages/gameover.html';
    }, 2000);
  } else {
    console.log('Game continues...');
  }
}
