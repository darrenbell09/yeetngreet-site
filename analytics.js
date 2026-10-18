/*
 * YeetnGreet site analytics: Cloudflare Web Analytics (cookie-free, no consent banner).
 * Included once on every marketing page, the /go/ redirect pages, and the docs.
 *
 * To enable: paste the site token from the Cloudflare dashboard
 * (Analytics & Logs > Web Analytics > yeetngreet.app > Manage site > JS snippet,
 * the value of "token") between the quotes on the next line. Leave it empty to stay off.
 */
var YG_CF_BEACON_TOKEN = "";

(function () {
  var token = YG_CF_BEACON_TOKEN;
  if (!token) {
    window.ygAnalyticsReady = Promise.resolve(false);
    return;
  }
  var s = document.createElement("script");
  s.defer = true;
  s.src = "https://static.cloudflareinsights.com/beacon.min.js";
  s.setAttribute("data-cf-beacon", JSON.stringify({ token: token }));
  window.ygAnalyticsReady = new Promise(function (resolve) {
    s.onload = function () { resolve(true); };
    s.onerror = function () { resolve(false); };
  });
  document.head.appendChild(s);
})();
