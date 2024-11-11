document.getElementById("prediction-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent default form submission

    // Gather form data
    const formData = new FormData(this);
    
    // Send a POST request to the server
    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        // Update the output div with the prediction results, using keys from JSON response
        document.getElementById("winner").textContent = "Winner: " + (data.winner || "N/A");
        document.getElementById("democrat-votes").textContent = "Democrat Votes: " + (data.democrat_votes || "N/A");
        document.getElementById("republican-votes").textContent = "Republican Votes: " + (data.republican_votes || "N/A");
    })
    .catch(error => console.error("Error:", error));
});
