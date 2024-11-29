document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("saved-games-container");

    try {
        // Fetch saved games from the API
        const response = await fetch("http://127.0.0.1:3000/api/saved-games");

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        container.innerHTML = ""; // Clear placeholder text

        if (data.saved_games && data.saved_games.length > 0) {
            // Display saved games
            data.saved_games.forEach((game) => {
                const gameDiv = document.createElement("div");
                gameDiv.classList.add("game-row"); // Use CSS for styling

                gameDiv.innerHTML = `
                    <span><strong>Round:</strong> ${game.round}</span>
                    <span><strong>Players:</strong> ${
                        game.players.length > 0 ? game.players.join(", ") : "None"
                    }</span>
                `;

                // Add Resume button
                const resumeButton = document.createElement("button");
                resumeButton.textContent = "Jatka peliä";
                resumeButton.addEventListener("click", () => {
                    window.location.href = `./game.html?game_id=${game.game_id}`;
                });

                gameDiv.appendChild(resumeButton);
                container.appendChild(gameDiv);
            });
        } else {
            container.innerHTML = "<p>Tallennettuja pelejä ei ole.</p>";
        }
    } catch (error) {
        console.error("Error fetching saved games:", error);
        container.innerHTML = "<p>Error fetching saved games. Please try again later.</p>";
    }
});
