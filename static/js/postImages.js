const images = document.querySelector("#post_images"); // get images from template
const imagesArray = JSON.parse(images.textContent);
console.log(imagesArray);
const output = document.querySelector("#imagesOutput");
const imagesInput = document.querySelector("#imagesInput");

showImages();
imagesInput.addEventListener("change", () => {
  const files = imagesInput.files;
  for (let i = 0; i < files.length; i++) {
    console.log(files[i]);
    imagesArray.push(files[i]);
  }
  showImages();
  console.log(imagesArray);
});

function showImages() {
  let images = "";
  imagesArray.forEach((image, index) => {
    images += `<div class="p-2 bd-highlight">
                 <img src="${image.url}"
                  alt="image"
                  style="border-radius:5%; width: 100%; object-fit: cover; height: 100px;"></img>
                  <button onclick=deleteImage(${index}) type="button" class="btn-close" aria-label="Close"></button>
               </div>`;
  });
  output.innerHTML = `<div style="display: flex; flex-wrap: nowrap; overflow-x: auto;">${images}</div>`;
}

function deleteImage(index) {
  imagesArray.splice(index, 1);
  showImages();
}

// showImages();
// // function checkImageType(image) {
// //   // Check image file type and convert it to jpeg
// // }
// // function changeImagesize(image) {
// //   // Check if the image size is greater than 1024x900
// // }
