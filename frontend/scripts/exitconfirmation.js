document.addEventListener("DOMContentLoaded", function() {
  const menuDropdown = document.getElementById("menu");
  const confirmModal = document.getElementById("confirmModal");
  const confirmYes = document.getElementById("confirmYes");
  const confirmNo = document.getElementById("confirmNo");


  menuDropdown.addEventListener("change", function(event) {
    if (menuDropdown.value === "#") {
      event.preventDefault();
      confirmModal.style.display = "block";
    }

    confirmYes.addEventListener("click", function() {
      window.location.href = "../index.html";
    });

    confirmNo.addEventListener("click", function() {
      menuDropdown.value = "#";
      confirmModal.style.display = "none";
    });
  });
});
