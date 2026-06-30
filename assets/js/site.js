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

  /* ---- Accordion (alumni) ------------------------------------------------- */
  function initAccordion() {
    document.querySelectorAll(".accordion__header").forEach(function (header) {
      header.addEventListener("click", function () {
        var item = header.closest(".accordion__item");
        var panel = item.querySelector(".accordion__panel");
        var open = header.getAttribute("aria-expanded") !== "true";
        header.setAttribute("aria-expanded", open ? "true" : "false");
        setPanel(panel, open);
      });
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

  /* ---- Publications, fetched live from ORCID ------------------------------
     The list is always current: it reads the PI's public ORCID record at load
     time, groups by year, and links each entry to its DOI. If ORCID can't be
     reached, it falls back to a link to the ORCID profile. */
  function initPublications() {
    var root = document.querySelector("[data-orcid]");
    if (!root) return;
    var id = root.getAttribute("data-orcid");
    var listEl = root.querySelector("[data-pub-list]");
    var countEl = root.querySelector("[data-pub-count]");
    var statusEl = root.querySelector("[data-pub-status]");

    function esc(s) { var d = document.createElement("div"); d.textContent = s == null ? "" : s; return d.innerHTML; }
    function typeLabel(t) {
      t = (t || "").toLowerCase();
      if (t.indexOf("conference") >= 0) return { label: "Conference", cls: "badge--blue" };
      if (t.indexOf("book") >= 0) return { label: "Book", cls: "badge--purple" };
      if (t.indexOf("journal") >= 0) return { label: "Journal", cls: "badge--green" };
      if (!t) return { label: "Other", cls: "badge--grey" };
      return { label: t.replace(/-/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); }), cls: "badge--grey" };
    }
    function renderPub(w) {
      var t = typeLabel(w.type);
      var venue = w.journal ? '<div class="pub-item__venue">' + esc(w.journal) + "</div>" : "";
      var link = w.url
        ? '<a class="btn btn--sm btn--ghost" href="' + esc(w.url) + '" target="_blank" rel="noopener"><i class="fa-solid fa-up-right-from-square" aria-hidden="true"></i>View</a>'
        : "";
      return '<div class="pub-item"><div class="pub-item__title">' + esc(w.title) + "</div>" + venue +
        '<div class="pub-item__actions"><span class="badge ' + t.cls + ' badge--subtle">' + t.label + "</span>" + link + "</div></div>";
    }

    fetch("https://pub.orcid.org/v3.0/" + id + "/works", { headers: { Accept: "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (data) {
        var works = (data.group || []).map(function (g) {
          var s = (g["work-summary"] || [])[0];
          if (!s) return null;
          var pd = s["publication-date"] || {};
          var doiUrl = "";
          var ids = (s["external-ids"] && s["external-ids"]["external-id"]) || [];
          ids.forEach(function (x) {
            if (x["external-id-type"] === "doi") {
              doiUrl = (x["external-id-url"] && x["external-id-url"].value) || ("https://doi.org/" + x["external-id-value"]);
            }
          });
          if (!doiUrl && ids[0] && ids[0]["external-id-url"]) doiUrl = ids[0]["external-id-url"].value;
          return {
            title: s.title && s.title.title ? s.title.title.value : "Untitled",
            journal: s["journal-title"] ? s["journal-title"].value : "",
            year: pd.year ? pd.year.value : "",
            month: pd.month ? parseInt(pd.month.value, 10) : 0,
            type: s.type || "",
            url: doiUrl
          };
        }).filter(Boolean);

        works.sort(function (a, b) {
          var d = (parseInt(b.year || "0", 10)) - (parseInt(a.year || "0", 10));
          return d !== 0 ? d : (b.month - a.month);
        });

        if (!works.length) { if (statusEl) statusEl.textContent = "No publications found."; return; }
        var html = "", lastYear = null;
        works.forEach(function (w) {
          var yr = w.year || "Undated";
          if (yr !== lastYear) { html += '<div class="pub-year">' + esc(yr) + "</div>"; lastYear = yr; }
          html += renderPub(w);
        });
        listEl.innerHTML = html;
        if (countEl) countEl.textContent = works.length + (works.length === 1 ? " publication" : " publications");
      })
      .catch(function () {
        if (statusEl) statusEl.innerHTML = 'Could not load publications automatically. View the full list on <a href="https://orcid.org/' + id + '" target="_blank" rel="noopener">ORCID</a>.';
        if (countEl) countEl.textContent = "";
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
