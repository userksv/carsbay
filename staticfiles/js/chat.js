const chatIcon = document.querySelector(".chat-icon");
const windowWidth = window.innerWidth;
function connect() {
  const chatLog = document.querySelector("#chat-log");
  const navBarMessageElement = document.getElementById("messages-navbar");
  const postDetailsMessageElement = document.getElementById(
    "post-details-message"
  );
  const protocol = window.location.protocol == "https:" ? "wss" : "ws";
  const url = `${protocol}://${window.location.host}/chat/`;
  // const url = "ws://carsbay.onrender.com/chat/";
  // console.log(url);

  let chatSocket = new WebSocket(url);
  let intervalID;
  const username = document.querySelector("#json_username").textContent.trim();
  const listUnstyled = document.querySelector("#list-conversations");
  let msgsFlag = false; // used for offCanvas

  function changeOffcanvasWidth() {
    if (windowWidth <= 768) {
      document
        .querySelector("#demo")
        .setAttribute(
          "style",
          "width: " + 100 + "% !important; visibility: visible;"
        );
      return;
    }
    document
      .querySelector("#demo")
      .setAttribute(
        "style",
        "width: " + 75 + "% !important; visibility: visible;"
      );
    return;
  }
  // clear chat-list
  document.getElementById("close-canvas").addEventListener("click", () => {
    document.querySelector(".chat-list").innerHTML = "";
  });

  function newMessageNotification(unreadCount) {
    let title = document.getElementById("title").textContent;
    let notification = `You have ${unreadCount} new messages!`;
    intervalID = setInterval(() => {
      document.title === title
        ? (document.title = notification)
        : (document.title = title);
    }, 1500);
  }

  function showPost(element) {
    const chatHeader = document.querySelector("#chat-header");
    const divPost = document.querySelector("#post-id");
    chatHeader.innerHTML = "";
    divPost.innerHTML = "";
    const img = document.createElement("img");
    const a = document.createElement("a");
    const h3 = document.createElement("h3");
    const p = document.createElement("p");

    img.className = "img-fluid custom-img img-thumbnail custom-img-header";
    img.src = element.image;
    a.href = `http://${window.location.host}/post/${element.post.id}`;
    a.target = "_blank";
    h3.textContent = `${element.post.make["make"]} ${element.post.model["name"]}`;
    p.textContent = `${element.post.price}₩`;
    a.append(h3);
    chatHeader.append(img);
    divPost.append(a, p);
  }

  function timestampToTime(timestamp) {
    const date = new Date(Number(timestamp));
    const hours = date.getHours();
    const minutes = date.getMinutes();
    if (hours < 12) {
      return `${hours}:${minutes} am`;
    }
    return `${hours}:${minutes} pm`;
  }

  function displayMessages(messages) {
    chatLog.innerHTML = " ";
    $(".modal-body").animate({ scrollTop: $(document).height() }, "fast");
    if (messages.length === 0) {
      chatLog.textContent = "No messages";
    }
    for (let i = 0; i < messages.length; i++) {
      const li = document.createElement("li");
      const p = document.createElement("p");
      const span = document.createElement("span");
      span.className = "time";
      p.textContent = messages[i].content;
      span.textContent = timestampToTime(messages[i].timestamp);
      if (username == messages[i].to_user.id) {
        li.className = "sender";
      } else {
        li.className = "replay";
      }
      li.append(p, span);
      chatLog.append(li);
    }
    const chatbox = document.querySelector(".chatbox");
    chatbox.classList.add("showbox");
  }

  function displayMessage(message) {
    // console.log(message);
    const li = document.createElement("li");
    const p = document.createElement("p");
    const span = document.createElement("span");
    span.className = "time";
    p.textContent = message["message"].content;
    span.textContent = timestampToTime(message["message"].timestamp);
    if (username == message["message"].to_user["id"]) {
      li.className = "sender";
    } else {
      li.className = "replay";
    }
    li.append(p, span);
    $(".modal-body").animate({ scrollTop: $(document).height() }, "fast");

    chatLog.append(li);
    showBox();
  }

  function displayConversation(conversation) {
    const chatList = document.querySelector(".chat-list");
    const a = document.createElement("a");
    const div = document.createElement("div");
    const img = document.createElement("img");
    const divContent = document.createElement("div");
    const h3 = document.createElement("h3");
    const p = document.createElement("p");

    a.href = "#";
    a.className = "d-flex align-items-center";
    a.id = `${conversation.id}`;
    div.className = "flex-shrink-0";
    // change image size
    img.src = `${conversation.image}`;
    img.className = "img-fluid img-thumbnail custom-img-conversation";
    divContent.className = "flex-grow-1 ms-3";
    h3.textContent = `${conversation.post["make"].make} ${conversation.post["model"].name}`;
    p.textContent = `${conversation.post["price"]} ₩`;

    div.append(img);
    divContent.append(h3, p);
    a.append(div, divContent);
    chatList.append(a);
  }

  function unlockMessageInput() {
    document.querySelector("#chat-message-input").disabled = false;
    document.querySelector("#chat-message-submit").disabled = false;
  }
  // Complete this functionality
  function showUnredMessagesStatus(unreadCount = false, id) {
    if (unreadCount) {
      const span = document.createElement("span");
      span.className = "contact-status unread";
      document.getElementById(`${id}`).append(span);
    }
  }

  chatSocket.onopen = function (e) {
    console.log("Opened", e);
  };

  if (navBarMessageElement) {
    navBarMessageElement.addEventListener("click", () => {
      chatSocket.send(JSON.stringify({ type: "get_conversations" }));
      // if (msgsFlag) {
      //   changeOffcanvasWidth(75);
      // }
    });
  }

  if (postDetailsMessageElement) {
    postDetailsMessageElement.addEventListener("click", () => {
      const postId = document.getElementById("json_post_id").textContent.trim();
      changeOffcanvasWidth();
      chatSocket.send(
        JSON.stringify({ type: "create_conversation", postId: postId })
      );
    });
  }
  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message_type = data["type"];

    switch (message_type) {
      case "new_message_notification":
        // put it to navbar if there is unread_count
        unreadCount = data.unread_count;
        if (unreadCount) {
          newMessageNotification(unreadCount);
        }
        break;

      case "get_conversations":
        // console.log(data);
        // clear list of conversations every time offcanvas is trigerred
        document.querySelector("#list-conversations").innerHTML = "";
        for (let i = 0; i < data.conversations.length; i++) {
          const element = data.conversations[i];
          displayConversation(element);
          document
            .getElementById(`${element.id}`)
            .addEventListener("click", () => {
              changeOffcanvasWidth();
              if (intervalID) {
                clearInterval(intervalID);
              }
              showPost(element);
              unlockMessageInput();
              // send current conversation name to consumer
              // and reset unread_count messages
              chatSocket.send(
                JSON.stringify({
                  type: "fetch_messages",
                  conversation_name: element.name,
                  // name_to_discard: name_to_discard
                })
              );
            });
        }
        break;

      case "fetch_messages":
        displayMessages(data.message, data.username);
        msgsFlag = true;
        break;

      case "chat_message":
        displayMessage(data);
        break;
      default:
        console.log("Unknow message type!");
    }

    document.querySelector("#chat-message-input").focus();
    document.querySelector("#chat-message-input").onkeyup = function (e) {
      if (e.key === "Enter") {
        document.querySelector("#chat-message-submit").click();
      }
    };

    document.querySelector("#chat-message-submit").onclick = function (e) {
      const messageInputDom = document.querySelector("#chat-message-input");
      const message = messageInputDom.value;
      // check if input string is not empty and not 'space'
      if (message.trim().length !== 0) {
        chatSocket.send(
          JSON.stringify({
            // send notification from here???
            type: "chat_message",
            message: message,
          })
        );
      }
      messageInputDom.value = "";
    };
  };

  chatSocket.onclose = function (e) {
    console.log("Closed", e);
  };
}
const userId = document.getElementById("json_username").textContent.trim();
if (userId) {
  connect();
}
const chatbox = document.querySelector(".chatbox");
chatIcon.addEventListener("click", () => {
  chatbox.classList.remove("showbox");
});
