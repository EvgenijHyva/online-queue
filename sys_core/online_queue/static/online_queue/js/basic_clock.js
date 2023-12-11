"use strict";
const displays = document.getElementsByClassName("time-display");

for (let display of displays) {
  const container = display.parentElement;
  if (container.classList.contains("d-none")) {
    container.classList.remove("d-none");
  }
}

if (displays.length) {
  const updateTime = () => {
    const time = new Date();
    let hours = time.getHours();
    let minutes = time.getMinutes();

    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;
    let timeString = `${hours}:${minutes}`;
    for (let display of displays) {
      display.innerText = timeString;
    }
  };

  setInterval(updateTime, 5000);

  updateTime();
} else {
  console.warn("Time display not found");
}
