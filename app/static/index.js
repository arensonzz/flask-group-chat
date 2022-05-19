// const socket = io("localhost:5000/live-chat");
const socket = io("/live-chat");

const form = document.getElementById("form");
const input = document.getElementById("input");
const messageContainer = document.getElementById("messageContainer");
const leaveButton = document.getElementById("leaveButton");

// Test SocketIO connection
socket.on("connect", () => {
  socket.emit("joined", {});
  console.log("SocketIO: Connected to server");
});

socket.on("status", (data) => {
  let newItem = `
    <div class="row gap-1 mb-2">
      <div class="message-text col me-2 text-muted">${data.msg}</div>
    </div>
  `;
  messageContainer.insertAdjacentHTML("beforeend", newItem);
});

socket.on("message", (data) => {
  let newItem = `
    <div class="row gap-1 mb-2">
      <div class="message-info col-2 ms-2 align-self-start bg-secondary text-white rounded-2">${data.user}</div>
      <div class="message-text col me-2 border border-1 rounded-2">${data.msg}</div>
    </div>
  `;
  messageContainer.insertAdjacentHTML("beforeend", newItem);
});

form.addEventListener("submit", function (e) {
  e.preventDefault();
  if (input.value) {
    socket.emit("message", {msg: input.value});
    input.value = "";
  }
});

// Leave room before leaving page
leaveButton.addEventListener("click", () => {
  isLeave = confirm("Do you want to leave chat?");

  if (isLeave) {
    socket.emit("left", {}, () => {
      socket.disconnect();
      window.location.href = "/";
    });
  }
});

// SocketIO
