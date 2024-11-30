// This script is used to check if a player already exists in the database when adding a new player.

async function fetchUserNames() {
  try {
    const response = await fetch('http://localhost:3000/api/check-user');
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    console.log('Fetched data:', data); // Debugging line
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

async function checkUser() {
  const userNameInputs = document.querySelectorAll(
      'input[name="player1"], input[name="player2"], input[name="player3"]');
  const userNames = await fetchUserNames();
  // console.log('Fetched user names in checkUser:', userNames); // Debugging line
  let resultMessage = '';

  if (userNames && Array.isArray(userNames)) {
    userNameInputs.forEach(input => {
          const userName = input.value.trim();
          // console.log('Checking user name:', userName); // Debugging line
          if (userNames.includes(userName)) {
            alert(`${userName} exists!`)
          // } else {
          //   resultMessage += `${userName} does not exist.`;
          // }
        }
      }
    );
  // } else {
  //   resultMessage = 'No user names fetched.';
  // }
    document.getElementById('result').innerHTML = resultMessage;
  }
}
