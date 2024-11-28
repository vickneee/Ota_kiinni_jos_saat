// When a checkbox is clicked, uncheck all other checkboxes in the same row

const checkboxes = document.querySelectorAll('.choice-checkbox');

checkboxes.forEach(checkbox => {
  // Event listener
  checkbox.addEventListener('change', function() {
    if (this.checked) {
      const rowCheckboxes = this.closest('tr').querySelectorAll('input[type="checkbox"]');
      rowCheckboxes.forEach(cb => {
        // Uncheck all except the selected
        if (cb !== this) {
          cb.checked = false;
        }
      });
    }
  });
});