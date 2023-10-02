function connect() {
  const chatLog = document.querySelector("#chat-log");
  const navBarMessageElement = document.getElementById("messages-navbar");
  const postDetailsMessageElement = document.getElementById(
    "post-details-message"
  );
  const protocol = window.location.protocol == "https:" ? "wss" : "ws";
  const url = `${protocol}://${window.location.host}/chat/`;
  // const url = "ws://carsbay.onrender.com/chat/";
  console.log(url);

  let chatSocket = new WebSocket(url);
  let intervalID;
  const username = document.querySelector("#json_username").textContent.trim();
  const listUnstyled = document.querySelector("#list-conversations");
  let msgsFlag = false; // used for offCanvas

  function changeOffcanvasWidth(width) {
    document
      .querySelector("#demo")
      .setAttribute(
        "style",
        "width: " + width + "px !important; visibility: visible;"
      );
    return;
  }

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
    console.log(element.post);
    document.querySelector(".contact-profile").innerHTML = "";
    // console.log(element.image);
    const price = `${element.post.price}₩`;
    const p = document.createElement("p");
    p.append(price);

    const linkToPost = document.createElement("a");
    linkToPost.target = "_blank";
    const url = `http://${window.location.host}/post/${element.post.id}`;
    // const url = `"{\% url 'post-detail' ${element.post.id} \%}"`; this doesn't work
    linkToPost.href = url;
    linkToPost.append(
      `${element.post.make["make"]} ${element.post.model["name"]}`
    );

    const image = document.createElement("img");
    image.src = `/media/${element.image}`;
    document.querySelector(".contact-profile").append(image, linkToPost);
  }

  function messageDate(timestamp) {
    const dateTime = new Date(Number(timestamp));
    return `${dateTime.getHours()}:${dateTime.getMinutes()}`;
  }

  function displayMessages(messages) {
    console.log(messages);
    chatLog.innerHTML = " ";
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
    for (let i = 0; i < messages.length; i++) {
      const li = document.createElement("li");
      // const span = document.createElement("span");
      // span.append(messageDate(messages[i].timestamp));
      // span.className = "message-data-time";

      const message = document.createElement("p");
      message.append(messages[i].content);
      li.append(message);

      if (username == messages[i].to_user.id) {
        li.className = "sent";
      } else {
        li.className = "replies";
      }
      chatLog.append(li);
    }
  }

  function displayMessage(message) {
    // console.log(message);
    const li = document.createElement("li");

    const msg = document.createElement("p");
    msg.append(message["message"].content);
    li.append(msg);

    if (username == message["message"].to_user["id"]) {
      li.className = "sent";
    } else {
      li.className = "replies";
    }
    // auto scrolling I don't know how it works.
    // I need to learn this later
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
    chatLog.append(li);
  }

  function displayConversation(conversation) {
    const postName = `${conversation.post["make"].make} ${conversation.post["model"].name}`;
    const id = `${conversation.id}`;
    const price = `${conversation.post["price"]} ₩`;
    // const imgUrl = `{% url '${conversation.image}'%}`;
    const imgUrl = `/media/${conversation.image}`;
    //parent
    const img = document.createElement("img");
    img.src = imgUrl;
    const meta = document.createElement("div");
    meta.className = "meta";
    const postElement = document.createElement("p");
    postElement.setAttribute("class", "fw-light");
    const postTextNode = document.createTextNode(postName);
    postElement.append(postTextNode);

    const priceElement = document.createElement("p");
    priceElement.className = "preview";
    priceElement.append(price);

    const liElement = document.createElement("li");
    liElement.className = "contact";
    // liElement.id = id;

    const divWrap = document.createElement("div");
    divWrap.className = "wrap";
    divWrap.id = id;

    const nameElement = document.createElement("h2");
    nameElement.className = "name";

    nameElement.append(postName);
    meta.append(nameElement, priceElement);
    divWrap.append(img);
    divWrap.append(meta);
    liElement.appendChild(divWrap);
    listUnstyled.append(liElement);
    showUnredMessagesStatus(conversation.unread_count, id);
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
      if (msgsFlag) {
        changeOffcanvasWidth(900);
      } else changeOffcanvasWidth(360);
    });
  }

  if (postDetailsMessageElement) {
    postDetailsMessageElement.addEventListener("click", () => {
      const postId = document.getElementById("json_post_id").textContent.trim();
      changeOffcanvasWidth(900);
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
        console.log(data);
        // clear list of conversations every time offcanvas is trigerred
        document.querySelector("#list-conversations").innerHTML = "";
        for (let i = 0; i < data.conversations.length; i++) {
          const element = data.conversations[i];
          displayConversation(element);
          document
            .getElementById(`${element.id}`)
            .addEventListener("click", () => {
              changeOffcanvasWidth(900);
              // showPost(data.conversations[i].post.author.username);
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
