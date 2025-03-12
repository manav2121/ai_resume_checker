const API_URL = "https://ai-resume-checker-e833.onrender.com"; // Update this with your actual backend URL

document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-input");
    const resultDiv = document.getElementById("result");

    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        try {
            const response = await fetch(`${API_URL}/upload`, {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("Failed to upload file");
            }

            const data = await response.json();
            resultDiv.innerHTML = `<h3>Analysis Result:</h3><p>${data.result}</p>`;
        } catch (error) {
            console.error("Error:", error);
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    });
});
