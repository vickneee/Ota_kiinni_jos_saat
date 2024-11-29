document.addEventListener("DOMContentLoaded", function () {
  const menuDropdown = document.getElementById("menu");
  const instructionsModal = document.getElementById("instructionsModal");
  const confirmModal = document.getElementById("confirmModal");
  const returnBack = document.getElementById("return");
  const confirmYes = document.getElementById("confirmYes");
  const confirmNo = document.getElementById("confirmNo");

  menuDropdown.addEventListener("change", function (event) {
    event.preventDefault();

    const selectedValue = menuDropdown.value;

    if (selectedValue === "#instructions") {
      // Show instructions modal
      instructionsModal.style.display = "block";
    } else if (selectedValue === "#exit") {
      // Show exit confirmation modal
      confirmModal.style.display = "block";
    }

    // Reset dropdown value after handling
    menuDropdown.value = "#";
  });

  // Handle instructions modal pop up close
  returnBack.addEventListener("click", function () {
    instructionsModal.style.display = "none";
  });

  // Handle "exit confirmation modal actions
  confirmYes.addEventListener("click", function () {
    window.location.href = "../index.html";
  });

  confirmNo.addEventListener("click", function () {
    confirmModal.style.display = "none";
  });
});
