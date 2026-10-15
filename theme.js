/* Shared site theme: light default, key yeetngreet-site-theme */
(function () {
  var STORAGE = "yeetngreet-site-theme";
  var root = document.documentElement;

  function apply(theme) {
    var light = theme !== "dark";
    root.setAttribute("data-theme", light ? "light" : "dark");
    var btn = document.getElementById("themeToggle");
    if (btn) btn.textContent = light ? "Dark" : "Light";
  }

  var saved = localStorage.getItem(STORAGE);
  apply(saved === "dark" || saved === "light" ? saved : "light");

  function bind() {
    var btn = document.getElementById("themeToggle");
    if (!btn || btn.dataset.ygBound) return;
    btn.dataset.ygBound = "1";
    btn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      localStorage.setItem(STORAGE, next);
      apply(next);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();
