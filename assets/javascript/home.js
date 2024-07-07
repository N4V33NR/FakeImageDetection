function toggleInput() {
    var fileUpload = document.getElementById("file_upload");
    var urlInput = document.getElementById("url_input");

    if (fileUpload.style.display === "block") {
        fileUpload.style.display = "none";
        urlInput.style.display = "block";
    } else {
        fileUpload.style.display = "block";
        urlInput.style.display = "none";
    }
}