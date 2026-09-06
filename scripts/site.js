/* Spencer Alexander Lawyers, small site behaviours (v3) */
(function () {
  "use strict";
  document.documentElement.classList.add("js");
  // Mobile menu toggle
  var toggle = document.querySelector("[data-nav-toggle]");
  var menu = document.getElementById("mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close navigation menu" : "Open navigation menu");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation menu");
      }
    });
  }
  if (toggle && menu) {
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("is-open")) {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation menu");
        toggle.focus();
      }
    });
  }

  // Preserve the visitor's service context without storing enquiry details.
  var enquiry = document.querySelector("[data-enquiry-form]");
  if (enquiry) {
    var matter = enquiry.querySelector("[name=matter]");
    var matterValues = {
      "family-law": "Family Law",
      "wills-and-estates": "Wills & Estates",
      "commercial-law": "Commercial Law"
    };
    var requestedMatter = new URLSearchParams(window.location.search).get("matter");
    if (matter && Object.prototype.hasOwnProperty.call(matterValues, requestedMatter)) {
      matter.value = matterValues[requestedMatter];
    }
    var preference = enquiry.querySelector("[name=contact_preference]");
    var phone = enquiry.querySelector("[name=phone]");
    var optionalPhone = enquiry.querySelector('label[for="phone"] .field-optional');
    if (preference && phone) {
      var syncPreference = function () {
        phone.required = preference.value === "Phone";
        if (optionalPhone) optionalPhone.textContent = phone.required ? "Required for a phone reply" : "Optional";
      };
      preference.addEventListener("change", syncPreference);
      syncPreference();
    }
  }

  // Optional first-party event hooks for a future analytics integration.
  // No network request, cookie, storage, form values or query strings are used.
  // A submission attempt is not evidence that the provider delivered an enquiry.
  var signal = function (action) {
    window.dispatchEvent(new CustomEvent("sa:conversion", {
      detail: { action: action, page: window.location.pathname }
    }));
  };
  document.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest("a[href]") : null;
    if (!link) return;
    var href = link.getAttribute("href");
    if (href.indexOf("tel:") === 0) signal("call_click");
    else if (/^\/contact(?:[?#]|$)/.test(href)) signal("enquiry_click");
  });
  if (enquiry) enquiry.addEventListener("submit", function () { signal("enquiry_submit_attempt"); });

  // Current year in footer
  var y = document.querySelector("[data-year]");
  if (y) { y.textContent = new Date().getFullYear(); }

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // View transitions: some contexts skip the transition and fire an unhandled rejection, so silence it
  window.addEventListener("unhandledrejection", function (e) {
    var msg = e.reason && (e.reason.message || e.reason);
    if (msg && String(msg).indexOf("Transition was skipped") !== -1) { e.preventDefault(); }
  });

  // Opt in to cross-page view transitions only in top-level windows (embedded contexts skip
  // transitions and log noisy rejections before any guard can attach)
  if (window.self === window.top && !reduceMotion) {
    try {
      var vt = document.createElement("style");
      vt.textContent = "@view-transition { navigation: auto; }";
      document.head.appendChild(vt);
    } catch (err) { /* no-op */ }
  }

  // Text and calls to action are available immediately, without scroll-reveal delays.

  // Same-page anchor scrolling, explicit so it works even in embedded previews
  // that block native hash-jump scrolling. Never uses scrollIntoView.
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var id = a.getAttribute("href").slice(1);
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    e.preventDefault();
    var top = el.getBoundingClientRect().top + (window.pageYOffset || document.documentElement.scrollTop) - 84;
    if (top < 0) top = 0;
    try { history.pushState(null, "", "#" + id); } catch (err) { /* no-op */ }
    window.scrollTo({ top: top, behavior: reduceMotion ? "auto" : "smooth" });
    if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "-1");
    try { el.focus({ preventScroll: true }); } catch (err) { el.focus(); }
  });


  // Insights category filter (progressive enhancement; the grid is complete without it)
  var filters = document.querySelector("[data-filters]");
  var grid = document.querySelector("[data-insights-grid]");
  var more = document.querySelector("[data-load-more]");
  if (more && grid) {
    more.addEventListener("click", function () { grid.classList.add("is-expanded"); more.parentNode.hidden = true; });
  }
  if (filters && grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".post-card"));
    filters.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("button[data-cat]") : null;
      if (!b) return;
      var cat = b.getAttribute("data-cat");
      grid.classList.add("is-expanded");
      if (more) { more.parentNode.hidden = true; }
      Array.prototype.forEach.call(filters.querySelectorAll("button[data-cat]"), function (x) {
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      });
      cards.forEach(function (c) {
        var el = c.querySelector(".post-cat");
        var own = el ? el.textContent.replace(/\s+/g, " ").trim() : "";
        c.classList.toggle("is-hidden", cat !== "all" && own !== cat);
      });
    });
  }

  // FAQ answer entrance on open
  document.addEventListener("toggle", function (e) {
    var d = e.target;
    if (!d || !d.classList || !d.classList.contains("faq-item") || !d.open) return;
    var a = d.querySelector(".faq-a");
    if (a && a.animate && !reduceMotion) {
      a.animate(
        [{ opacity: 0, transform: "translateY(-6px)" }, { opacity: 1, transform: "none" }],
        { duration: 240, easing: "cubic-bezier(0.32,0.08,0.24,1)" }
      );
    }
  }, true);
  // Home page film: click to play, source chosen for the device, end card stays up when it ends
  var film = document.querySelector("[data-film]");
  if (film) {
    var video = film.querySelector("video");
    // The poster is fetched only as the band approaches, so it never competes with the first paint
    var posterSrc = video.getAttribute("data-poster");
    if (posterSrc) {
      if ("IntersectionObserver" in window) {
        var posterIo = new IntersectionObserver(function (entries) {
          if (entries.some(function (e) { return e.isIntersecting; })) { video.poster = posterSrc; posterIo.disconnect(); }
        }, { rootMargin: "1200px 0px" });
        posterIo.observe(film);
      } else {
        video.poster = posterSrc;
      }
    }
    var playBtn = film.querySelector("[data-film-play]");
    var card = film.querySelector("[data-film-card]");
    var after = film.querySelector("[data-film-after]");
    var replay = film.querySelector("[data-film-replay]");
    var chosen = false;
    var quiet = function (p) { if (p && p.catch) p.catch(function () {}); };
    // With script running, the overlay is the one control until play; without it the native controls stay
    video.removeAttribute("controls");
    var pickSource = function () {
      if (chosen) return;
      chosen = true;
      var small = video.getAttribute("data-src-720");
      var large = video.getAttribute("data-src-1080");
      var conn = navigator.connection || {};
      var slow = !!conn.saveData || /(^|-)(2g|3g)$/.test(conn.effectiveType || "");
      var handheld = window.matchMedia("(max-width: 760px), (pointer: coarse) and (max-width: 1024px)").matches;
      var pick = small && (slow || handheld) ? small : large;
      if (pick) video.src = pick;
    };
    var loadCard = function () {
      if (!card || card.getAttribute("src")) return;
      var small = card.getAttribute("data-src-small");
      card.src = small && card.clientWidth < 700 ? small : card.getAttribute("data-src");
    };
    var leaveNativeSurfaces = function () {
      var fs = document.fullscreenElement || document.webkitFullscreenElement;
      if (fs === video) {
        quiet(document.exitFullscreen ? document.exitFullscreen() : (document.webkitExitFullscreen && document.webkitExitFullscreen()));
      } else if (video.webkitDisplayingFullscreen && video.webkitExitFullscreen) {
        video.webkitExitFullscreen();
      }
      if (document.pictureInPictureElement === video && document.exitPictureInPicture) quiet(document.exitPictureInPicture());
    };
    var start = function () {
      pickSource();
      quiet(video.play());
      video.focus({ preventScroll: true });
    };
    if (playBtn) playBtn.addEventListener("click", start);
    // The play event is the one place that sets the playing state, however playback was resumed
    video.addEventListener("play", function () {
      film.classList.add("is-playing");
      film.classList.remove("is-ended");
      video.setAttribute("controls", "");
      if (card) card.setAttribute("aria-hidden", "true");
      if (after) after.hidden = true;
    });
    video.addEventListener("playing", loadCard);
    video.addEventListener("ended", function () {
      var hadFocus = film.contains(document.activeElement);
      leaveNativeSurfaces();
      loadCard();
      film.classList.add("is-ended");
      video.removeAttribute("controls");
      if (card) card.removeAttribute("aria-hidden");
      if (after) after.hidden = false;
      if (hadFocus && replay) replay.focus({ preventScroll: true });
    });
    if (replay) replay.addEventListener("click", function () {
      video.currentTime = 0;
      start();
    });
  }
})();
