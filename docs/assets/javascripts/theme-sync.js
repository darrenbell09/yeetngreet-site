/* Sync marketing data-theme with Material color scheme (shared localStorage key). */
(function () {
  var STORAGE = "yeetngreet-site-theme";
  var root = document.documentElement;

  function apply(theme) {
    var light = theme !== "dark";
    root.setAttribute("data-theme", light ? "light" : "dark");
    if (document.body) {
      document.body.setAttribute("data-md-color-scheme", light ? "default" : "slate");
    }
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

  function bindImageZoom() {
    if (window.matchMedia("(max-width: 640px)").matches === false) return;
    document.querySelectorAll(".md-typeset img").forEach(function (img) {
      if (img.dataset.ygZoomBound) return;
      if (img.closest("a")) return;
      img.dataset.ygZoomBound = "1";
      img.style.cursor = "zoom-in";
      img.addEventListener("click", function () {
        window.open(img.currentSrc || img.src, "_blank", "noopener,noreferrer");
      });
    });
  }


  function closeDocsDrawer() {
    var drawer = document.getElementById("__drawer");
    if (drawer && drawer.checked) {
      drawer.checked = false;
      drawer.dispatchEvent(new Event("change", { bubbles: true }));
    }
  }

  function bindDrawerEscape() {
    if (document.documentElement.dataset.ygDrawerEsc) return;
    document.documentElement.dataset.ygDrawerEsc = "1";
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeDocsDrawer();
    });
  }

  function bind() {
    bindTheme();
    bindImageZoom();
    bindDrawerEscape();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(function () {
      apply(localStorage.getItem(STORAGE) || "light");
      bind();
    });
  }
})();
