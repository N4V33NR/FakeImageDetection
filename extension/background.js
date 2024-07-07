//*** this script is used for background logic */

//download image

async function downloadImage(imageUrl) {
    url=imageUrl
     try {
       const response = await fetch(imageUrl);
       const blob = await response.blob();
       return blob;
     } catch (error) {
       console.error('Error downloading image:', error);
       return null;
     }
   }
   
   // Function to handle messages from content script
   chrome.runtime.onMessage.addListener(async function(message, sender, sendResponse) {
     if (message.action === 'imageClicked') {
       // Handle the image URL received from content script
       var imageUrl = message.imageUrl;
       console.log(imageUrl);
       // Perform any necessary actions with the image URL
       // download the image
       const blob = await downloadImage(imageUrl);
       
       // Display the downloaded image on the popup page
       displayImage(blob, url);
     }
   });
   
   
   
  // Function to get CSRF token from cookies
  function getCSRFToken() {
   const cookieValue = document.cookie.match(/(^|[^;]+)\s*csrftoken=([^;]*)/);
   return cookieValue ? cookieValue.pop() : '';
 }
 
 async function displayImage(blob, url) {
   if (blob && url) {
       try {
           const formData = new FormData();
           formData.append('image_url', url); // Include image URL in the form data
 
           const csrfToken = getCSRFToken(); // Get CSRF token from cookies
           const response = await fetch('http://127.0.0.1:8000/api/check-image-authenticity/', {
               method: 'POST',
               headers: {
                   'X-CSRFToken': csrfToken, // Include CSRF token in the request headers
               },
               body: formData // Send the FormData object in the request body
           });
           
           if (response.ok) {
               const data = await response.json();
               
               const result= document.getElementById("prediction")
               result.innerHTML=data.authenticity
               console.log('Prediction:', data.authenticity);
           } else {
               console.error('Failed to check image authenticity:', response.statusText);
           }
       } catch (error) {
           console.error('Error checking image authenticity:', error);
       }

       
       const imageUrl = URL.createObjectURL(blob); // Create URL for the blob representing the image
       const imagePreviewDiv = document.querySelector('.image-previews'); // Select the container for image previews
       
       // Check if there is an existing <img> element in the container
       const existingImgElement = imagePreviewDiv.querySelector('img');
       if (existingImgElement) {
           // Remove the existing <img> element
           existingImgElement.remove();
       }
       
       // Create a new <img> element
       const imgElement = document.createElement('img');
       imgElement.src = imageUrl; // Set the source (URL) for the image element
       
       // Create a <span> element to contain the image
       const imageSpan = document.createElement('span');
       imageSpan.classList.add('image'); // Add a CSS class to the <span> element
       imageSpan.appendChild(imgElement); // Append the image element to the <span>
       
       // Append the <span> containing the image to the container
       imagePreviewDiv.appendChild(imageSpan);
       
       
   } else {
       const errorMessage = document.createElement('p');
       errorMessage.textContent = 'Failed to download image';
       document.body.appendChild(errorMessage);
   }
 }
 