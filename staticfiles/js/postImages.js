const images = document.querySelector("#post_images"); // get images from template

const imagesFromServerArray = JSON.parse(images.textContent);
const preview = document.querySelector("#preview");
const imagesInput = document.querySelector("#id_images");
const submitBtn = document.querySelector("#submit-id-submit");
const imagesFromClientArray = [];

let combinedImages = [...imagesFromServerArray]; // this array for rendering images on page

displayImages(combinedImages);

async function updateData(id) {
  // Send PUT request to server with image id,
  // on server created list of image instances for deleting whitout saving changes
  const url = window.location;
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ imageId: id }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    console.log(response);
  } catch (error) {
    console.error("Error updating data:", error);
  }
}

function createElement(type, className) {
  // creating html element with class attr
  var element = document.createElement(type);
  element.className = className;
  return element;
}

function createCloseBtnOnImage(index, id) {
  const closeBtn = createElement(
    "button",
    "btn-close btn-close-hidden btn-close-white btn-close-visible-mobile"
  );
  closeBtn.setAttribute("data-bs-dismiss", "modal");
  closeBtn.setAttribute("arial-label", "Close");
  closeBtn.setAttribute("type", "button");
  closeBtn.setAttribute("onclick", `removeImageFromArray(${index}, ${id})`);
  return closeBtn;
}

function createImgElement(imgUrl, id, index) {
  const col = createElement(
    "div",
    "col mb-1 mr-2 image-container position-relative"
  );
  const img = createElement("img", "img");
  const closeBtn = createCloseBtnOnImage(index, id);
  img.style = "border-radius:5%; width: 140px; height: 100px;";
  img.src = imgUrl;
  img.id = id;

  col.append(img);
  col.append(closeBtn);

  return col;
}

function displayImages(imagesArray) {
  preview.innerHTML = ""; // clear preview div and render new images array

  imagesArray.forEach((image, index) => {
    if (index % 4 === 0) {
      // every 4th image starts on new row
      const dFlex = createElement("div", "d-flex justify-content-center");
      const row = createElement("div", "row mb-2");
      dFlex.append(row);
      preview.appendChild(dFlex);
    }
    const imgElement = createImgElement(image.url, image.id, index);

    const dFlexs = document.querySelectorAll(".d-flex.justify-content-center");
    const lastDFlex = dFlexs[dFlexs.length - 1];
    lastDFlex.lastChild.appendChild(imgElement);
  });
}

function removeImageFromArray(index, id) {
  console.log(id);
  // removes elements from combinedImages array
  // updateData sends request to server with id
  // removeFileFromFileList creates new fileList excluding image on index
  // combinedImages used only for rendering in template
  // images from client do not have id
  if (id !== 0) {
    updateData(id);
  } else {
    removeFileFromFileList(combinedImages[index]);
  }
  combinedImages.splice(index, 1);
  displayImages(combinedImages);
}

//////////////////////////////////////////////////////////////////////////////////////

imagesInput.addEventListener("change", handleInput, false);
// https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications
function handleInput() {
  const fileList = this.files;
  for (let i = 0; i < fileList.length; i++) {
    const file = fileList[i];

    if (!file.type.startsWith("image/")) {
      continue;
    }
    const imageURL = URL.createObjectURL(file); // for rendering in template
    const imageId = 0; // must be defined for combinedImages array
    const name = fileList[i].name;

    const image = { url: imageURL, id: imageId, name: name };
    imagesFromClientArray.push(image);
  }
  console.log(imagesFromClientArray);
  // creating combined array for rendering
  combinedImages = imagesFromServerArray.concat(imagesFromClientArray);
  displayImages(combinedImages);
}

function removeFileFromFileList(image) {
  // https://stackoverflow.com/a/64019766
  const dt = new DataTransfer();
  const input = document.querySelector("#id_images");
  const { files } = input;
  const fileListForManipulation = [...files];

  for (let i = 0; i < fileListForManipulation.length; i++) {
    const file = fileListForManipulation[i];
    if (file.name !== image.name) {
      // creating new file list excluding passed `image`
      dt.items.add(file);
    }
  }
  input.files = dt.files; // this input.files will be sent to server
}
