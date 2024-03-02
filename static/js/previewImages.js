const imagesInput = document.querySelector("#id_images");
const submitBtn = document.querySelector("#submit-id-submit");
const imagesArray = [];

function displayImages(imagesArray) {
  let images = "";
  for (let i = 0; i < imagesArray.length; i++) {
    const image = imagesArray[i].url;
    const imageId = imagesArray[i].id;
    images += `<div class="p-2 bd-highlight">
                   <img src="${image}"
                    alt="image"
                    style="border-radius:5%; width: 100%; object-fit: cover; height: 100px;"></img>
                    <button onclick="removeImageFromArray(${i})" type="button" class="obj btn-close" aria-label="Close"></button>
                 </div>`;
  }
  preview.innerHTML = `<div style="display: flex; flex-wrap: nowrap; overflow-x: auto;">${images}</div>`;
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
    // const imageId = 0; // must be defined for combinedImages array
    const name = fileList[i].name;

    const image = { url: imageURL, name: name };
    imagesArray.push(image);
  }
  // creating combined array for rendering
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
