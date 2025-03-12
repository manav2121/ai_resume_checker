document.getElementById("upload-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById("file-input");
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Uploading..."; // Show loading message
    
    if (fileInput.files.length === 0) {
        resultDiv.innerHTML = "Please select a file to upload.";
        return;
    }
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    try {
        const response = await fetch("https://ai-resume-checker-e833.onrender.com/upload", {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultDiv.innerHTML = `<h3>Upload Successful!</h3><p>${data.message}</p>`;
            if (data.extracted_text) {
                resultDiv.innerHTML += `<h4>Extracted Text:</h4><pre>${data.extracted_text}</pre>`;
            }
        } else {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
    }
});
