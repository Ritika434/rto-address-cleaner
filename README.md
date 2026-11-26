# RTO Address Cleaner
A rules first, LLM second pipeline that helps avoid delivery failures due to address issues in India by analysing and scoring address completeness and requesting missing address info to the customers on whatsapp predelivery.

## The problem          
Returns and its Logistics are a nightmare for D2C brands especially in countries like India where the addresses are not very structured. Customers usually share their addresses with good intent on what seem enough for them but it is not sufficient sometimes for a successful delivery. Address Quality and its completeness needs an internal pipeline to ensure that all addresses are complete before the actual delivery attempts are made.

## Approach            
RTO Address Cleaner is an attempt to create such a pipeline that can assist D2C brands with their RTO issues. It works in five stages:
1. Generate - This stage helps generate synthetic orders modelled on common Indian address problems (vague lines, bad pincodes, messy city names), so no real customer data is used.
2. Rules Engine - This is the deterministic stage that helps filter out or correct the address information based on set guardrails and rules across identified patterns.
3. LLM - After rules engine, any indeterministic changes are looked at by LLM to ensure address completeness is thorough. The LLM prompt is structured and only takes effect if the rules were insufficient thus keeping the total token costs low.
4. Drafts - This stage collates the missing or incorrect information from the address data and generates a draft for the user to send them a message and request info that would make the address complete and assist in ease of delivery.
5. Risk scoring - a transparent, rule-based score (not a trained model) that flags high-risk orders before dispatch.

## Results

| Metric | Value |
|---|---|
| Orders processed | 1,000 (synthetic) |
| Handled by rules alone (no LLM) | **79.2%** (792 of 1,000) |
| Sent to the LLM | 208 orders, in **11 calls** (batches of 20) |
| Tokens | **28,158** total, about **135 per order** |
| WhatsApp drafts | **200 drafts** (172 English / 28 Hindi) |
| Unreachable (invalid phone) | **46** orders → `reach_other_way.csv` instead of WhatsApp |
| Vague-address rule vs planted ground truth | **138 of 138**: precision 100%, recall 100% |
| Pincodes copied by the LLM (eval) | **0**, checked automatically on every run |
| Tests | **27 pytest tests**, no API calls |

## Evaluation findings
Evals caught five issues; each was fixed or explained, and re-measured.

| # | What the eval found | Fix | Result |
|---|---|---|---|
| 1 | City/pincode mismatches (61 orders) never triggered a question to the customer | New `city` ask, in English and Hindi | Mismatches now get a draft |
| 2 | Customers with invalid phone numbers were getting WhatsApp drafts | Route them to a separate "reach another way" list (checked across all rows, not just LLM rows) | 46 orders routed correctly |
| 3 | The vague-address rule flagged 2 real addresses (e.g. `418 Ben, Saket`) because they were short | Rule changed to "no house number digit". A "short AND no digit" variant was tested and rejected: it would have missed 4 of 6 vague patterns | 138 flagged, 138 planted |
| 4 | The LLM kept a `H.No.` prefix on some house numbers | Deterministic post-LLM `clean_house_number()` | 6 parametrized tests |
| 5 | 3 pincodes appeared "copied" from the pincode field in one run | Automated check on every run | 0 on a fresh run, so the 3 were run-to-run model variation, not a prompt regression |

## Risk scoring
A transparent, rule-based score: a COD base, weights per issue from config, plus repeat-customer phones, then a threshold sweep against the RTO labels (RTO base rate 18.8%).

| Threshold | Flagged | Precision | Recall |
|---|---|---|---|
| 0.15 | 722 | 24.8% | 95.2% |
| 0.20 | 299 | 35.5% | 56.4% |
| 0.30 | 234 | 44.4% | 55.3% |
| 0.40 | 177 | 53.1% | 50.0% |
| 0.50 | 41 | 70.7% | 15.4% |

**Key insight:** recall plateaus at about 55%. Roughly **half of RTOs happen on orders with no address or phone problem**, so address quality alone can't catch them; customer history and pincode-level return rates are the next signals to add. Accuracy is misleading here: at 0.5 it scores 82.9%, while flagging nothing would score 81.2%.

**Suggested policy:** score ≥ 0.4 (177 per 1,000 orders) → WhatsApp address fix plus a human confirmation call; all other COD orders → an automated "confirm your order" WhatsApp.

## Limitations
- **Synthetic data.** I wrote both the rules and the data generator, so 100% on planted patterns means "matches what I planted", not "works on real orders". The next step is a hand-labelled sample of real orders.
- **RTO labels are synthetic too.** They were generated from similar flags, so risk-score results will be noisier on real data.
- **LLM outputs vary between runs**, which is why the evals run every time, not once.
- A real address with no number (e.g. "Flat B, Sunrise Apartments") is flagged as vague. That's acceptable, because the cost is one extra WhatsApp question.

## Tests
`pytest -v`: 27 tests covering phone normalisation, the vague rule (all planted patterns plus regression tests), pincode flags, house-number cleaning, draft text in English and Hindi, batching and prompt wrapping, and risk-score boundaries. No test calls the LLM.


## How to run
```bash
cp .env.example .env       # then add your GEMINI_API_KEY to .env
python -m src.generate     # synthetic orders → data/
python -m src.pipeline     # rules + LLM → data/cleaned_orders_v0.csv
python -m src.drafts       # WhatsApp drafts → data/drafts.csv
python -m src.risk         # risk-score threshold sweep
python -m src.evaluate     # eval checks (vague rule, copied pincodes)
pytest -v                  # unit tests (no API calls)             
```