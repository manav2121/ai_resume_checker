document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    let fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Please select a file.");
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
            alert("Success: " + result.message);
        } else {
            alert("Error: " + result.error);
        }
    } catch (error) {
        console.error("Upload failed:", error);
        alert("Failed to upload file.");
    }
});
