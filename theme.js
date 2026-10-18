/* Shared site theme + mobile nav: light default, key yeetngreet-site-theme */
(function () {
  var STORAGE = "yeetngreet-site-theme";
  var root = document.documentElement;

  function apply(theme) {
    var light = theme !== "dark";
    root.setAttribute("data-theme", light ? "light" : "dark");
    document.querySelectorAll(".theme-toggle").forEach(function (btn) {
      btn.textContent = light ? "Dark" : "Light";
    });
  }

  var saved = localStorage.getItem(STORAGE);
  apply(saved === "dark" || saved === "light" ? saved : "light");

  function bindTheme() {
    document.querySelectorAll(".theme-toggle").forEach(function (btn) {
      if (btn.dataset.ygBound) return;
      btn.dataset.ygBound = "1";
      btn.addEventListener("click", function () {
        var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
        localStorage.setItem(STORAGE, next);
        apply(next);
      });
    });
  }

  function closeNav(toggle, nav) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
  }

  function openNav(toggle, nav) {
    toggle.setAttribute("aria-expanded", "true");
    nav.classList.add("is-open");
    document.body.classList.add("nav-open");
  }

  function bindNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    if (!toggle || !nav || toggle.dataset.ygNavBound) return;
    toggle.dataset.ygNavBound = "1";

    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      if (open) closeNav(toggle, nav);
      else openNav(toggle, nav);
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        closeNav(toggle, nav);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeNav(toggle, nav);
    });

    document.addEventListener("click", function (event) {
      if (!nav.classList.contains("is-open")) return;
      if (nav.contains(event.target) || toggle.contains(event.target)) return;
      closeNav(toggle, nav);
    });

    window.addEventListener("resize", function () {
      if (window.matchMedia("(min-width: 641px)").matches) {
        closeNav(toggle, nav);
      }
    });
  }

  function syncTableScrollHints() {
    document.querySelectorAll(".report-table-wrap").forEach(function (wrap) {
      var scrollable = wrap.scrollWidth > wrap.clientWidth + 1;
      wrap.classList.toggle("is-scrollable", scrollable);
    });
  }

  function bindTableScrollHints() {
    syncTableScrollHints();
    window.addEventListener("resize", syncTableScrollHints);
  }

  function bind() {
    bindTheme();
    bindNav();
    bindTableScrollHints();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();
