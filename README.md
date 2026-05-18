# MaticDrop — Free MATIC Faucet (Master Template)

## Faucet Clone Army — 5x Deploy

This is the master template. Deploy × 5 Render services, each with its own Adsterra account.

## Revenue Layers (all 6 wired)
1. **Adsterra display ads** — replace `[AD BANNER]` / `[AD SLOT]` placeholders with Adsterra zone scripts
2. **Offer walls** — wire Cointiply / AdGateMedia iframe or API into offer-item hrefs
3. **PTC links** — replace `href="#"` on ptc-card anchors with your PTC network URLs
4. **Shortlinks** — replace `href="#"` on sl-btn anchors with AdFly / Linkvertise / ShrinkMe links
5. **Referral signups** — replace `href="#"` in referral-grid with your referral URLs
6. **Survey wall** — wire CPAGrip / OGAds into the survey offer-item href

## Wiring Checklist (per clone)
- [ ] Create Adsterra account → get zone ID → replace 3 ad slot placeholders
- [ ] Wire offer wall (Cointiply embed or AdGateMedia widget)
- [ ] Wire 10 PTC links
- [ ] Wire 20 shortlinks (AdFly / Linkvertise)
- [ ] Wire referral URLs (Coinbase, Binance, Cointiply, AdGateMedia)
- [ ] Wire 2captcha in captcha-slot div
- [ ] Connect backend payout (MATIC drip — needs ~$5 seed)

## Deploy to Render
1. Push this repo to GitHub
2. Create Render Static Site → point to repo
3. No build command needed — pure static HTML
4. Clone Render service × 4 more → rename each (maticdrop-2, maticdrop-3, etc.)

## CloakBrowser Automation
- 1,000 unique fingerprints
- Rotates across all 5 faucet URLs
- Auto-solves captchas via 2captcha API key
- Hits all 6 revenue layers per visit cycle
