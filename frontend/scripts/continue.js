document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("saved-games-container");
    container.classList.add("saved-game-container");

    try {
        // Fetch saved games from the API
        const response = await fetch("http://127.0.0.1:3000/api/saved-games");

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        container.innerHTML = ""; // Clear placeholder text

        if (data.saved_games && data.saved_games.length > 0) {
            // Create a table to display saved games
            const table = document.createElement("table");
            table.classList.add("saved-games-table");

            // Create table header
            const headerRow = document.createElement("tr");
            headerRow.innerHTML = `
                <th class="new-game-th">Kierros</th>
                <th class="new-game-th">Pelaajat</th>
                <th class="new-game-th">Päivämäärä</th>
                <th class="new-game-th jatka-pelia">Jatka peliä</th>
            `;
            table.appendChild(headerRow);

            // Populate table rows with saved games
            data.saved_games.forEach((game) => {
                const gameRow = document.createElement("tr");
                gameRow.classList.add("game-row");


                const formattedDate = new Date(game.date).toLocaleDateString("fi-FI"); // Finnish date format (Nordic style)

                gameRow.innerHTML = `
                    <td class="new-game-td">${game.round}</td>
                    <td class="new-game-td">${game.players.length > 0 ? game.players.join(", ") : "None"}</td>
                    <td class="new-game-td">${formattedDate}</td>
                `;

                // Add Resume button
                const actionCell = document.createElement("td");
                const resumeButton = document.createElement("button");
                resumeButton.classList.add("continue-button");
                resumeButton.textContent = "Jatka peliä";
                resumeButton.addEventListener("click", async () => {
                  await resumeGame(game);
                  localStorage.setItem('resume', 'true');

                  window.location.href = '../pages/map.html';
                  console.log(game);
                });

                actionCell.appendChild(resumeButton);
                gameRow.appendChild(actionCell);
                table.appendChild(gameRow);
            });

            container.appendChild(table);
        } else {
            container.innerHTML = "<p>Tallennettuja pelejä ei ole.</p>";
        }
    } catch (error) {
        console.error("Error fetching saved games:", error);
        container.innerHTML = "<p>Error fetching saved games. Please try again later.</p>";
    }
});

  async function resumeGame(gamedata) {
    try {
      const response = await fetch('http://127.0.0.1:3000/api/resume_game', {
        method: 'POST',
        body: JSON.stringify({
          'gamedata': gamedata,
        }),
        headers: {
          'Content-type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const json = await response.json();
      console.log(json);
      return json
    } catch (error) {
      console.error('Error resuming game', error);
    }


}