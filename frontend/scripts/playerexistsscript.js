// This script is used to check if a player already exists in the database when adding a new player.

async function fetchUserNames() {
  try {
    const response = await fetch('http://localhost:3000/api/check-user');
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    // console.log('Fetched data:', data); // Debugging line
    if (data.status === 200 && Array.isArray(data.player_info)) {
      // console.log('Fetched user names:', data.player_info); // Debugging line
      return data.player_info;
    } else {
      throw new Error(data.teksti || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching user names:', error);
    return [];
  }
}

async function checkUser(input) {
  const userNameInputs = document.querySelectorAll(
      'input[name="player1"], input[name="player2"], input[name="player3"]');
  const userNames = await fetchUserNames();
  // console.log('Fetched user names in checkUser:', userNames); // Debugging line

  if (userNames && Array.isArray(userNames)) {
    userNameInputs.forEach(input => {
          const userName = input.value.trim();
          // console.log('Checking user name:', userName); // Debugging line
          if (userNames.includes(userName)) {
            input.setCustomValidity('Username already exists');
            input.reportValidity();
          } else {
            input.setCustomValidity('');
          }
        },
    );
  }
}

document.addEventListener('DOMContentLoaded', async function() {
  const userNameInputs = document.querySelectorAll(
      'input[name="player1"], input[name="player2"], input[name="player3"]');
  // const userNames = await fetchUserNames();
  userNameInputs.forEach(input => {
    input.addEventListener('input', function() {
      checkUser(input);
    });
  });
});
