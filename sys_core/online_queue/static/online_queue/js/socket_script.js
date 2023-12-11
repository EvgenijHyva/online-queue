"use strict";
const socket = new WebSocket("ws://" + window.location.host + "/ws/queue/");

const renderItem = (item, index, time) => {
  const { plate, created_at } = item;
  const listItemContainer = document.createElement("li");
  listItemContainer.classList.add(
    "list-group-item",
    "d-flex",
    "w-100",
    "justify-content-between"
  );
  listItemContainer.innerHTML = `<span class="align-self-center">
        <i class="fa-solid fa-car"></i>&nbsp;${String(plate).toUpperCase()}
      </span> 
      <small class="text-center align-self-center">
        <i class="fa-solid fa-square-parking"></i>&nbsp;${new Date(
          created_at
        ).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
          hour24: true,
        })}</small> 
      <small class="text-end align-self-center">
        <i class="fa-solid fa-hourglass-start"></i>&nbsp;${
          index * Number(time)
        } min
  </small>`;
  listItemContainer.setAttribute("data-id", plate);
  return listItemContainer;
};

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log(data);

  const platesDataArray = Object.values(data?.queue).sort(
    (a, b) => new Date(a.created_at) - new Date(b.created_at)
  );

  const ulsContainers = document.querySelectorAll("ul[id^='queue-list-']");
  for (let ul of ulsContainers) {
    ul.innerHTML = "";
  }

  const services = data?.queue
    ? [...new Set(platesDataArray.map((el) => el.service))]
    : [];

  for (let item of services) {
    const serviceContainer = document.getElementById(`queue-list-${item}`);
    const duration = serviceContainer.getAttribute("data-duration");
    const time = duration?.match(/\d+/)?.[0] ?? 0;
    let i = 0;
    for (let plateItem of platesDataArray) {
      if (plateItem.service === item) {
        i++;
        const itemHTML = renderItem(plateItem, i, time);
        serviceContainer.append(itemHTML);
      }
    }
  }
};

socket.onclose = function (event) {
  console.error("Connection closed:", event);
};
