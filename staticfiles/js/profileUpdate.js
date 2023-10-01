// const url = `http://${window.location.host}/users/get-image/${userId}`;

// function getProfileImage(url) {
//   const getImage = fetch(url)
//     .then((res) => {
//       return res.json();
//     })
//     .then((data) => {
//       const profileImage = document.getElementById("profile-image");
//       //   profileImage.setAttribute("src", data.image);
//       console.log(data.image);
//     });
// }
// function deleteProfileImage(id) {
//   const url = `http://${window.location.host}/users/delete-profile-image/${id}`;
//   const rawResponse = fetch(url, {
//     method: "POST",
//     headers: {
//       Accept: "application/json",
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ type: "delete_image" }),
//   });
//   const content = rawResponse.json();
//   console.log(content);
// }
// // getProfileImage(url);
// deleteProfileImage(userId);
