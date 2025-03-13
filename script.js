document.getElementById("uploadForm").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default form submission
    
    const fileInput = document.getElementById("resume");
    const resultDiv = document.getElementById("result");
    
    if (fileInput.files.length === 0) {
        resultDiv.innerHTML = "<p>Please select a file to upload.</p>";
        return;
    }
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    try {
        const response = await fetch("https://ai-resume-checker-e833.onrender.com/upload", {
            method: "POST",
            body: formData
        });
        
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        
        const data = await response.json();
        console.log("Server Response:", data); // Debugging log
        
        if (data.analysis) {
            resultDiv.innerHTML = `
                <h2>Analysis Result:</h2>
                <p><strong>Education:</strong> ${data.analysis.education}</p>
                <p><strong>Experience:</strong> ${data.analysis.experience.join(", ")}</p>
                <p><strong>Skills:</strong> ${data.analysis.skills.join(", ")}</p>
            `;
        } else {
            resultDiv.innerHTML = "<p>No analysis found.</p>";
        }
    } catch (error) {
        console.error("Error processing file:", error);
        resultDiv.innerHTML = "<p>Error processing file. Please try again.</p>";
    }
});
