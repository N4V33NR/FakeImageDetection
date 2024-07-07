//**this script works for popup.html page ***/


// Function to handle button click event
async function handleBtnClick() {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  var body = document.querySelector('body');
  body.style.background = "aqua";
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: imageUrl,
  });
}

const btn = document.querySelector('.btn');
btn.addEventListener('click', handleBtnClick);

