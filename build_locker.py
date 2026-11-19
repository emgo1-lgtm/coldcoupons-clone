"""Build standalone AdBlueMedia Content Locker styled to match ColdCoupons.com."""
import base64, pathlib

OUT = pathlib.Path(__file__).parent
logo_b64 = base64.b64encode(
    (OUT / "assets_mirror/public/assets/uploads/logo_darks/logo_dark_67fd5c00e3f9e.png").read_bytes()
).decode()
logo_uri = f"data:image/png;base64,{logo_b64}"

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Unlock Your Code | ColdCoupons</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap" rel="stylesheet" />

  <!-- =========================================================
       ADBLUEMEDIA CUSTOM LOCKER CSS
       (Copy everything inside <style> into AdBlueMedia CSS tab)
       ========================================================= -->
  <style>
    :root {{
      --cc-text: #2b3845;
      --cc-text-second: #5d7185;
      --cc-text-third: #8fa3b7;
      --cc-bg: #f8fbfd;
      --cc-bg-secondary: #f0f7fc;
      --cc-card: #ffffff;
      --cc-primary: #0088cc;
      --cc-accent: #01c0ff;
      --cc-accent-soft: #dff6ff;
      --cc-border: #e3eef6;
      --cc-success: #4bb543;
      --cc-radius: 1rem;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: "Lexend", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 15% 15%, rgba(1, 192, 255, 0.12), transparent 45%),
        radial-gradient(circle at 85% 85%, rgba(0, 136, 204, 0.10), transparent 45%),
        var(--cc-bg);
      color: var(--cc-text);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      -webkit-font-smoothing: antialiased;
    }}

    .cc-locker-backdrop {{
      width: 100%;
      max-width: 500px;
    }}

    .cc-locker-card {{
      background: var(--cc-card);
      border: 1px solid var(--cc-border);
      border-radius: 1.25rem;
      box-shadow: 0 20px 50px rgba(24, 58, 90, 0.12);
      overflow: hidden;
      animation: ccFadeUp 0.35s ease-out;
    }}

    @keyframes ccFadeUp {{
      from {{ opacity: 0; transform: translateY(14px) scale(0.98); }}
      to   {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    /* Header matching ColdCoupons navbar + modal top */
    .cc-locker-header {{
      background: linear-gradient(135deg, #0d2236 0%, #163654 60%, #0b4a73 100%);
      padding: 22px 24px 20px;
      color: #ffffff;
      position: relative;
      overflow: hidden;
    }}

    .cc-locker-header::after {{
      content: "";
      position: absolute;
      inset: 0;
      background-image: radial-gradient(rgba(1, 192, 255, 0.22) 1px, transparent 1px);
      background-size: 16px 16px;
      opacity: 0.35;
      pointer-events: none;
    }}

    .cc-header-top {{
      position: relative;
      z-index: 1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
    }}

    .cc-logo-wrap {{
      display: inline-flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.96);
      padding: 6px 12px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
    }}

    .cc-logo {{
      height: 24px;
      width: auto;
      display: block;
    }}

    .cc-badges {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .cc-pill {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 11.5px;
      font-weight: 500;
      padding: 5px 10px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.14);
      backdrop-filter: blur(6px);
      color: #ffffff;
      border: 1px solid rgba(255, 255, 255, 0.18);
    }}

    .cc-pill-verified svg {{
      color: #6ee768;
    }}

    .cc-title {{
      position: relative;
      z-index: 1;
      font-size: 20px;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 4px;
      letter-spacing: -0.01em;
    }}

    .cc-subtitle {{
      position: relative;
      z-index: 1;
      font-size: 13px;
      color: rgba(255, 255, 255, 0.8);
      font-weight: 400;
    }}

    /* Body */
    .cc-locker-body {{
      padding: 22px 24px 20px;
    }}

    /* ColdCoupons signature notched coupon ticket */
    .cc-ticket {{
      position: relative;
      background: var(--cc-accent-soft);
      border: 1.5px dashed rgba(1, 192, 255, 0.55);
      border-radius: 1rem;
      padding: 16px 22px;
      text-align: center;
      margin-bottom: 18px;
    }}

    .cc-ticket::before,
    .cc-ticket::after {{
      content: "";
      position: absolute;
      top: 50%;
      width: 18px;
      height: 18px;
      background: var(--cc-card);
      border-radius: 50%;
      transform: translateY(-50%);
    }}

    .cc-ticket::before {{
      left: -10px;
      border-right: 1.5px dashed rgba(1, 192, 255, 0.55);
    }}

    .cc-ticket::after {{
      right: -10px;
      border-left: 1.5px dashed rgba(1, 192, 255, 0.55);
    }}

    .cc-ticket-label {{
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--cc-primary);
      margin-bottom: 6px;
    }}

    .cc-code-preview {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #ffffff;
      border: 1px dashed var(--cc-accent);
      border-radius: 10px;
      padding: 8px 16px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 16px;
      font-weight: 700;
      color: var(--cc-text);
      letter-spacing: 0.08em;
    }}

    .cc-code-blur {{
      filter: blur(4.5px);
      user-select: none;
      color: var(--cc-primary);
    }}

    .cc-step-note {{
      font-size: 13.5px;
      color: var(--cc-text-second);
      text-align: center;
      line-height: 1.5;
      margin-bottom: 16px;
    }}

    .cc-step-note strong {{
      color: var(--cc-text);
      font-weight: 600;
    }}

    /* Offers list container (AdBlueMedia injects offers here) */
    .cc-offers-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 18px;
    }}

    .cc-offer-btn {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      width: 100%;
      text-decoration: none;
      background: var(--cc-bg-secondary);
      border: 1.5px solid var(--cc-border);
      border-radius: 12px;
      padding: 13px 15px;
      color: var(--cc-text);
      transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease, background 0.16s ease;
      cursor: pointer;
    }}

    .cc-offer-btn:hover {{
      transform: translateY(-2px);
      border-color: var(--cc-accent);
      background: #ffffff;
      box-shadow: 0 8px 20px rgba(1, 192, 255, 0.16);
    }}

    .cc-offer-left {{
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }}

    .cc-offer-num {{
      flex-shrink: 0;
      width: 30px;
      height: 30px;
      border-radius: 9px;
      background: var(--cc-accent);
      color: #ffffff;
      font-weight: 700;
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 10px rgba(1, 192, 255, 0.35);
    }}

    .cc-offer-info {{
      min-width: 0;
      text-align: left;
    }}

    .cc-offer-name {{
      font-size: 14px;
      font-weight: 600;
      color: var(--cc-text);
      line-height: 1.3;
      margin-bottom: 2px;
    }}

    .cc-offer-desc {{
      font-size: 12px;
      color: var(--cc-text-second);
      line-height: 1.35;
    }}

    .cc-offer-cta {{
      flex-shrink: 0;
      background: var(--cc-accent);
      color: #ffffff;
      font-size: 12px;
      font-weight: 600;
      padding: 7px 13px;
      border-radius: 8px;
      white-space: nowrap;
      transition: background 0.16s ease;
    }}

    .cc-offer-btn:hover .cc-offer-cta {{
      background: var(--cc-primary);
    }}

    /* Waiting status bar */
    .cc-status-bar {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 9px;
      background: var(--cc-bg);
      border: 1px solid var(--cc-border);
      border-radius: 10px;
      padding: 10px 14px;
      font-size: 12.5px;
      color: var(--cc-text-second);
      font-weight: 500;
    }}

    .cc-pulse-dot {{
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: var(--cc-accent);
      position: relative;
    }}

    .cc-pulse-dot::after {{
      content: "";
      position: absolute;
      inset: -4px;
      border-radius: 50%;
      border: 2px solid var(--cc-accent);
      animation: ccPulse 1.5s infinite ease-out;
    }}

    @keyframes ccPulse {{
      0%   {{ transform: scale(0.7); opacity: 0.9; }}
      100% {{ transform: scale(1.8); opacity: 0; }}
    }}

    /* Footer trust row matching ColdCoupons footer */
    .cc-locker-footer {{
      border-top: 1px solid var(--cc-border);
      background: var(--cc-bg);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
      font-size: 11.5px;
      color: var(--cc-text-third);
    }}

    .cc-trust-item {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}

    .cc-trust-item svg {{
      color: var(--cc-accent);
    }}

    @media (max-width: 480px) {{
      .cc-locker-header, .cc-locker-body {{ padding: 18px; }}
      .cc-offer-btn {{ padding: 11px 12px; }}
      .cc-offer-cta {{ padding: 6px 10px; font-size: 11.5px; }}
    }}
  </style>
</head>
<body>

  <!-- =========================================================
       ADBLUEMEDIA CUSTOM LOCKER HTML
       (Copy inside AdBlueMedia HTML tab; supports {{offers}} or JS feed)
       ========================================================= -->
  <div class="cc-locker-backdrop">
    <div class="cc-locker-card">

      <!-- Header with ColdCoupons Logo -->
      <div class="cc-locker-header">
        <div class="cc-header-top">
          <div class="cc-logo-wrap">
            <img class="cc-logo" src="{logo_uri}" alt="ColdCoupons Logo" />
          </div>
          <div class="cc-badges">
            <span class="cc-pill cc-pill-verified">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              Verified
            </span>
            <span class="cc-pill" id="cc-left-pill">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/></svg>
              <span id="cc-coupons-left">184</span> left
            </span>
          </div>
        </div>
        <h1 class="cc-title" id="cc-locker-title">Human Verification Required</h1>
        <p class="cc-subtitle">Instant automatic unlock right after completion</p>
      </div>

      <!-- Body -->
      <div class="cc-locker-body">
        <!-- ColdCoupons Ticket Box -->
        <div class="cc-ticket">
          <div class="cc-ticket-label" id="cc-ticket-label">Your Reserved Code</div>
          <div class="cc-code-preview">
            <span class="cc-code-blur">X9K4-M7Q2-</span><span id="cc-code-tail">8F2N</span>
          </div>
        </div>

        <p class="cc-step-note">
          Complete <strong>1 quick free offer</strong> below to verify you're human and reveal your full code immediately.
        </p>

        <!-- AdBlueMedia Offer List Container -->
        <div class="cc-offers-list" id="offerContainer">
          <!-- AdBlueMedia live offers populate here automatically -->
        </div>

        <!-- Waiting Status -->
        <div class="cc-status-bar">
          <span class="cc-pulse-dot"></span>
          <span id="cc-status-text">Waiting for offer completion...</span>
        </div>
      </div>

      <!-- Footer -->
      <div class="cc-locker-footer">
        <span class="cc-trust-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          100% Free &amp; Verified
        </span>
        <span class="cc-trust-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          Instant Unlock
        </span>
        <span>&copy; 2026 ColdCoupons</span>
      </div>
    </div>
  </div>

  <!-- =========================================================
       ADBLUEMEDIA INTEGRATION SCRIPT
       Replace YOUR_IT_ID and YOUR_KEY with your AdBlueMedia
       Locker credentials from the AdBlueMedia dashboard.
       ========================================================= -->
  <script>
    const ADBLUE_CONFIG = {{
      it: "YOUR_IT_ID",       // <-- Replace with your AdBlueMedia `it` (numeric ID)
      key: "YOUR_KEY",        // <-- Replace with your AdBlueMedia `key`
      maxOffers: 4            // Number of offers to display
    }};

    // Optional: read ?title=...&tail=... from URL so each coupon can personalize the locker
    (function applyQueryParams() {{
      const params = new URLSearchParams(window.location.search);
      const title = params.get("title");
      const tail = params.get("tail");
      if (title) {{
        document.getElementById("cc-ticket-label").textContent = title;
      }}
      if (tail) {{
        document.getElementById("cc-code-tail").textContent = tail.slice(-4).toUpperCase();
      }}
    }})();

    function renderOffers(offers) {{
      const container = document.getElementById("offerContainer");
      container.innerHTML = offers.slice(0, ADBLUE_CONFIG.maxOffers).map((offer, i) => `
        <a class="cc-offer-btn" href="${{offer.url}}" target="_blank" rel="noopener noreferrer" onclick="onOfferClick()">
          <div class="cc-offer-left">
            <span class="cc-offer-num">${{i + 1}}</span>
            <div class="cc-offer-info">
              <div class="cc-offer-name">${{offer.anchor || offer.name}}</div>
              <div class="cc-offer-desc">${{offer.conversion || offer.description || "Complete this free step to unlock"}}</div>
            </div>
          </div>
          <span class="cc-offer-cta">Free</span>
        </a>
      `).join("");
    }}

    function onOfferClick() {{
      document.getElementById("cc-status-text").textContent = "Checking completion... Keep this tab open";
    }}

    // Load live AdBlueMedia JSONP offer feed when credentials are configured,
    // otherwise show styled preview offers so you can test the design locally.
    (function loadAdBlueMediaOffers() {{
      const isConfigured = ADBLUE_CONFIG.it !== "YOUR_IT_ID" && ADBLUE_CONFIG.key !== "YOUR_KEY";

      if (!isConfigured) {{
        renderOffers([
          {{
            name: "Download & Open Opera GX Browser",
            description: "Install and run for 30 seconds to verify",
            url: "#configure-adbluemedia-id"
          }},
          {{
            name: "Enter Your Email for a \$100 Gift Card",
            description: "Submit a valid email on the next page",
            url: "#configure-adbluemedia-id"
          }},
          {{
            name: "Quick 2-Question Rewards Survey",
            description: "Complete the short survey to unlock instantly",
            url: "#configure-adbluemedia-id"
          }}
        ]);
        return;
      }}

      // AdBlueMedia JSONP Feed Loader
      window.adBlueCallback = function (offers) {{
        if (Array.isArray(offers) && offers.length > 0) {{
          renderOffers(offers);
        }} else {{
          document.getElementById("offerContainer").innerHTML =
            '<div class="cc-status-bar">No offers currently available for your region. Please try again shortly.</div>';
        }}
      }};

      const script = document.createElement("script");
      script.src =
        "https://d2xohqmdyl2cj3.cloudfront.net/public/offers/feed.php" +
        "?user_id=" + encodeURIComponent(ADBLUE_CONFIG.it) +
        "&api_key=" + encodeURIComponent(ADBLUE_CONFIG.key) +
        "&s1=&s2=&callback=adBlueCallback";
      document.body.appendChild(script);
    }})();
  </script>
</body>
</html>
'''

(OUT / "adbluemedia-locker.html").write_text(html, encoding="utf-8")
print("Wrote adbluemedia-locker.html,", len(html), "bytes")
