function downloadImage() {
    var imageURL = document.getElementById('imageURL').value;

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: imageURL }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                document.getElementById('displayedImage').src = data.image_path;
            } else {
                alert('Error downloading image. Please check the URL.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        });
}
