// Dark/Light theme toggle
const toggleBtn = document.getElementById("themeToggle");
if (toggleBtn) {
  toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
    if (document.body.classList.contains("light-mode")) {
      localStorage.setItem("theme", "light");
    } else {
      localStorage.setItem("theme", "dark");
    }
  });

  // Load saved theme
  if (localStorage.getItem("theme") === "light") {
    document.body.classList.add("light-mode");
  }
}
