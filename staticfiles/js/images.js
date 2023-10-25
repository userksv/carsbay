console.log("Output");
const imagesInput = document.querySelector("#id_images");
const output = document.querySelector("#imageOutput");
const imagesArray = [];

imagesInput.addEventListener("change", () => {
  const files = imagesInput.files;
  for (let i = 0; i < files.length; i++) {
    imagesArray.push(files[i]);
  }
  showImages();
  console.log(imagesArray);
});

function showImages() {
  let images = "";
  imagesArray.forEach((image, index) => {
    images += `<div class="p-2 bd-highlight">
                 <img src="${URL.createObjectURL(image)}"
                  alt="image"
                  style="border-radius:5%; width: 100%; object-fit: cover; height: 100px;"></img>
                  <button onclick="deleteImage(${index})" type="button" class="btn-close" aria-label="Close"></button>
               </div>`;
  });
  output.innerHTML = images;
}
function checkImageType(image) {
  // Check image file type and convert it to jpeg
}
function changeImagesize(image) {
  // Check if the image size is greater than 1024x900
}
function deleteImage(index) {
  imagesArray.splice(index, 1);
  showImages();
  console.log(imagesArray);
}
