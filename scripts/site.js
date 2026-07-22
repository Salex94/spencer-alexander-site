/* Spencer Alexander Lawyers — small site behaviours */
(function () {
  "use strict";
  // Mobile menu toggle
  var toggle = document.querySelector("[data-nav-toggle]");
  var menu = document.getElementById("mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }
  // Current year in footer
  var y = document.querySelector("[data-year]");
  if (y) { y.textContent = new Date().getFullYear(); }

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // View transitions: some contexts skip the transition and fire an unhandled rejection — silence it
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

  // Scroll reveal — progressive enhancement; content is never hidden without JS + IO
  if ("IntersectionObserver" in window && !reduceMotion) {
    var revealSel = [
      ".section-head", ".area-card", ".detail-card", ".svc", ".process .step",
      ".faq-item", ".value", ".cred", ".post-card", ".fee-note", ".related__link",
      ".reach", ".intro-grid .prose", ".intro-grid .page-photo", ".process-grid .page-photo",
      ".bio__media", ".bio__body", ".info-block", ".form-card", ".faq-group__h"
    ].join(",");
    var revealEls = Array.prototype.slice.call(document.querySelectorAll(revealSel));
    if (revealEls.length) {
      document.documentElement.classList.add("js-reveal");
      var finish = function (el) {
        if (el.classList.contains("is-inview")) { return; }
        el.classList.add("is-inview");
        // Hand transitions back to the original styles once the entrance is done
        setTimeout(function () {
          el.classList.remove("reveal", "is-inview");
          el.style.transitionDelay = "";
        }, 980);
      };
      var vh = window.innerHeight || document.documentElement.clientHeight;
      var onScreen = [];
      revealEls.forEach(function (el) {
        el.classList.add("reveal");
        var i = 0, sib = el;
        while ((sib = sib.previousElementSibling)) { if (sib.classList.contains("reveal")) i++; }
        el.style.transitionDelay = Math.min(i, 5) * 70 + "ms";
        var r = el.getBoundingClientRect();
        if (r.top < vh * 0.96 && r.bottom > 0) { onScreen.push(el); }
      });
      // Reveal anything already in view on the next frame — no dependence on IO for first paint
      requestAnimationFrame(function () { requestAnimationFrame(function () { onScreen.forEach(finish); }); });
      var ioFired = false;
      var io = new IntersectionObserver(function (entries) {
        ioFired = true;
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          io.unobserve(entry.target);
          finish(entry.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
      revealEls.forEach(function (el) { io.observe(el); });
      // Canary: if IO never fires (hidden or throttled contexts), drop the effect entirely
      setTimeout(function () {
        if (!ioFired) {
          io.disconnect();
          document.documentElement.classList.remove("js-reveal");
          revealEls.forEach(function (el) {
            el.classList.remove("reveal", "is-inview");
            el.style.transitionDelay = "";
          });
        }
      }, 1200);
    }
  }

  // Same-page anchor scrolling — explicit, so it works even in embedded previews
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
  });

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
})();
