// Initiate dropdowns for the play and start menus
document.addEventListener("DOMContentLoaded", function () {
  const playMenuDropdown = document.getElementById("play-menu");
  const startMenuDropdown = document.getElementById("start-menu");
  const instructionsModal = document.getElementById("instructionsModal");
  const confirmModal = document.getElementById("confirmModal");
  const returnBack = document.getElementById("return");
  const confirmYes = document.getElementById("confirmYes");
  const confirmNo = document.getElementById("confirmNo");

  // Event listeners for the dropdowns
  playMenuDropdown.addEventListener("change", function () {
    const selectedValue = playMenuDropdown.value;
    if (selectedValue === "#instructions") {
      instructionsModal.style.display = "block";
    } else if (selectedValue === "#exit") {
      confirmModal.style.display = "block";
    }
    playMenuDropdown.value = "#";
  });

  // Event listeners for the dropdowns
  startMenuDropdown.addEventListener("change", function () {
    const selectedValue = startMenuDropdown.value;
    if (selectedValue === "#instructions") {
      instructionsModal.style.display = "block";
    } else if (selectedValue === "#exit") {
      confirmModal.style.display = "block";
    }
    startMenuDropdown.value = "#";
  });

  returnBack.addEventListener("click", function () {
    instructionsModal.style.display = "none";
  });

  confirmYes.addEventListener("click", function () {
    window.location.href = "../index.html";
  });

  confirmNo.addEventListener("click", function () {
    confirmModal.style.display = "none";
  });
});