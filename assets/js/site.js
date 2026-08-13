/* =============================================================================
   MSIG site behaviour — plain, dependency-free JavaScript.
   The site is server-rendered, so every piece of content is in the HTML and
   readable without JS. This file only layers on interactivity: theme toggle,
   mobile nav, tabs, expand/collapse cards, the alumni accordion, the gallery
   carousel, and the publications filter. Each feature is isolated and guards
   against its target being absent, so pages only run what they need.
   ============================================================================= */
(function () {
  "use strict";

  /* ---- Shared: animate a panel open/closed by max-height ------------------ */
  function setPanel(panel, open) {
    if (!panel) return;
    if (open) {
      panel.style.maxHeight = panel.scrollHeight + "px";
      var done = function (e) {
        if (e.propertyName !== "max-height") return;
        panel.removeEventListener("transitionend", done);
        // Let the panel grow naturally afterwards (handles images/reflow).
        if (panel.dataset.open === "1") panel.style.maxHeight = "none";
      };
      panel.addEventListener("transitionend", done);
      panel.dataset.open = "1";
    } else {
      // Fix the current height, force reflow, then collapse — so "none" animates.
      panel.style.maxHeight = panel.scrollHeight + "px";
      void panel.offsetHeight;
      panel.dataset.open = "0";
      panel.style.maxHeight = "0px";
    }
  }

  /* ---- Theme toggle (light / dark, remembered) ---------------------------- */
  function initTheme() {
    var root = document.documentElement;
    document.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-theme-toggle]");
      if (!btn) return;
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("msig-theme", next); } catch (err) {}
    });
  }

  /* ---- Mobile navigation -------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var links = document.getElementById("nav-links");
    if (!toggle || !links) return;
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // Close the menu after following a link.
    links.addEventListener("click", function (e) {
      if (e.target.closest(".navbar__link")) {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---- Tabs --------------------------------------------------------------- */
  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (root) {
      var tabs = root.querySelectorAll(".tabs__tab");
      var panels = root.querySelectorAll(".tabs__panel");
      tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          var id = tab.getAttribute("data-tab");
          tabs.forEach(function (t) {
            var on = t === tab;
            t.classList.toggle("tabs__tab--active", on);
            t.setAttribute("aria-selected", on ? "true" : "false");
          });
          panels.forEach(function (p) {
            p.hidden = p.getAttribute("data-panel") !== id;
          });
        });
      });
    });
  }

  /* ---- Expand / collapse cards (projects, people, PI details) ------------- */
  function initExpandables() {
    document.addEventListener("click", function (e) {
      var trigger = e.target.closest("[data-expand]");
      if (!trigger) return;
      // A whole card can be the trigger (e.g. the PI card). Let real links and
      // other buttons inside it work normally instead of toggling.
      var interactive = e.target.closest("a, button");
      if (interactive && interactive !== trigger && !interactive.hasAttribute("data-expand")) return;
      var box = trigger.closest("[data-expandable]");
      if (!box) return;
      var panel = box.querySelector(".expand-panel");
      var open = !box.classList.contains("is-open");
      box.classList.toggle("is-open", open);
      // Keep every toggle in this card (header region + Details button) in sync.
      box.querySelectorAll("[data-expand]").forEach(function (t) {
        t.setAttribute("aria-expanded", open ? "true" : "false");
      });
      setPanel(panel, open);
    });
  }

  /* ---- Accordion (alumni, publications) ----------------------------------
     Delegated from the document so it also drives accordions built after boot
     — the publications list is rendered once ORCID answers. */
  function initAccordion() {
    document.addEventListener("click", function (e) {
      var header = e.target.closest ? e.target.closest(".accordion__header") : null;
      if (!header) return;
      var item = header.closest(".accordion__item");
      var panel = item && item.querySelector(".accordion__panel");
      var open = header.getAttribute("aria-expanded") !== "true";
      header.setAttribute("aria-expanded", open ? "true" : "false");
      setPanel(panel, open);
    });
  }

  /* ---- Carousel (gallery) ------------------------------------------------- */
  function initCarousels() {
    document.querySelectorAll("[data-carousel]").forEach(function (root) {
      var slides = Array.prototype.slice.call(root.querySelectorAll(".carousel__slide"));
      var thumbs = Array.prototype.slice.call(root.querySelectorAll(".carousel__thumb"));
      var counter = root.querySelector(".carousel__counter");
      var caption = root.querySelector(".carousel__caption");
      var n = slides.length;
      if (!n) return;
      var i = 0;

      function show(idx) {
        i = (idx + n) % n;
        slides.forEach(function (s, j) { s.classList.toggle("is-active", j === i); });
        thumbs.forEach(function (t, j) { t.classList.toggle("is-active", j === i); });
        if (counter) counter.textContent = (i + 1) + " / " + n;
        if (caption) caption.textContent = slides[i].getAttribute("data-caption") || "";
      }

      root.querySelectorAll("[data-carousel-prev]").forEach(function (b) {
        b.addEventListener("click", function () { show(i - 1); });
      });
      root.querySelectorAll("[data-carousel-next]").forEach(function (b) {
        b.addEventListener("click", function () { show(i + 1); });
      });
      thumbs.forEach(function (t, j) {
        t.addEventListener("click", function () { show(j); });
      });
      // Keyboard arrows when the carousel has focus.
      root.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") { show(i - 1); }
        else if (e.key === "ArrowRight") { show(i + 1); }
      });
      show(0);
    });
  }

  /* ---- Publications ------------------------------------------------------
     The list is rendered at build time from _data/publications_generated.yml
     (written by tools/sync_publications.py), so crawlers receive the paper
     titles instead of a loading message, and the page needs no network round
     trip to show anything.

     Nothing is fetched here any more. The only behaviour left is the Cite
     button, which copies the citation string already sitting in each button's
     data-citation attribute. The year accordion needs no code of its own --
     initAccordion is delegated from the document and picks up the
     server-rendered markup. */
  function initPublications() {
    var list = document.querySelector("[data-pub-list]");
    if (!list) return;

    /* navigator.clipboard needs a secure context, so keep the old execCommand
       path as a fallback. */
    function copyText(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text);
      }
      return new Promise(function (resolve, reject) {
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.setAttribute("readonly", "");
        ta.style.position = "fixed";
        ta.style.top = "0";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        var ok = false;
        try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
        document.body.removeChild(ta);
        if (ok) resolve(); else reject();
      });
    }

    function flash(label, text, ms) {
      label.textContent = text;
      setTimeout(function () { label.textContent = "Cite"; }, ms);
    }

    list.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest("[data-pub-cite]") : null;
      if (!btn) return;
      var text = btn.getAttribute("data-citation");
      var label = btn.querySelector("[data-pub-cite-label]");
      if (!text || !label) return;
      copyText(text).then(
        function () { flash(label, "Copied", 1600); },
        function () { flash(label, "Copy failed", 2400); }
      );
    });
  }

  /* ---- Gallery lightbox --------------------------------------------------- */
  function initGallery() {
    var items = document.querySelectorAll("[data-lightbox]");
    if (!items.length) return;

    var box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.innerHTML =
      '<button class="lightbox__close" type="button" aria-label="Close">×</button>' +
      '<figure class="lightbox__fig"><img class="lightbox__img" alt=""><figcaption class="lightbox__cap"></figcaption></figure>';
    document.body.appendChild(box);
    var img = box.querySelector(".lightbox__img");
    var cap = box.querySelector(".lightbox__cap");

    function open(src, caption) {
      img.src = src; img.alt = caption || ""; cap.textContent = caption || "";
      box.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }
    function close() {
      box.classList.remove("is-open");
      document.body.style.overflow = "";
      img.src = "";
    }
    items.forEach(function (it) {
      it.addEventListener("click", function () {
        open(it.getAttribute("data-full"), it.getAttribute("data-caption"));
      });
    });
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.closest(".lightbox__close")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && box.classList.contains("is-open")) close();
    });
  }

  /* ---- Boot --------------------------------------------------------------- */
  function boot() {
    initTheme();
    initNav();
    initTabs();
    initExpandables();
    initAccordion();
    initCarousels();
    initGallery();
    initPublications();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
