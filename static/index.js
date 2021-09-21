let listening = false;
let speechFlag = true;
window.addEventListener("DOMContentLoaded", () => {
  const button = $("#mic-text");
  const result = $("#send-input");
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (typeof SpeechRecognition === "undefined") {
    button.attr("disabled", true);
    alert("Your browser doesn't support Speech Recognition. Sorry.");
  } else {
    listening = false;
    const recognition = new SpeechRecognition();
    const start = () => {
      recognition.start();
      button.addClass("speaking");
    };
    const stop = () => {
      recognition.stop();
      button.removeClass("speaking");
    };
    const onResult = (event) => {
      result.val("");
      for (const res of event.results) {
        const text = res[0].transcript;
        result.val(`${result.val()}${text}`);
        let objDiv = document.getElementById("send-input");
        objDiv.scrollTop = objDiv.scrollHeight;
      }
    };
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.addEventListener("result", onResult);
    button.on("click", () => {
      listening ? stop() : start();

      listening = !listening;
    });
  }
});

$("#voice").click(function () {
  if (speechFlag) {
    $("#voice").removeClass("fa-volume-up");
    $("#voice").addClass("fa-volume-mute");
    speechFlag = !speechFlag;
  } else {
    $("#voice").removeClass("fa-volume-mute");
    $("#voice").addClass("fa-volume-up");
    speechFlag = !speechFlag;
  }
});

let socket = io("https://vishwashackerbot.herokuapp.com/", {
  transports: ["websocket"],
reconnection:false
 });
$("#reload").click(function () {
  socket.disconnect();
  $("#message-container").html("");
  window.speechSynthesis.cancel();
  socket.connect();
});
socket.on("connect", function () {
  socket.emit("start", { data: "I'm connected!" });
});

socket.on("bot-message", function (data) {
  addData(createBotMessage(data.message));
  if (data.isOption) {
    addData(createButtons(data.options));
  }
  if (data.docs) {
    addData(createLink());
  }
  let objDiv = document.getElementById("message-container");
  objDiv.scrollTop = objDiv.scrollHeight;
  let speech;
  if (speechFlag) {
    speech = new SpeechSynthesisUtterance();
    speech.lang = "en-IN";
    speech.text = data.message;
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;
    if (data.isOption) {
      if (data.options.length === 2) {
        speech.text += `. Please select ${data.options[0]} or ${data.options[1]}`
      } else {
        let options = "";
        data.options.forEach((option) => {
          options += `${option}, `;
        });
        speech.text += ` Please select an option from ${options}`
      }
    }
    window.speechSynthesis.speak(speech);
  }
});

$("#send").click(function () {
  if ($("#send-input").val()) {
    window.speechSynthesis.cancel();
    addData(createUserMessage($("#send-input").val()));
    socket.emit("client-message", {
      select: false,
      message: $("#send-input").val(),
      select_data: "",
    });
    $("#send-input").val("");
    if (listening) {
      $("#mic-text").trigger("click");
    }
    let objDiv = document.getElementById("message-container");
    objDiv.scrollTop = objDiv.scrollHeight;
  }
});

$("#send-input").on("keyup", function (e) {
  if (e.keyCode === 13) {
    e.preventDefault();
    $("#send").trigger("click");
  }
});

function optionButtonClick(e, message) {
  window.speechSynthesis.cancel();
  addData(createUserMessage(message));
  $("button.option-btn").attr("disabled", true);
  socket.emit("client-message", {
    select: true,
    message: "",
    select_data: message,
  });
}

function createButtons(arr) {
  let buttons = `<div class="d-flex flex-wrap justify-content-center flex-row py-3"><DATA></div>`;
  let temp = buttons.split("<DATA>");
  let newButtons = temp[0];
  arr.forEach((item) => {
    let aTag = `<button class="btn btn-outline-success m-1 option-btn" onclick="optionButtonClick(this,'${item}')">`;
    newButtons += aTag + item + "</button>";
  });
  return newButtons + temp[1];
}

function createLink() {
  let buttons = `<div class="d-flex flex-wrap justify-content-center flex-row py-3"><DATA></div>`;
  let temp = buttons.split("<DATA>");
  let newButtons = temp[0];
  let url =
    "https://docs.google.com/forms/d/e/1FAIpQLSe_0-EIBY_jRAPKrI3FPwvPSBL-C-tdolilEyXvHHnKTdLxvg/viewform";
  newButtons += `<a href="${url}" target="_blank" class="btn btn-outline-success m-1 option-btn" onclick="optionButtonClick(this,'')">Register Now</a>`;
  newButtons += `<button class="btn btn-outline-success m-1 option-btn" onclick="optionButtonClick(this,'Skip')">Skip</button>`;
  return newButtons + temp[1];
}

function createBotMessage(message) {
  return `<div class="d-flex justify-content-start flex-row py-3">
  <img src="./static/chatbot.png" width="25" height="25" />
  <div class="chat ml-2 p-3">${message}</div>
</div>`;
}

function createUserMessage(message) {
  return `<div class="d-flex justify-content-end flex-row py-3">
  <div class="bg-white mr-2 p-3">
    <span class="text-muted">${message}</span>
  </div>
  <img src="./static/user.png" width="30" height="30" />
</div>`;
}

function addData(element) {
  $("#message-container").append(element);
}
