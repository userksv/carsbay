const imagesInput = document.querySelector("#id_images");
const submitBtn = document.querySelector("#submit-id-submit");
const div_id_images = document.querySelector("#div_id_images");
const parentPreview = document.querySelector("#parentPreview");
const preview = document.querySelector("#preview");

const imagesArray = [];

function createElement(type, className) {
  var element = document.createElement(type);
  element.className = className;
  return element;
}

function createCloseBtnOnImage(index) {
  const closeBtn = createElement(
    "button",
    "btn-close btn-close-hidden btn-close-white btn-close-visible-mobile"
  );
  closeBtn.setAttribute("data-bs-dismiss", "modal");
  closeBtn.setAttribute("arial-label", "Close");
  closeBtn.setAttribute("type", "button");
  closeBtn.setAttribute("onclick", `removeImageFromArray(${index})`);
  return closeBtn;
}

function createImgElement(imgUrl, imgIndex) {
  const col = createElement(
    "div",
    "col mb-1 mr-2 image-container position-relative"
  );
  const img = createElement("img", "img");
  const closeBtn = createCloseBtnOnImage(imgIndex);
  console.log(closeBtn);
  img.style = "border-radius:5%; width: 140px; height: 100px;";
  img.src = imgUrl;
  img.id = imgIndex;

  col.append(img);
  col.append(closeBtn);

  return col;
}

function displayImages(imagesArray) {
  preview.innerHTML = ""; // clear preview div and render new images array
  imagesArray.forEach((image, index) => {
    if (index % 4 === 0) {
      const dFlex = createElement("div", "d-flex justify-content-center");
      const row = createElement("div", "row mb-2");
      dFlex.append(row);
      preview.appendChild(dFlex);
    }
    const imgElement = createImgElement(image.url, index);

    const dFlexs = document.querySelectorAll(".d-flex.justify-content-center");
    const lastDFlex = dFlexs[dFlexs.length - 1];
    lastDFlex.lastChild.appendChild(imgElement);
  });
}

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
    const name = fileList[i].name;

    const image = { url: imageURL, name: name };
    imagesArray.push(image);
  }
  displayImages(imagesArray);
}

function removeImageFromArray(index) {
  removeFileFromFileList(imagesArray[index]);
  imagesArray.splice(index, 1);
  displayImages(imagesArray);
}

function removeFileFromFileList(image) {
  // https://stackoverflow.com/a/64019766
  const dt = new DataTransfer();
  const name = image.name;
  const input = document.querySelector("#id_images");
  const { files } = input;
  const fileListForManipulation = [...files];

  for (let i = 0; i < fileListForManipulation.length; i++) {
    const file = fileListForManipulation[i];
    if (file.name !== name) {
      dt.items.add(file);
    }
  }
  input.files = dt.files; // this input.files will be sent to server
  console.log(input.files);
}
