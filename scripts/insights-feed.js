/* Spencer Alexander Lawyers — dynamic insights feed
   ==================================================================
   Posts live in a Google Sheet the firm edits — publishing a post is
   adding a row (or using admin.html). No redeploy needed.

   ONE-TIME SETUP (full steps on admin.html):
   1. Create a Google Sheet with a tab named "Posts" and header row:
      slug | title | category | date | excerpt | body | published
   2. File → Share → Publish to web → select the "Posts" tab →
      "Comma-separated values (.csv)" → Publish → copy the link.
   3. Paste that link between the quotes below and upload this one file.
      After that, new rows appear on the site instantly — no redeploys.
   ================================================================== */

window.SA_INSIGHTS_FEED_URL = "";

(function () {
  "use strict";

  /* ---------- helpers (exposed for admin.html preview) ---------- */

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function slugify(s) {
    return String(s || "").toLowerCase()
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 80);
  }

  function safeHref(url) {
    var u = String(url || "").trim();
    if (/^(https?:\/\/|mailto:|tel:|\/)/i.test(u)) return u;
    if (/^[a-z0-9._-]+\.html([?#].*)?$/i.test(u)) return u;
    return "";
  }

  function inline(md) {
    var s = esc(md);
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, text, url) {
      var href = safeHref(url);
      return href ? '<a href="' + href + '">' + text + "</a>" : text;
    });
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/(^|[\s(])\*([^*\n]+)\*(?=[\s).,;:!?]|$)/g, "$1<em>$2</em>");
    return s;
  }

  /* Small, safe markdown subset: ## h2, ### h3, - lists, 1. lists,
     > blockquote, **bold**, *italic*, [text](url), blank-line paragraphs. */
  function renderMarkdown(md) {
    var blocks = String(md || "").replace(/\r\n?/g, "\n").split(/\n{2,}/);
    var out = [];
    blocks.forEach(function (block) {
      var b = block.replace(/^\n+|\n+$/g, "");
      if (!b) return;
      var lines = b.split("\n");
      if (/^###\s+/.test(b)) {
        out.push("<h3>" + inline(b.replace(/^###\s+/, "")) + "</h3>");
      } else if (/^##\s+/.test(b)) {
        out.push("<h2>" + inline(b.replace(/^##\s+/, "")) + "</h2>");
      } else if (/^#\s+/.test(b)) {
        out.push("<h2>" + inline(b.replace(/^#\s+/, "")) + "</h2>");
      } else if (lines.every(function (l) { return /^\s*[-*]\s+/.test(l); })) {
        out.push("<ul>" + lines.map(function (l) {
          return "<li>" + inline(l.replace(/^\s*[-*]\s+/, "")) + "</li>";
        }).join("") + "</ul>");
      } else if (lines.every(function (l) { return /^\s*\d+\.\s+/.test(l); })) {
        out.push("<ol>" + lines.map(function (l) {
          return "<li>" + inline(l.replace(/^\s*\d+\.\s+/, "")) + "</li>";
        }).join("") + "</ol>");
      } else if (lines.every(function (l) { return /^\s*>\s?/.test(l); })) {
        out.push("<blockquote><p>" + inline(lines.map(function (l) {
          return l.replace(/^\s*>\s?/, "");
        }).join(" ")) + "</p></blockquote>");
      } else {
        out.push("<p>" + inline(lines.join(" ")) + "</p>");
      }
    });
    return out.join("\n");
  }

  function parseCSV(text) {
    var rows = [], row = [], cell = "", inQ = false, i, c;
    text = String(text || "").replace(/\r\n?/g, "\n");
    for (i = 0; i < text.length; i++) {
      c = text[i];
      if (inQ) {
        if (c === '"') {
          if (text[i + 1] === '"') { cell += '"'; i++; } else { inQ = false; }
        } else { cell += c; }
      } else if (c === '"') { inQ = true; }
      else if (c === ",") { row.push(cell); cell = ""; }
      else if (c === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
      else { cell += c; }
    }
    if (cell !== "" || row.length) { row.push(cell); rows.push(row); }
    return rows;
  }

  function toPosts(csvText) {
    var rows = parseCSV(csvText);
    if (!rows.length) return [];
    var head = rows[0].map(function (h) { return String(h || "").trim().toLowerCase(); });
    var idx = function (name) { return head.indexOf(name); };
    var iSlug = idx("slug"), iTitle = idx("title"), iCat = idx("category"),
        iDate = idx("date"), iEx = idx("excerpt"), iBody = idx("body"), iPub = idx("published");
    if (iTitle === -1 || iBody === -1) return [];
    return rows.slice(1).map(function (r) {
      var title = (r[iTitle] || "").trim();
      return {
        slug: slugify((iSlug !== -1 && r[iSlug]) ? r[iSlug] : title),
        title: title,
        category: ((iCat !== -1 && r[iCat]) || "Insights").trim(),
        date: ((iDate !== -1 && r[iDate]) || "").trim(),
        excerpt: ((iEx !== -1 && r[iEx]) || "").trim(),
        body: (iBody !== -1 && r[iBody]) || "",
        published: iPub === -1 ? true : /^(true|yes|y|1|published)$/i.test((r[iPub] || "").trim())
      };
    }).filter(function (p) { return p.title && p.published; });
  }

  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  function formatDate(iso) {
    var m = /^(\d{4})-(\d{1,2})-(\d{1,2})/.exec(String(iso || "").trim());
    if (!m) return String(iso || "").trim();
    return parseInt(m[3], 10) + " " + MONTHS[parseInt(m[2], 10) - 1] + " " + m[1];
  }

  function dateValue(iso) {
    var t = Date.parse(String(iso || "").trim());
    return isNaN(t) ? 0 : t;
  }

  function readMinutes(body) {
    var words = String(body || "").split(/\s+/).filter(Boolean).length;
    return Math.max(2, Math.round(words / 200));
  }

  function categoryLook(cat) {
    var c = String(cat || "").toLowerCase();
    var base = "https://images.unsplash.com/photo-";
    var q = "?q=80&w=800&h=500&auto=format&fit=crop";
    if (c.indexOf("family") !== -1) return { img: base + "1609220136736-443140cffec6" + q + "&crop=faces", chip: "post-cat" };
    if (c.indexOf("wills") !== -1 || c.indexOf("estate") !== -1) return { img: base + "1584515933487-779824d29309" + q + "&crop=entropy", chip: "post-cat" };
    if (c.indexOf("commercial") !== -1 || c.indexOf("business") !== -1) return { img: base + "1517048676732-d65bc937f952" + q, chip: "post-cat" };
    return { img: base + "1454165804606-c3d57bc86b40" + q, chip: "post-cat" };
  }

  function yearOf(iso) {
    var m = /(\d{4})/.exec(String(iso || ""));
    return m ? m[1] : "2026";
  }

  window.SAInsights = {
    renderMarkdown: renderMarkdown,
    slugify: slugify,
    formatDate: formatDate,
    esc: esc
  };

  /* ---------- feed rendering ---------- */

  var FEED_URL = String(window.SA_INSIGHTS_FEED_URL || "").trim();
  var grid = document.querySelector("[data-insights-grid]");
  var postPage = document.querySelector("[data-post-page]");
  if (!FEED_URL || (!grid && !postPage)) {
    if (postPage && !FEED_URL) showPostError("This article isn't available yet.", "The insights feed hasn't been connected. Browse our published insights instead.");
    return;
  }

  fetch(FEED_URL, { cache: "no-store" })
    .then(function (r) { if (!r.ok) throw new Error("Feed request failed"); return r.text(); })
    .then(function (text) {
      var posts = toPosts(text).sort(function (a, b) { return dateValue(b.date) - dateValue(a.date); });
      if (grid) renderCards(posts);
      if (postPage) renderPost(posts);
    })
    .catch(function () {
      if (postPage) showPostError("We couldn't load this article.", "Please try again in a moment, or browse our published insights.");
    });

  function renderCards(posts) {
    var frag = document.createDocumentFragment();
    posts.forEach(function (p) {
      var look = categoryLook(p.category);
      var a = document.createElement("a");
      a.className = "post-card";
      a.href = "post.html?post=" + encodeURIComponent(p.slug);

      var media = document.createElement("div");
      media.className = "post-card__media post-card__media--photo";
      var photo = document.createElement("img");
      photo.src = look.img;
      photo.alt = "";
      photo.loading = "lazy";
      photo.width = 800; photo.height = 500;
      var chip = document.createElement("span");
      chip.className = look.chip;
      chip.textContent = p.category;
      media.appendChild(photo); media.appendChild(chip);

      var body = document.createElement("div");
      body.className = "post-card__body";
      var h = document.createElement("h3");
      h.className = "post-card__title";
      h.textContent = p.title;
      var ex = document.createElement("p");
      ex.className = "post-card__excerpt";
      ex.textContent = p.excerpt;
      var meta = document.createElement("span");
      meta.className = "post-card__meta";
      meta.textContent = (p.date ? yearOf(p.date) + " · " : "") + readMinutes(p.body) + " min read";
      body.appendChild(h); body.appendChild(ex); body.appendChild(meta);

      a.appendChild(media); a.appendChild(body);
      frag.appendChild(a);
    });
    grid.insertBefore(frag, grid.firstChild);
  }

  function renderPost(posts) {
    var params = new URLSearchParams(window.location.search);
    var slug = slugify(params.get("post") || "");
    var post = null;
    posts.forEach(function (p) { if (!post && p.slug === slug) post = p; });
    if (!post) { showPostError("Article not found", "This article may have been moved or unpublished. Browse our published insights instead."); return; }

    document.title = post.title + " | Spencer Alexander Lawyers";
    setMeta("description", post.excerpt || post.title);
    var canon = document.querySelector('link[rel="canonical"]');
    if (canon) canon.setAttribute("href", "https://www.spenceralexander.com.au/post.html?post=" + encodeURIComponent(post.slug));

    setText("[data-post-title]", post.title);
    setText("[data-post-crumb]", post.title);
    setText("[data-post-category]", post.category);
    setText("[data-post-meta]", (post.date ? yearOf(post.date) + " · " : "") + readMinutes(post.body) + " min read");
    var bodyEl = document.querySelector("[data-post-body]");
    if (bodyEl) bodyEl.innerHTML = renderMarkdown(post.body);
    var loading = document.querySelector("[data-post-loading]");
    if (loading) loading.remove();
    var shell = document.querySelector("[data-post-shell]");
    if (shell) shell.hidden = false;

    var ld = {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": post.title,
      "datePublished": post.date || undefined,
      "articleSection": post.category,
      "author": { "@type": "Person", "name": "Spencer Alexander" },
      "publisher": { "@type": "LegalService", "name": "Spencer Alexander Lawyers", "telephone": "+61-3-9001-4400" },
      "description": post.excerpt || post.title,
      "mainEntityOfPage": "https://www.spenceralexander.com.au/post.html?post=" + encodeURIComponent(post.slug)
    };
    var s = document.createElement("script");
    s.type = "application/ld+json";
    s.textContent = JSON.stringify(ld);
    document.head.appendChild(s);
  }

  function showPostError(title, message) {
    var loading = document.querySelector("[data-post-loading]");
    if (loading) loading.remove();
    setText("[data-post-title]", title);
    setText("[data-post-crumb]", "Insight");
    setText("[data-post-category]", "Insights");
    setText("[data-post-meta]", "");
    var bodyEl = document.querySelector("[data-post-body]");
    if (bodyEl) bodyEl.innerHTML = "<p>" + esc(message) + ' <a href="insights.html">All insights</a>.</p>';
    var shell = document.querySelector("[data-post-shell]");
    if (shell) shell.hidden = false;
  }

  function setText(sel, text) {
    var el = document.querySelector(sel);
    if (el) el.textContent = text;
  }

  function setMeta(name, content) {
    var el = document.querySelector('meta[name="' + name + '"]');
    if (!el) { el = document.createElement("meta"); el.setAttribute("name", name); document.head.appendChild(el); }
    el.setAttribute("content", content);
  }
})();
