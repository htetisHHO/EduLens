const loginForm = document.getElementById("loginForm");
const loginEmailInput = document.getElementById("loginEmail");
const loginPasswordInput = document.getElementById("loginPassword");

const togglePasswordBtn = document.getElementById("togglePasswordBtn");
const forgotPasswordBtn = document.getElementById("forgotPasswordBtn");
const closeForgotPopupBtn = document.getElementById("closeForgotPopupBtn");
const continueBtn = document.getElementById("continueBtn");
const guestAccessBtn = document.getElementById("guestAccessBtn");

const loginError = document.getElementById("loginError");
const successPopup = document.getElementById("successPopup");

const forgotPasswordPopup = document.getElementById("forgotPasswordPopup");

const usersStorageKey = "truthLensUsers";
const storageKeys = [usersStorageKey, "truthlensUsers", "users", "truthLensAccounts"];
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function showFieldError(input, message) {
  const errorElement = document.getElementById(
    input.id === "loginEmail" ? "emailError" : "passwordError"
  );

  input.classList.add("input-error");
  errorElement.textContent = message;
}

function clearFieldError(input) {
  const errorElement = document.getElementById(
    input.id === "loginEmail" ? "emailError" : "passwordError"
  );

  input.classList.remove("input-error");
  errorElement.textContent = "";
}

function validateLoginForm() {
  let isValid = true;

  clearFieldError(loginEmailInput);
  clearFieldError(loginPasswordInput);
  loginError.textContent = "";

  if (loginEmailInput.value.trim() === "") {
    showFieldError(loginEmailInput, "Please enter your email address.");
    isValid = false;
  } else if (!emailPattern.test(loginEmailInput.value.trim())) {
    showFieldError(loginEmailInput, "Please enter a valid email address.");
    isValid = false;
  }

  if (loginPasswordInput.value === "") {
    showFieldError(loginPasswordInput, "Please enter your password.");
    isValid = false;
  }

  return isValid;
}

function getSavedUsers() {
  for (const key of storageKeys) {
    try {
      const rawValue = localStorage.getItem(key);
      if (!rawValue) continue;

      const parsed = JSON.parse(rawValue);
      if (Array.isArray(parsed)) {
        if (key !== usersStorageKey) {
          localStorage.setItem(usersStorageKey, JSON.stringify(parsed));
        }
        return parsed;
      }
    } catch (error) {
      continue;
    }
  }

  return [];
}

function accountMatches() {
  const email = loginEmailInput.value.trim().toLowerCase();
  const password = loginPasswordInput.value.trim();
  const users = getSavedUsers();

  return users.find((user) => {
    const savedEmail = String(user.email || "").trim().toLowerCase();
    const savedPassword = String(user.password || "").trim();

    return savedEmail === email && savedPassword === password;
  });
}

function openSuccessPopup() {
  successPopup.hidden = false;
  continueBtn.focus();

  window.setTimeout(goToChatbot, 2000);
}

function goToChatbot() {
  window.location.href = "CB2.html";
}

function continueAsGuest() {
  const guestUser = {
    name: "Guest",
    isGuest: true,
  };

  sessionStorage.setItem("truthLensCurrentUser", JSON.stringify(guestUser));
  goToChatbot();
}
function continueAsGuest() {
  const guestUser = {
    name: "Guest",
    isGuest: true,
  };

  sessionStorage.setItem("truthLensCurrentUser", JSON.stringify(guestUser));
  goToChatbot();
}

togglePasswordBtn.addEventListener("click", () => {
  const passwordIsHidden = loginPasswordInput.type === "password";

  loginPasswordInput.type = passwordIsHidden ? "text" : "password";
  togglePasswordBtn.textContent = passwordIsHidden ? "Hide" : "Show";
  togglePasswordBtn.setAttribute(
    "aria-label",
    passwordIsHidden ? "Hide password" : "Show password"
  );
});

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!validateLoginForm()) {
    return;
  }

  const user = accountMatches();

  if (!user) {
    loginError.textContent =
      "We could not find an account with that email and password.";
    return;
  }

  sessionStorage.setItem("truthLensCurrentUser", JSON.stringify(user));
  openSuccessPopup();
});

continueBtn.addEventListener("click", goToChatbot);

guestAccessBtn.addEventListener("click", continueAsGuest);


forgotPasswordBtn.addEventListener("click", () => {
  forgotPasswordPopup.hidden = false;
  closeForgotPopupBtn.focus();
});

closeForgotPopupBtn.addEventListener("click", () => {
  forgotPasswordPopup.hidden = true;
  forgotPasswordBtn.focus();
});
