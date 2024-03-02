const images = document.querySelector("#post_images"); // get images from template

const imagesFromServerArray = JSON.parse(images.textContent);
const preview = document.querySelector("#preview");
const imagesInput = document.querySelector("#id_images");
const submitBtn = document.querySelector("#submit-id-submit");
const imagesFromClientArray = [];

let combinedImages = [...imagesFromServerArray]; // for rendering

displayImages(combinedImages);

async function updateData(id) {
  // Send PUT request to server with image id, on server created list of image instances for deleting
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

function displayImages(imagesArray) {
  let images = "";
  for (let i = 0; i < imagesArray.length; i++) {
    const image = imagesArray[i].url;
    const imageId = imagesArray[i].id;
    images += `<div class="p-2 bd-highlight">
                 <img src="${image}"
                  alt="image"
                  style="border-radius:5%; width: 100%; object-fit: cover; height: 100px;"></img>
                  <button onclick="removeImageFromArray(${i}, ${imageId})" type="button" class="obj btn-close" aria-label="Close"></button>
               </div>`;
  }
  preview.innerHTML = `<div style="display: flex; flex-wrap: nowrap; overflow-x: auto;">${images}</div>`;
}

function removeImageFromArray(index, id) {
  // removes elements from combinedImages array
  // updateData sends request to server with id
  // removeFileFromFileList creates new fileList excluding image on index
  // combinedImages used only for rendering in template
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
  // creating combined array for rendering
  combinedImages = imagesFromServerArray.concat(imagesFromClientArray);
  displayImages(combinedImages);
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
}
