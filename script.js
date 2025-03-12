document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    let fileInput = document.getElementById("fileInput");
    let responseMessage = document.getElementById("responseMessage");

    if (!fileInput.files.length) {
        responseMessage.innerText = "Please select a file.";
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        let response = await fetch("https://ai-resume-checker-e833.onrender.com/upload", {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        if (response.ok) {
            responseMessage.innerText = "Success: " + result.message;
        } else {
            responseMessage.innerText = "Error: " + result.error;
        }
    } catch (error) {
        console.error("Upload failed:", error);
        responseMessage.innerText = "Failed to upload file.";
    }
});
