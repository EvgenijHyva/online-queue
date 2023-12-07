const socket = new WebSocket("ws://" + window.location.host + "/ws/queue/");

const renderItem = (item, number) => {
  const { plate } = item;
  const listItemContainer = document.createElement("li");
  listItemContainer.classList.add(
    "list-group-item",
    "d-flex",
    "w-100",
    "justify-content-between"
  );
  listItemContainer.innerHTML = `<span>${String(
    plate
  ).toUpperCase()}</span> <small>~${"3 days ago"}</small>`;
  listItemContainer.setAttribute("data-id", plate);
  return listItemContainer;
};

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log(data);

  const platesDataArray = Object.values(data?.queue);
  const services = data?.queue
    ? [...new Set(platesDataArray.map((el) => el.service))]
    : [];

  for (let item of services) {
    const serviceContainer = document.getElementById(`queue-list-${item}`);
    serviceContainer.innerHTML = "";
    for (plateItem of platesDataArray) {
      if (plateItem.service === item) {
        const itemHTML = renderItem(plateItem);
        serviceContainer.append(itemHTML);
      }
    }
  }
};

socket.onclose = function (event) {
  console.error("Connection closed:", event);
};
