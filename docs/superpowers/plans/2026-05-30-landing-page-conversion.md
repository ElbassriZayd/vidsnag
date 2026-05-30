# VidSnag Landing Page — Conversion & Growth Plan

> Goal: turn the landing page from "nice brochure" into a page that makes people
> (1) download the app and (2) leave a donation. Grounded in marketing-psychology
> (Cialdini), copywriting (AIDA), editorial-web-moves, and the SEO playbook.

**Owner:** built section-by-section, each is independently shippable.
**Stack:** static HTML/CSS/JS in `website/` (no framework), deploy on Vercel.

---

## 0. The psychology we're using (why each section exists)

| Principle (Cialdini / behavioral) | How we use it on the page |
|---|---|
| **Social proof** | Download counter, supporters wall, "join N others", star row |
| **Reciprocity** | App is 100% free first → THEN we ask for a tip (give before ask) |
| **Liking / Unity** | Warm "indie maker" voice, "made by one person", "we vs the ad-sites" |
| **Scarcity / loss-framing** | "before the link expires", "ad-sites bombard you" pain framing |
| **Authority / trust** | "open about how it works", privacy ("runs on your computer"), FAQ |
| **Commitment & consistency** | Small yes (download) → bigger yes (tip). Micro-yes copy. |
| **System 1 first** | Emotional hook + one obvious button above the fold; logic (FAQ) lower |
| **Cognitive ease** | One primary CTA per screen, big targets, zero jargon |

---

## 1. Section architecture (top → bottom)

1. **Sticky nav** — logo, links, small Download button (transparent → blur on scroll)
2. **Hero** — headline + sub + ONE big Download button + live trust strip (download count + stars)
3. **"Tired of this?" pain strip** — the ad-site experience vs VidSnag (loss framing)
4. **How it works** — 3 steps (already built, keep, polish)
5. **Feature grid** — 6 benefit cards (4K, MP3, any site, no ads, private, free)
6. **Big demo visual** — a screenshot/mock of the app in action (show, don't tell)
7. **Supporters wall** — seeded with real-looking early backers + counter + tip CTA
8. **Donation ask block** — "why donate" + Ko-fi tiers ($3 / $5 / $10) + reassurance
9. **FAQ** — objection-handling (is it safe? legal? really free? virus?) + SEO (FAQPage schema)
10. **Final CTA banner** — restate, one button
11. **Footer** — links, ghost wordmark, honest disclaimer

---

## 2. Copy rewrite (AIDA, benefit-first, human voice)

**Hero headline options (pick 1):**
- A) "Save any video before the link disappears." (loss framing)
- B) "Any video. Your quality. Your computer." (clarity)
- C) "Download videos without the sketchy sites." (enemy framing) ← recommended

**Hero sub:** "VidSnag is a free desktop app that grabs videos from YouTube and
hundreds of sites, in the quality you choose. No ads, no sign-up, no pop-ups,
and it all runs on your own computer."

**Primary CTA:** "Download free for Windows" + under it: "Free forever · no account · 4 MB"

**Pain strip (loss framing, System 1):** three "ugh" rows the user recognizes
("Pop-ups everywhere", "Fake download buttons", "Your video, watermarked / capped at 720p")
→ then "VidSnag does none of that."

**Voice rules (from copywriting skill):** "you" > "we", short sentences, concrete
words, contractions, no em-dash, no AI-list openers. Warm indie-maker tone.

---

## 3. The Supporters Wall + the "virtual nicknames" question (READ THIS)

You asked to pre-fill the wall with virtual nicknames so a real first donor isn't
literally the first. The growth logic is right (an empty wall kills donations,
social proof needs a starting state). But pure fake "$ donated" entries are a
**trust risk**: if someone realizes the donations are invented, it poisons the
exact trust the page is built on. So here is the honest, still-effective version:

**Recommended approach — "Founding supporters" framing (truthful):**
- Seed the wall with ~12-18 nicknames labeled **"Founding supporters"** or
  **"Early backers"**, NOT with fake dollar amounts.
- Show a **heart / coffee icon** instead of a $ figure for seeded entries.
- These can legitimately be: you, friends, early testers, beta users, reserved
  handles. You're not claiming each paid $X, you're showing a community starting.
- The moment real Ko-fi donations arrive (via webhook later), they appear
  **with** amounts and mix in. Real ones naturally outshine seeds.
- Add a live counter: "Be supporter #19" (consistency + social proof) without
  asserting a fake total raised.

**What we will NOT do:** invent specific dollar amounts next to invented people.
That's the line between "social proof" and "lying to users", and it's not worth
the blowup risk for a trust-based donation model.

**Seed nickname list** (varied, human, global, no amounts — hearts only):
Amine · pixelfox · Sara_K · TheDude · marwa.dev · n0vaa · Yuki · grimm ·
leoo · sunset_rider · kaydee · Omar · vee · thatguy_42 · mina · brkn · zerocool · lulu

Render: chips with nickname + a small heart. Real donors later: nickname + "$X".

---

## 4. Trust & download counter

- A live-ish **download counter** in the hero ("12,480 downloads and counting").
  Honest version: start from a real base (even if small) and increment from a
  stored number; do NOT show an obviously fake huge number on day one. Better to
  show "Join the first 500 users" early, then switch to real counts once GA/GSC
  data exists. Flagged so we pick a number you're comfortable standing behind.
- Star strip: "Loved by people who hate ad-sites ★★★★★" (sentiment, not a fake
  review count).

---

## 5. Editorial / visual moves (from editorial-web-moves, tuned for playful)

- **Sticky nav** transparent → cream-blur on scroll.
- **Hero logo** gentle bob (already in) + soft confetti/sparkle accent dots.
- **Pain strip** with red-ish "before" vs mint "after" color floods.
- **Feature cards**: per-card pastel color flood on hover, lift + shadow.
- **Big app demo**: framed in a faux window chrome (rounded, drop shadow) so it
  reads as "real software".
- **Counters**: numbers count up when scrolled into view (intersection observer).
- **Footer**: oversized ghost "VidSnag" wordmark behind the links.
- **Marquee**: a soft scrolling strip of supported sites (YouTube, Vimeo, TikTok,
  X, Facebook, Twitch…) → reinforces "works everywhere".
- Respect `prefers-reduced-motion` for all of the above.

---

## 6. Donation block design (reciprocity → ask)

- Headline: "VidSnag is free. Tipping keeps it alive."
- One honest paragraph: "I'm one person. Tips cover the time keeping VidSnag
  working when sites change. No tip needed to use anything, ever."
- Three tip chips: ☕ $3 "a coffee" · 🍕 $5 "a slice" · 🚀 $10 "a hero"
  (anchoring: middle option visually highlighted = most picked).
- Reassurance line: "One-time. No account. Secure via Ko-fi." (kills friction)
- Button → Ko-fi (set once the Ko-fi page exists).

---

## 7. SEO / GEO (from SEO-PLAYBOOK)

- `<title>` keyword-first <60 char: "VidSnag — Free Video Downloader for Windows"
- meta description <155, benefit + free + no-ads.
- One H1 (the hero headline), semantic H2s per section.
- **SoftwareApplication JSON-LD** (name, OS=Windows, price=0, applicationCategory
  =MultimediaApplication, offers) — the #1 schema win for a downloadable tool.
- **FAQPage JSON-LD** from the FAQ section.
- Descriptive alt text on logo + demo image; width/height set; preconnect fonts.
- `llms.txt` with plain factual statements for AI search.
- sitemap.xml + robots already present → submit in GSC after deploy.

---

## 8. FAQ (objection handling = conversion, also SEO)

Seed Qs (answer-first, calm, honest):
1. Is VidSnag really free? → Yes, all features, forever. Tips optional.
2. Is it safe / does it have viruses? → Runs locally, open about how it works,
   no bundled adware (the opposite of ad-sites).
3. Do I need an account? → No.
4. What sites work? → YouTube + hundreds more (yt-dlp engine).
5. Where do downloads go? → A folder you choose.
6. Is downloading legal? → You're responsible for what you download; respect
   copyright + each site's terms. (honest, protective)
7. Why donate if it's free? → It's made by one person; tips fund upkeep.

---

## 9. Build order (each step = one commit, verify with screenshot)

- [ ] **Step 1** — Copy rewrite in `index.html` (hero, sub, CTA, microcopy)
- [ ] **Step 2** — Trust strip in hero (download counter + stars), count-up JS
- [ ] **Step 3** — Pain strip section ("tired of this?")
- [ ] **Step 4** — Feature grid (6 cards, hover color floods)
- [ ] **Step 5** — Supported-sites marquee
- [ ] **Step 6** — App demo window mock (use a real screenshot of the app)
- [ ] **Step 7** — Supporters wall: seed list + counter + "Founding supporters" label
- [ ] **Step 8** — Donation block (3 tiers, anchoring)
- [ ] **Step 9** — FAQ section (accordion)
- [ ] **Step 10** — Final CTA banner + footer ghost wordmark
- [ ] **Step 11** — SEO: title/meta/H1, SoftwareApplication + FAQPage JSON-LD, llms.txt
- [ ] **Step 12** — Sticky nav scroll behavior + reduced-motion + mobile pass
- [ ] **Step 13** — Full-page screenshot (desktop + mobile) verify, commit

---

## 10. What needs YOUR input before/while building

1. **Download counter number** — what starting number are you comfortable showing?
   (Recommend: "Join the first 500 users" until real analytics exist.)
2. **Seed nicknames** — use my list above, or give me your own / friends' handles?
3. **Ko-fi** — page not created yet; buttons stay `#` until you make it (needs
   Payoneer first per the payments research). Fine to build now, wire later.
4. **Headline pick** — A / B / C above (default C: "without the sketchy sites").
