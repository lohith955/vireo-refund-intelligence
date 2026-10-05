import pandas as pd

# Load reconciled data
tickets = pd.read_csv("data/clean_tickets.csv")

# Keep refund tickets only
refunds = tickets[tickets["refund_amount_inr"] > 0].copy()

# Convert date
refunds["created_at"] = pd.to_datetime(refunds["created_at"])

# Create month
refunds["month"] = refunds["created_at"].dt.to_period("M").astype(str)

# Monthly refund summary
monthly = (
    refunds.groupby("month")
    .agg(
        refund_tickets=("ticket_id", "count"),
        refund_amount_inr=("refund_amount_inr", "sum"),
        average_refund=("refund_amount_inr", "mean"),
    )
    .reset_index()
)

print("\nMONTHLY REFUNDS")
print(monthly.to_string(index=False))

print("\nTOTAL REFUNDS: ₹{:,.2f}".format(
    refunds["refund_amount_inr"].sum()
))
# Refund analysis by reason code
reason_summary = (
    refunds.groupby("refund_reason_code")
    .agg(
        refund_tickets=("ticket_id", "count"),
        refund_amount_inr=("refund_amount_inr", "sum"),
        average_refund=("refund_amount_inr", "mean"),
    )
    .sort_values("refund_amount_inr", ascending=False)
    .reset_index()
)

print("\nREFUNDS BY REASON CODE")
print(reason_summary.to_string(index=False))