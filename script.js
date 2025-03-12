document.getElementById("uploadForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById("resume");
    const resultDiv = document.getElementById("result");
    
    if (fileInput.files.length === 0) {
        resultDiv.innerHTML = "Please select a file to upload.";
        return;
    }
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    try {
        resultDiv.innerHTML = "Uploading...";
        
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        resultDiv.innerHTML = `<strong>Analysis Result:</strong> <br>${data.result}`;
    } catch (error) {
        resultDiv.innerHTML = "Error uploading file. Please try again.";
        console.error("Error:", error);
    }
});
