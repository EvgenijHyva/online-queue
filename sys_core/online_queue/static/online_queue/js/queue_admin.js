"use strict";
const socket = new WebSocket("ws://" + window.location.host + "/ws/queue/");
let globalPlates = [];

const renderItem = (item, time) => {
  const { plate, created_at } = item;
  const listItemContainer = document.createElement("li");
  listItemContainer.classList.add(
    "list-group-item",
    "d-flex",
    "w-100",
    "justify-content-between"
  );
  listItemContainer.innerHTML = `
    <span class="align-self-center plate-block">
      <i class="fa-solid fa-car"></i>&nbsp;${String(plate).toUpperCase()}
    </span>
    <small class="align-self-center middle-block">
      <i class="fa-solid fa-square-parking"></i>&nbsp;${new Date(
        created_at
      ).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        hour24: true,
      })}
    </small>  
    <div class="d-flex gap-3">
      <button 
        type="button" 
        class="btn btn-danger" 
        data-bs-toggle="modal" 
        data-bs-target="#staticBackdrop"
        onClick="renderModalBody('cancel', '${plate}')"
      > 
        <i class="fa-solid fa-trash-can"></i> 
      </button>
      <button 
        type="button" 
        class="btn btn-success" 
        data-bs-toggle="modal" 
        data-bs-target="#staticBackdrop"
        onClick="renderModalBody('confirm', '${plate}')"
      > 
        <i class="fa-regular fa-circle-check"></i> 
      </button> 
    </div>
  `;
  listItemContainer.setAttribute("data-id", plate);
  return listItemContainer;
};

const renderModalBody = (type, plate) => {
  const dataItem = globalPlates.find((item) => item.plate === plate);
  if (!dataItem) return;
  const title = document.getElementById("staticBackdropLabel");
  const body = document.querySelector("div[class='modal-body']");
  body.setAttribute("data-plate", plate);
  const confirmBtn = document.getElementById("confirm-button");
  const event = { type: "modify_queue" };
  switch (type) {
    case "confirm":
      title.innerText = "Confirm";
      body.innerText = `'${dataItem.plate}' ${gettext("Done")}?`;
      confirmBtn.addEventListener("click", async () => {
        await socket.send(
          JSON.stringify({ ...event, action: "done", item: dataItem })
        );
      });
      return;
    case "cancel":
      title.innerText = "Cancel";
      body.innerText = `${gettext("Cancel car")} '${dataItem.plate}'?`;
      confirmBtn.addEventListener("click", async () => {
        await socket.send(
          JSON.stringify({ ...event, action: "cancel", item: dataItem })
        );
      });
      return;
    default:
      return;
  }
};

socket.onerror = (e) => {
  console.log("error socket", e);
};

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log(data);

  const platesDataArray = Object.values(data?.queue).sort(
    (a, b) => new Date(a.created_at) - new Date(b.created_at)
  );
  globalPlates = platesDataArray;

  const ulsContainers = document.querySelectorAll("ul[id^='queue-list-']");
  for (let ul of ulsContainers) {
    ul.innerHTML = "";
  }

  const services = data?.queue
    ? [...new Set(platesDataArray.map((el) => el.service))]
    : [];

  for (let item of services) {
    const serviceContainer = document.getElementById(`queue-list-${item}`);

    for (let plateItem of platesDataArray) {
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

socket.onerror = function (event) {
  console.error("error", event);
};
