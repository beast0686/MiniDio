// Handle form submission
document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Stop the form from submitting normally

    var formData = new FormData(this);

    fetch('upload.php', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text()) // Assuming server sends plain text
        .then(data => {
            document.getElementById('minutesText').innerText = data;
            document.getElementById('minutesOutput').style.display = 'block';
            document.getElementById('knowMoreButtonContainer').style.display = 'block'; // Show Know More button
            // Optionally scroll to the output
            document.getElementById('minutesOutput').scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error uploading your file.');
        });
});

// Display selected filename
document.querySelector('.custom-file-input').addEventListener('change', function(e) {
    var fileName = e.target.files[0].name;
    var nextSibling = e.target.nextElementSibling;
    nextSibling.innerText = fileName;
});
