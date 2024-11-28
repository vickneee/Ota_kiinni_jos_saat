// Ehkä toimii ehkä ei:D pitää kokeilla myöhemmin vielä
// When pressing "palaa" in instructions. User is redirected to the game and no progress is lost

document.addEventListener("DOMContentLoaded", () => {
  const backtoGameButton = document.getElementById("backToGame");

  backtoGameButton.addEventListener("click", () => {
    window.history.back()
  })
})