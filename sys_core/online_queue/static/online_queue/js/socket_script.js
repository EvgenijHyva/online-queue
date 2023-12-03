const socket = new WebSocket("ws://" + window.location.host + "/ws/queue/");

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log(data);
};

socket.onclose = function (event) {
  console.error("WebSocket closed:", event);
};
