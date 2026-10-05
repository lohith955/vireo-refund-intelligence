# Banao Technologies — AI Pre-Assessment Submission

## 1. What did you build, and what business outcome does it move? State the number and money.

I built an AI-assisted **Refund Intelligence and Audit Platform** that reconciles helpdesk and legacy refund data, analyzes refund reasons and agent attribution, and performs AI-assisted audit and control checks.

The reconciled dataset contains **2,340 refund tickets worth ₹67.10 lakh**. **GW-OTHER accounts for 43.3% of refund value**, making refund reason attribution the main business opportunity.

The tool also identified **638 migration duplicate ticket IDs**, while **250 paired refund records matched after normalization**, and found **0 refund-plus-replacement violations** under the available fields.

---

## 2. What does one run cost, and what would a month cost at Vireo's volume (roughly 650 tickets a week)? Show arithmetic.

No paid AI/API calls were used, so the direct AI cost is **₹0 per run**.

Vireo's volume is roughly 650 tickets/week.

```text
650 × 4.33 = 2,815 tickets/month

AI/API cost per ticket = ₹0

2,815 × ₹0 = ₹0/month
```

Therefore, the direct AI/API cost is **₹0 per month**.

This excludes local electricity, internet, hosting, or other infrastructure costs.

---

## 3. How do you know it works? Sample size, how checked, error rate, and kind of case it gets wrong.

I validated the solution using the supplied dataset and a **stratified 80/20 train-test split** for the AI reason-classification model.

The AI model was evaluated on **493 test records**.

Results:

- Overall accuracy: **55.98%**
- Overall error rate: **44.02%**
- GW-OTHER test records: **198**
- GW-OTHER correctly classified: **20**
- GW-OTHER accuracy: **10.10%**
- GW-OTHER error rate: **89.90%**

The model gets GW-OTHER cases wrong because their text can resemble several other refund categories, including **DUP-PAYMENT, WTY-BUYBACK, RETURN-QC-OK, CANCEL, and DOA-REPL**.

Because of this limitation, the AI is used only for **audit and human review**, not for automatically changing financial records or refund reason codes.

---

## 4. Did you change, narrow, or push back on the client's ask? What, when, and why?

Yes. I narrowed the original question from **"who is giving away money and for what"** into **refund attribution, reconciliation, and control analysis**.

I made this change during the analysis after finding that high refund volume alone does not prove that an agent is giving away money, especially because the Returns Desk processes the majority of refunds according to the policy.

Instead of making a potentially misleading agent-blame conclusion, I focused the tool on showing where the money is going, which refund reasons drive it, how refunds reconcile across systems, and whether control exceptions exist.

This makes the output more defensible for Finance and management.

---

## 5. What did you deliberately leave out, and why that rather than something else?

I deliberately left out **automatic refund reclassification, automatic financial decisions, and ranking agents as "bad actors."**

I left these out because the AI model was not accurate enough for automatic decisions, and high refund volume alone does not prove agent misconduct. The policy also says that the Returns Desk processes most refunds.

Instead, I focused on **refund attribution, reconciliation, AI audit flags, and control checks** because these directly support the Finance team's goal without making unsupported conclusions.

---

## 6. What is wrong with what you are handing us? Be specific: bugs, shortcuts, things you know are off.

The main limitation is the AI classification model. Its overall accuracy is only **55.98%**, and GW-OTHER accuracy is **10.10%**, so it is not reliable enough for automatic financial or reason-code changes. I therefore use it only for audit and human review.

The project is also a working prototype, not a production system. It does not connect directly to Vireo's live helpdesk or Finance systems, so the data must be supplied as files.

The reconciliation depends on the fields available in the provided dataset, so the refund-plus-replacement control can only confirm cases represented by those fields.

I also did not claim causation between refund trends and the Q4 policy change; the dashboard shows the observed data rather than proving why refunds changed.

Finally, the dashboard focuses on the requested refund analysis and controls rather than production features such as authentication, automated deployment, live database integration, or scheduled monitoring.

---

## 7. Anything you built or found that nobody asked for?

I built a few useful controls and insights beyond the basic monthly refund report.

The main additions were a **migration reconciliation check**, which identified **638 ticket IDs appearing across both systems** and verified **250 paired refund records after normalization**; a **refund-plus-replacement control**, which found **0 cases** under the available fields; and an **AI audit layer** to identify potentially misclassified refund reasons, especially the high-volume GW-OTHER category.

I also added a management-facing **Board Room summary** so the Finance team can move from raw refund data to the main risks, trends, and actions without reading the full analysis.

---

## 8. AI use — Where and how did you use AI?

AI was used as part of the development and analysis workflow.

I used AI assistance to help structure the solution, refine analysis logic, develop the Streamlit dashboard, prepare validation logic, improve the README and submission documentation, and review the business framing.

The final application also contains an AI-assisted refund reason classification component using **TF-IDF and Logistic Regression**.

No paid AI/API calls were used for the final tool.

The AI classifier is deliberately restricted to **audit and human review** because its accuracy is not sufficient for automatic financial decisions.

---

## 9. Public Google Drive link

Screen recording / assessment files:

[https://drive.google.com/file/d/1bd4CqvhzWZaJoyB6Hc0lTv63lxw7tg_Z/view?usp=drive_link](https://drive.google.com/file/d/1bd4CqvhzWZaJoyB6Hc0lTv63lxw7tg_Z/view?usp=drive_link)

---

## 10. Someone picks this up on Monday and you are unreachable. The three things they need to know.

1. **Start with the README and run `streamlit run app.py`.** The dashboard is the main entry point and `requirements.txt` contains the required Python packages.

2. **Trust the reconciliation and control results, not the AI as an automated decision-maker.** The reconciled total is ₹67.10 lakh across 2,340 refund tickets, with 638 migration duplicate IDs identified and 0 refund-plus-replacement cases found under the available fields.

3. **The AI classifier is audit-only.** Overall accuracy is 55.98% and GW-OTHER accuracy is only 10.10%, so it must not automatically change reason codes or make financial decisions. The main business opportunity is improving the 43.3% GW-OTHER attribution.

---

## 11. Honest hours spent

3.45



---

## 13. Final deliverables

- [x] Working Streamlit application
- [x] README with setup instructions
- [x] Requirements file
- [x] Reconciled/cleaned dataset
- [x] Refund analysis
- [x] Agent analysis
- [x] AI audit
- [x] Control checks
- [x] One-page Finance memo
- [x] Screen recording
- [x] Google Drive link
- [x] Public GitHub repository
- [x] Submission form

---

