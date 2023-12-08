const displays = document.getElementsByClassName("time-display");

if (displays.length) {
  const updateTime = () => {
    const time = new Date();
    let hours = time.getHours();
    let minutes = time.getMinutes();

    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;
    var timeString = `${hours}:${minutes}`;
    for (let display of displays) {
      display.innerText = timeString;
    }
  };

  setInterval(updateTime, 5000);

  updateTime();
} else {
  console.warn("Time display not found");
}
