function changeTheme() {
  var content = document.getElementById("theme-icon");
  if (content.classList.contains("fa-moon")) {
    content.classList.remove("fa-moon");
    content.classList.add("fa-sun");
  } else if (content.classList.contains("fa-sun")) {
    content.classList.remove("fa-sun");
    content.classList.add("fa-moon");
  }
}
