const socket = io("http://localhost:5000");

        socket.on("connect", () => {
            console.log("Connected to server");
        });

        socket.on("result", (data) => {
            document.getElementById("result").innerText = data.result;
        });

        function sendNumbers() {
            const num1 = parseFloat(document.getElementById("num1").value);
            const num2 = parseFloat(document.getElementById("num2").value);
            socket.emit("add_numbers", { num1, num2 });
        }