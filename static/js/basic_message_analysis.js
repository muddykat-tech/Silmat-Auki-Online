var messagePanes = document.querySelectorAll('.eye-message-pane');

document.querySelectorAll('.dropdown').forEach(function(dropDown, index) {
    var dropDownContent = dropDown.querySelector('.dropdown-content');
    var dropBtn = dropDown.querySelector('.dropbtn');

    dropBtn.addEventListener('click', function() {
        dropDownContent.classList.toggle('show');
    });

    dropDownContent.querySelectorAll('a').forEach(function(option) {
        option.addEventListener('click', function(e) {
            e.preventDefault();
            var selectedKey = option.getAttribute('data-key');
            var selectedValue = option.textContent;
            dropBtn.textContent = selectedValue;
            dropDownContent.classList.remove('show');

            var textarea = document.querySelector(".editor-textarea");
            textarea.value = selectedValue;

            // Perform AJAX request to fetch message content
            fetch('/basic_analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: selectedKey })
            })
            .then(response => response.text()) // Convert response to text
            .then(data => {
                // Log the data for debugging
                data = JSON.parse(data)

                // Update the corresponding message pane with HTML code for images
                messagePanes[index].innerHTML = ''; // Clear previous content

                // Insert HTML code into the message pane
                messagePanes[index].insertAdjacentHTML('beforeend', data);
            })
            .catch(error => {
                console.error('Error fetching message content:', error);
            });
        });
    });
});
