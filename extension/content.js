//*** this script works for the web page opened on the browser */


// Function to handle image URL extraction
function imageUrl() {
    document.addEventListener('click', function(event) {
      // Check if the clicked element is an image
      if (event.target.tagName.toLowerCase() === 'img') {
        event.preventDefault(); //*****this need to be removed when we are not using extension
        // Extract the URL of the clicked image
        var imageUrl = event.target.src;
        console.log(imageUrl);
        // Send the image URL to the background script
        chrome.runtime.sendMessage({
          action: 'imageClicked',
          imageUrl: imageUrl
        });
      }
    });
  }