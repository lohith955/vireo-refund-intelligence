VIREO AUDIO â€” SUPPORT DATA PACK
================================# Vireo Refund Intelligence & Audit Platform

An AI-assisted refund intelligence and audit platform built as part of the **Banao Technologies AI Engineer / Applied AI assessment**.

The platform reconciles refund data from helpdesk and legacy systems, analyzes refund drivers, provides agent/team attribution, performs AI-assisted reason-code auditing, and checks key refund controls.

## Business Objective

The original business question was to understand **monthly refunds by reason and agent**, reconcile the total with Finance, and identify where refund value is being attributed.

The project narrows this into a more defensible analysis of:

- Where refund money is going
- Which refund reasons drive the most value
- How refunds are attributed to agents and teams
- Whether legacy/helpdesk data contains migration duplicates
- Whether refund control violations exist
- Whether AI can assist with refund-reason auditing

## Key Results

| Metric | Result |
|---|---:|
| Reconciled refund value | ₹67.10 lakh |
| Reconciled refund tickets | 2,340 |
| GW-OTHER refund value | ₹29.07 lakh |
| GW-OTHER share | 43.3% |
| Migration duplicate ticket IDs | 638 |
| Paired refund records validated | 250 |
| Refund + replacement violations | 0 |

The highest refund-value category is **GW-OTHER**, making refund-reason attribution and classification the main business opportunity identified by the analysis.

## Main Dashboard

The Streamlit dashboard contains six main sections:

1. **Executive Overview** – key financial and operational KPIs
2. **Refund Intelligence** – monthly and reason-level refund analysis
3. **Agent Intelligence** – refund attribution by agent, team, tier, and reason
4. **AI Audit** – machine-learning based reason-code audit
5. **Control Scanner** – reconciliation and refund-control checks
6. **Board Room** – management-oriented summary and key actions

## Data Reconciliation

The dataset contains records from two systems:

- `helpdesk`
- `legacy_fd`

The analysis identified **638 ticket IDs appearing across both systems**.

For **250 paired refund records**, the legacy monetary values were normalized and matched exactly with their helpdesk counterparts.

This reconciliation prevents the legacy values from being incorrectly counted at their exported scale.

## Refund Analysis

The reconciled dataset contains **2,340 refund tickets worth ₹67.10 lakh**.

The largest refund reasons by value are:

| Reason | Refund Value | Share |
|---|---:|---:|
| GW-OTHER | ₹29.07 lakh | 43.3% |
| RETURN-QC-OK | ₹11.81 lakh | 17.6% |
| DUP-PAYMENT | ₹8.85 lakh | 13.2% |
| CANCEL | ₹6.13 lakh | 9.1% |
| DOA-REPL | ₹4.71 lakh | 7.0% |

## Agent Analysis

Agent analysis uses the cleaned ticket data together with the roster information in `agents.csv`.

High refund volume is **not treated as proof of agent misconduct** because:

- The Returns Desk processes the majority of refunds.
- Agents can have different responsibilities and teams.
- Tier 2 should not be directly compared with Tier 1 on volume metrics.
- Refund volume alone does not establish whether a refund was inappropriate.

The dashboard therefore focuses on attribution and patterns rather than labeling agents as bad actors.

## AI Audit

The AI audit uses:

- TF-IDF text features
- Unigrams and bigrams
- Logistic Regression
- Stratified 80/20 train-test validation

The model combines:

- `customer_message`
- `agent_notes`

### Validation Results

- Overall accuracy: **55.98%**
- Overall error rate: **44.02%**
- GW-OTHER test records: **198**
- GW-OTHER correct: **20**
- GW-OTHER accuracy: **10.10%**
- GW-OTHER error rate: **89.90%**

GW-OTHER is difficult to classify because its text can resemble several other refund categories, including:

- DUP-PAYMENT
- WTY-BUYBACK
- RETURN-QC-OK
- CANCEL
- DOA-REPL

Because of the model's accuracy, the AI layer is used **only for audit and human review**. It does not automatically change financial records or refund reason codes.

## Control Checks

The project includes a refund-plus-replacement control check.

Under the available dataset fields, the analysis found:

**0 tickets where both a refund and replacement were recorded.**

The reconciliation and control checks are based only on the fields available in the supplied dataset.

## Running the Project

### Requirements

Python 3.x is recommended.

Install the required packages:

```bash
pip install -r requirements.txt
```

### Start the Dashboard

Run:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

## Project Structure

```text
vireo-refund-intelligence/
│
├── app.py
├── ai_analysis.py
├── agent_analysis.py
├── violations.py
├── requirements.txt
├── README.md
├── submission-form.md
│
└── data/
    ├── clean_tickets.csv
    └── agents.csv
```

## Limitations

This is a working assessment prototype rather than a production deployment.

Known limitations:

- The AI classifier is not accurate enough for automatic financial decisions.
- The tool does not directly connect to Vireo's live helpdesk or Finance systems.
- Input data must currently be supplied as files.
- Refund-plus-replacement validation is limited to the fields available in the supplied dataset.
- The analysis does not claim that the Q4 policy change caused the observed refund trend.
- The project does not include production authentication, deployment, live database integration, or scheduled monitoring.

## Cost

No paid AI/API calls were used for the final tool.

At approximately **650 tickets per week**:

```text
650 × 4.33 = 2,815 tickets/month
2,815 × ₹0 paid AI/API cost = ₹0/month
```

This excludes local electricity, internet, hosting, and other infrastructure costs.

## Original Dataset Documentation

The following documentation describes the supplied Vireo dataset and operating-policy files.

### tickets.csv

Support tickets, 1 Jan 2025 – 30 Jun 2026. One row per ticket as exported.

- `ticket_id` — Helpdesk ticket number
- `created_at` — Ticket creation
- `first_response_at` — First human agent reply
- `resolved_at` — Resolution (blank if open/pending). For legacy tickets this was reconstructed from the event log.
- `status` — `resolved | closed` (auto-closed, no customer reply) `| open | pending`
- `channel` — `chat | email | voice | social`
- `customer_id` — Key into `customers.csv`
- `order_id` — Key into `orders.csv`. Blank when the customer did not quote it. `customer_id + product_sku` is the fallback join.
- `product_sku` — Key into `products.csv`
- `category` — Category tag set by the intake bot at creation; agents may re-tag on closure
- `priority` — `Low | Normal | High`
- `assigned_team` — Team the ticket was first routed to
- `agent_id` — Agent who resolved the ticket. Key into `agents.csv`. Use the ID, not the name.
- `transfers` — Number of hand-offs between teams
- `csat_score` — 1–5 survey score. Blank = no response.
- `refund_amount_inr` — Refund raised on the ticket, as exported by each system. Blank = none.
- `refund_reason_code` — Dropdown code selected by the agent (see `support-policy.pdf` §5)
- `replacement_issued` — Y/N flag set by the agent
- `customer_message` — Customer's opening message (chat/email/social) or IVR transcript (voice)
- `agent_notes` — Agent's closing note
- `source_system` — `helpdesk | legacy_fd` (migrated from Freshdesk, see `support-policy.pdf` §9)

### agents.csv

Roster. One row per assignment:

```text
agent_id, name, site, team, shift, tier, from_date, to_date
```

An agent can have more than one row.

### orders.csv

Orders:

```text
order_id, customer_id, sku, order_date, channel, qty,
order_value_inr, lot_code
```

`lot_code` is the manufacturing lot printed on the box.

### customers.csv

Customers:

```text
customer_id, name, city, state, signup_date, care_plus
```

### products.csv

Products:

```text
sku, product_name, family, launch_date, unit_cost_inr,
retail_price_inr, warranty_months
```

### support-policy.pdf

Vireo's support operating policy v3.2 covering:

- SLAs
- Support costs
- Refund rules
- Replacement rules
- Shifts
- Reporting definitions
- Reason codes
- Legacy-system handling

### email-thread.txt

Messages already exchanged between Vireo and us about this work.

No other documentation was available in the supplied assessment materials.