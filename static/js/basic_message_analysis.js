const messagePanes = document.querySelectorAll('.eye-message-pane');

// Function to handle dropdown button click
function handleDropdownButtonClick(event) {
  const dropdownContent = event.target.nextElementSibling;
  dropdownContent.classList.toggle('show');
}

// Function to handle option click within dropdown content
function handleOptionClick(event) {
  event.preventDefault();
  const option = event.target;
  const dropdownContent = option.parentNode;
  const dropdownId = parseInt(dropdownContent.id.split('-').pop());

  let selectedKey = option.getAttribute('data-key');
  let selectedMode = option.getAttribute('data-mode');
  console.log(selectedKey, selectedMode)
  console.log(dropdownContent.id)
  if(dropdownContent.id === 'dropdown-content-' + dropdownId){
    selectedMode = document.getElementById('trigram-dropdown-content-' + dropdownId).getAttribute('selected-mode')
  } else {
    dropdownContent.setAttribute('selected-mode', selectedMode)
  }

  const selectedValue = option.textContent;

  const dropBtn = dropdownContent.previousElementSibling;
  dropBtn.textContent = selectedValue;
  dropdownContent.classList.remove('show');

  // Perform AJAX request to fetch message content
  fetch('/basic_analysis', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: selectedKey, mode: selectedMode })
  })
  .then(response => response.text()) // Convert response to text
  .then(data => {
    // Log the data for debugging
    data = JSON.parse(data);

    // Update the corresponding message pane with HTML code for images
    messagePanes[dropdownId].innerHTML = ''; // Clear previous content

    // Insert HTML code into the message pane
    messagePanes[dropdownId].insertAdjacentHTML('beforeend', data);
  })
  .catch(error => {
    console.error('Error fetching message content:', error);
  });
}

// Adding event listeners to dropdown buttons and options within dropdown content
document.querySelectorAll('.dropdown').forEach(function(dropDown, index) {
  const dropdownContent = dropDown.querySelector('.dropdown-content');
  const dropBtn = dropDown.querySelector('.dropbtn');

  dropBtn.addEventListener('click', handleDropdownButtonClick);

  dropdownContent.querySelectorAll('a').forEach(function(option) {
    option.addEventListener('click', handleOptionClick);
  });
});
