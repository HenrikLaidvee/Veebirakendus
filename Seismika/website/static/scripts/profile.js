let editVisible = false;

function toggleEdit() {
  const section = document.getElementById("edit-section");
  const box = document.getElementById("profile-box");
  editVisible = !editVisible;

  if (editVisible) {
    section.style.display = "block";
    box.style.maxWidth = "700px";
  } else {
    section.style.display = "none";
    box.style.maxWidth = "500px";
  }
}

function updateEmail() {
  const user = firebase.auth().currentUser;
  const newEmail = document.getElementById("new-email").value;
  if (user && newEmail) {
    user.updateEmail(newEmail)
      .then(() => showProfileNotification("E-post uuendatud!", "success"))
      .catch(err => showProfileNotification(err.message, "error"));
  }
}

function updatePassword() {
  const user = firebase.auth().currentUser;
  const newPassword = document.getElementById("new-password").value;
  if (user && newPassword) {
    user.updatePassword(newPassword)
      .then(() => showProfileNotification("Parool uuendatud!", "success"))
      .catch(err => showProfileNotification(err.message, "error"));
  }
}

function showProfileNotification(message, type = "success") {
  const box = document.getElementById("profile-notification");
  box.textContent = message;
  box.className = `notification-box ${type}`;
  box.style.display = "block";
  setTimeout(() => {
    box.style.display = "none";
  }, 3000);
}

function updateUsername() {
  const user = firebase.auth().currentUser;
  const newUsername = document.getElementById("new-username").value;
  if (user && newUsername) {
    user.updateProfile({ displayName: newUsername })
      .then(() => {
        showProfileNotification("Kasutajanimi uuendatud!", "success");
        // DOM-i uuendamine
        const header = document.querySelector("#profile-box h4");
        if (header) {
          header.textContent = `Tere tulemast, ${newUsername}!`;
        }
      })
      .catch(err => showProfileNotification(err.message, "error"));
  }
}


