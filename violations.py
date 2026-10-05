import pandas as pd

# Load reconciled data
tickets = pd.read_csv("data/clean_tickets.csv")

# Find tickets where BOTH refund and replacement were issued
violations = tickets[
    (tickets["refund_amount_inr"] > 0)
    & (tickets["replacement_issued"] == True)
].copy()

print("\n" + "=" * 70)
print("REFUND + REPLACEMENT VIOLATIONS")
print("=" * 70)

print("Violation tickets:", len(violations))
print(
    "Refund amount involved: ₹{:,.2f}".format(
        violations["refund_amount_inr"].sum()
    )
)

print("\nViolation details:")

print(
    violations[
        [
            "ticket_id",
            "created_at",
            "agent_id",
            "refund_amount_inr",
            "refund_reason_code",
            "replacement_issued",
            "order_id",
            "product_sku",
        ]
    ].to_string(index=False)
)