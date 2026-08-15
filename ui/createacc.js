const createAccountForm = document.getElementById("createAccountForm");
const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmPassword");

const emailCheck = document.getElementById("emailCheck");
const lengthRule = document.getElementById("lengthRule");
const matchRule = document.getElementById("matchRule");
const successPopup = document.getElementById("successPopup");
const continueBtn = document.getElementById("continueBtn");

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const usersStorageKey = "truthLensUsers";
const storageKeys = [usersStorageKey, "truthlensUsers", "users", "truthLensAccounts"];

function showError(input, message) {
  const errorElement = document.getElementById(`${input.id}Error`);

  input.classList.add("input-error");
  errorElement.textContent = message;
}

function clearError(input) {
  const errorElement = document.getElementById(`${input.id}Error`);

  input.classList.remove("input-error");
  errorElement.textContent = "";
}

function updateEmailCheck() {
  const emailIsValid = emailPattern.test(emailInput.value.trim());

  emailCheck.classList.toggle("visible", emailIsValid);
}

function updatePasswordRules() {
  const isLongEnough = passwordInput.value.length >= 8;
  const passwordsMatch =
    passwordInput.value.length > 0 &&
    passwordInput.value === confirmPasswordInput.value;

  lengthRule.classList.toggle("valid", isLongEnough);
  lengthRule.textContent = isLongEnough
    ? "✓ At least 8 characters"
    : "○ At least 8 characters";

  matchRule.classList.toggle("valid", passwordsMatch);
  matchRule.textContent = passwordsMatch
    ? "✓ Passwords match"
    : "○ Passwords match";
}

function validateForm() {
  let isValid = true;

  clearError(usernameInput);
  clearError(emailInput);
  clearError(passwordInput);
  clearError(confirmPasswordInput);

  if (usernameInput.value.trim() === "") {
    showError(usernameInput, "Please enter your name.");
    isValid = false;
  }

  if (emailInput.value.trim() === "") {
    showError(emailInput, "Please enter your email address.");
    isValid = false;
  } else if (!emailPattern.test(emailInput.value.trim())) {
    showError(emailInput, "Please enter a valid email address.");
    isValid = false;
  }

  if (passwordInput.value.length < 8) {
    showError(passwordInput, "Your password must be at least 8 characters.");
    isValid = false;
  }

  if (confirmPasswordInput.value === "") {
    showError(confirmPasswordInput, "Please confirm your password.");
    isValid = false;
  } else if (passwordInput.value !== confirmPasswordInput.value) {
    showError(confirmPasswordInput, "Passwords do not match.");
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

function saveUser() {
  const users = getSavedUsers();
  const email = emailInput.value.trim().toLowerCase();
  const password = passwordInput.value.trim();

  const emailAlreadyExists = users.some((user) => {
    const savedEmail = String(user.email || "").trim().toLowerCase();
    return savedEmail === email;
  });

  if (emailAlreadyExists) {
    showError(emailInput, "An account with this email already exists.");
    return false;
  }

  const newUser = {
    username: usernameInput.value.trim(),
    email: email,
    password: password
  };

  users.push(newUser);
  localStorage.setItem(usersStorageKey, JSON.stringify(users));
  localStorage.setItem("truthlensUsers", JSON.stringify(users));
  localStorage.setItem("users", JSON.stringify(users));

  return true;
}

function openSuccessPopup() {
  successPopup.hidden = false;
  continueBtn.focus();

  window.setTimeout(goToLogin, 3000);
}

function goToLogin() {
  window.location.href = "login.html";
}

emailInput.addEventListener("input", updateEmailCheck);

passwordInput.addEventListener("input", updatePasswordRules);
confirmPasswordInput.addEventListener("input", updatePasswordRules);

createAccountForm.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!validateForm()) {
    return;
  }

  if (saveUser()) {
    openSuccessPopup();
  }
});

continueBtn.addEventListener("click", goToLogin);