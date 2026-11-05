# REFORGE | Circular Materials Innovation Lab

I built REFORGE after reading NCC Industry's Product Developer role. I wanted to explore the full product-development conversation: understanding a customer brief, designing a circular material concept, reviewing lab evidence, weighing commercial and environmental tradeoffs, and documenting a decision that colleagues can challenge.

This is a **fictional portfolio demonstration**, not an NCC product, certified asphalt mix-design tool, or materials-engineering recommendation.

## Launch in one click

Open `index.html` in a modern browser. No server, package installation, login, or API key is required. Internet is optional; the only external resource is a Google Fonts stylesheet, with system-font fallback.

## Explore

1. **Innovation overview:** see portfolio readiness and product-development pathway.
2. **Material tradeoff lab:** adjust RAP content, binder fraction, transport and energy cost; see indicative cost, modeled carbon proxy and customer-brief checks recalculate.
3. **Customer discovery:** choose a fictional customer brief and record needs or open questions.
4. **Quality & testing:** inspect fictional laboratory measurements, missing-field validation and acceptance thresholds.
5. **Product portfolio:** compare three candidate concepts and export CSV for Excel.
6. **Decision gate:** document a recommendation, responsible function and rationale.
7. **Review package:** export a review memo and structured JSON including calculations and limitations.

Notes, gate decisions and the current what-if scenario are stored in browser localStorage. No information is transmitted to a server. Browser data can be cleared using browser site-data controls.

## Tests

With Node.js 18+: `node --test tests/engine.test.js`. The application itself does not need Node.

## Technical limitations

- All company, customer, laboratory and product data are invented.
- Illustrative mix composition is RAP + binder + remaining virgin aggregate by mass; this simplifies real mix design.
- Cost uses simple material, transport and energy components in SEK per tonne; it is not a supplier quote.
- The carbon proxy uses arbitrary factors, not verified EPDs, ISO-compliant LCA or lifecycle inventory data. Do not interpret the output as real emissions.
- Lab readings are fixed fictional observations. Changing a slider does **not** predict how real physical properties change; it only changes cost, composition and the carbon proxy. A changed formulation needs new lab tests.
- Acceptance thresholds are fictional customer-brief screening criteria, **not** EN/SS-EN asphalt compliance or product certification.
- Stage-gate recommendations are exploratory and do not authorize production, road placement or safety decisions.

## Why this fits the role

NCC emphasizes circularity, customer needs, cross-Nordic collaboration, material evaluation, quality, commercial value and structured product development. REFORGE turns those themes into a concrete, explainable workflow. I would welcome expert critique of the assumptions and testing framework.
