// Get username or ask for it if new user
function getUsername() {
    let username = localStorage.getItem("username");
    if (!username) {
        username = prompt("Enter your name:");
        if (username) {
            localStorage.setItem("username", username);
        } else {
            username = "Anonymous"; // Default if empty
        }
    }
    return username;
}

// Connect to the server with the username
const username = getUsername();
const socket = io("http://localhost:5000", {
    query: { username: username }
});

socket.on("connect", () => {
    console.log("Connected to server as", username);
});

// Receive and display full list of results
socket.on("update_results", (data) => {
    const resultList = document.getElementById("resultList");
    resultList.innerHTML = ""; // Clear existing list

    data.results.forEach(result => {
        const listItem = document.createElement("li");
        listItem.innerText = result;
        resultList.appendChild(listItem);
    });
});

function sendNumbers() {
    const num1 = parseFloat(document.getElementById("num1").value);
    const num2 = parseFloat(document.getElementById("num2").value);
    
    socket.emit("add_numbers", { username: username, num1, num2 });
}

document.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendNumbers();
});
