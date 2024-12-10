// When a checkbox is clicked, uncheck all other checkboxes in the same row
function checkboxes(){
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
}

// Check if a checkbox is checked for each player
function checked(){
  const form = document.querySelector('form');
  form.addEventListener('submit', function(event) {
    const rows = form.querySelectorAll('tr');
    let valid = true;

    rows.forEach(row => {
      const rowCheckboxes = row.querySelectorAll('input[type="checkbox"]');
      const isChecked = Array.from(rowCheckboxes).some(cb => cb.checked);

      if (!isChecked) {
        valid = false;
        rowCheckboxes.forEach(cb => cb.classList.add('error')); // Ad
        // const input = row.querySelector('input[type=checkbox]')
        // input.classList.add('error'); // Add error class to highlight the row
      } else {
        rowCheckboxes.forEach(cb => cb.classList.remove('error'));
      }
    });

    if (!valid) {
      event.preventDefault();

      // alert('Sinun täytyy valita valita jokaiselle pelaajalle tyyppi');
    }
    if(valid){
      window.location.href = '../pages/map.html'
    }
  });
  const checkboxes = form.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      const rowCheckboxes = this.closest('tr').querySelectorAll('input[type="checkbox"]');
      if (this.checked) {
         rowCheckboxes.forEach(cb => cb.classList.remove('error')); // Remove error class from all checkboxes in the same row
      }
    });
  });
}

// Start the game
function start_game(){
  const form = document.querySelector('form')
  const trs = form.querySelectorAll('tr')
  let players = []
  trs.forEach(tr=>{
      const input = tr.querySelector('input[name]');
      const boxes = tr.querySelectorAll('input[type=checkbox]')
      let type;
      if(tr.id === '1'){
        type = 0
      }else{
        type = 1
      }
      if (boxes[0].checked === true){
        let player = {name:input.value,type:type, is_computer:1}
        players.push(player)
      }else if(boxes[1].checked === true){
        let player = {name:input.value, type:type,is_computer:0}
        players.push(player)
      }
  });
  // console.log(players)
  return players
}

// Store the form data
function storeFormData(players){
  localStorage.setItem('players',JSON.stringify(players))
}

// Event listener for the form
const formlistener =()=>{
  checkboxes()
  const form = document.querySelector('form')
  const btn = document.querySelector('#submit')
  checked()
  form.addEventListener('submit',function(evt){
    evt.preventDefault()
    let players = start_game()
    localStorage.setItem('resume', 'false');

    storeFormData(players)

  })
}

formlistener();