
document.querySelector("#url").addEventListener("keyup", (event) => {
    if (event.key === "Enter") {
        document.querySelector("#connect").click();
    }
});
document.querySelector("#msg").addEventListener("keyup", (event) => {
    if (event.key === "Enter") {
        document.querySelector("#send").click();
    }
});

let ws;

const notificationQueue = [];

function notify(msg, opts={type:"neutral"}) {
    notificationQueue.push([msg, opts]);
}

setInterval(() => {
    if (notificationQueue.length > 0) {
        const n = document.getElementById("notify");
        if (n.classList.contains("show")) return;
        const [msg, opts] = notificationQueue.shift();
        n.innerText = msg;
        n.classList.remove("error");
        n.classList.remove("success");
        switch (opts.type) {
            case "success":
                n.classList.add("success");
                break;
            case "error":
                n.classList.add("error");
                break;
        }
        n.classList.add("show");
        setTimeout(() => {
            n.classList.remove("show");
        }, notificationQueue.length > 2 ? 2000 : 4000);
    }
}, 100);

function sendMSG() {
    if (!ws || ws.readyState !== WebSocket.OPEN) return notify("WebSocket is not open", {type: "error"});
    let msg = document.getElementById("msg").value;
    ws.send(msg);
}

function onopen(event) {
    notify("Connection established", {type: "success"});
}

function onclose(event) {
    notify("Connection closed with code " + event.code + "\n" + event.reason, {type: event.code == 1000 ? "neutral" : "error"});
}

function onerror() {
    notify("WebSocket Error", {type: "error"});
}

function onmessage(event) {
    const dt = new Date();
    const msgs = document.getElementById("messages");
    msgs.innerHTML += `<div class="message"><span>${dt.toLocaleTimeString()}</span>${event.data}</div>`;
    msgs.scrollTop = msgs.scrollHeight;
}


function connect() {
    ws = new WebSocket(document.getElementById("url").value);
    ws.onopen = onopen;
    ws.onclose = onclose;
    ws.onmessage = onmessage;
    ws.onerror = onerror;
}

// notify("WebSocket is not open", {type: "neutral"});
// notify("WebSocket is dead", {type: "error"});
// notify("WebSocket is open", {type: "success"});