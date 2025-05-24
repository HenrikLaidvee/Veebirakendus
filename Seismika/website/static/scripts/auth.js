const auth = firebase.auth();

// Näita ühte vormi, peida teised
function showForm(formName) {
  document.getElementById('login-form').style.display = 'none';
  document.getElementById('register-form').style.display = 'none';
  document.getElementById('reset-form').style.display = 'none';
  document.getElementById(`${formName}-form`).style.display = 'block';
}

// Teavituste funktsioon
function showNotification(message, type = "success") {
  const notification = document.getElementById("notification");
  notification.textContent = message;
  notification.className = `notification-box ${type}`;
  notification.style.display = "block";
  setTimeout(() => {
    notification.style.display = "none";
  }, 3000);
}

// Logimine
document.getElementById('login-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  auth.signInWithEmailAndPassword(email, password)
  .then(userCredential => {
    return userCredential.user.getIdToken();
  })
  .then(token => {
    return fetch("/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idToken: token })
    });
  })
  .then(res => {
    if (res.ok) {
      window.location.href = "/profile";
    } else {
      showNotification("Sessiooni loomine ebaõnnestus", "error");
    }
  })
  .catch(err => showNotification(err.message, "error"));
});

//  Registreerimine
document.getElementById('register-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const email = document.getElementById('register-email').value;
  const password = document.getElementById('register-password').value;
  const username = document.getElementById('register-username').value;

  auth.createUserWithEmailAndPassword(email, password)
    .then(cred => cred.user.updateProfile({ displayName: username }))
    .then(() => {
      showNotification("Kasutaja loodud! Logi nüüd sisse.", "success");
      showForm('login');
    })
    .catch(err => showNotification(err.message, "error"));
});

// Parooli taastamine
document.getElementById('reset-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const email = document.getElementById('reset-email').value;
  auth.sendPasswordResetEmail(email)
    .then(() => showNotification("Taastelink saadetud!", "success"))
    .catch(err => showNotification(err.message, "error"));
});

// Profiili andmete muutmini

const user = firebase.auth().currentUser;

function updateEmail() {
  const newEmail = document.getElementById("new-email").value;
  if (user && newEmail) {
    user.updateEmail(newEmail)
      .then(() => showProfileNotification("E-post uuendatud!", "success"))
      .catch(err => showProfileNotification(err.message, "error"));
  }
}

function updatePassword() {
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

