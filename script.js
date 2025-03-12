document.getElementById("uploadForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    let fileInput = document.getElementById("resumeInput");
    if (fileInput.files.length === 0) {
        alert("Please select a file to upload.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        let response = await fetch(" https://ai-resume-checker-e833.onrender.com/upload", {  // Change this to your actual backend endpoint
            method: "POST",
            body: formData
        });

        let result = await response.json();
        document.getElementById("result").innerText = `Result: ${result.message || "Processed successfully!"}`;
    } catch (error) {
        document.getElementById("result").innerText = "Error processing file!";
    }
});
