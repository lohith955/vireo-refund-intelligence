import pandas as pd

tickets = pd.read_csv("data/tickets.csv")

refunds = tickets[tickets["refund_amount_inr"] > 0].copy()

print("Raw rows:", len(tickets))
print("Raw refund rows:", len(refunds))

print("\nRefund amount by source:")
print(
    refunds.groupby("source_system")["refund_amount_inr"]
    .agg(["count", "sum"])
)
# Find ticket IDs that appear in both systems
source_counts = tickets.groupby("ticket_id")["source_system"].nunique()

migration_duplicate_ids = source_counts[source_counts > 1].index

print("\nMigration duplicate ticket IDs:", len(migration_duplicate_ids))

# Show a few examples
print("\nSample migration duplicates:")
print(
    tickets[tickets["ticket_id"].isin(migration_duplicate_ids)][
        ["ticket_id", "source_system", "refund_amount_inr"]
    ].head(10)
)
# Check the legacy-to-helpdesk amount relationship
paired = tickets[
    tickets["ticket_id"].isin(migration_duplicate_ids)
    & (tickets["refund_amount_inr"] > 0)
].copy()

paired["normalized_amount"] = paired.apply(
    lambda row: row["refund_amount_inr"] / 100
    if row["source_system"] == "legacy_fd"
    else row["refund_amount_inr"],
    axis=1
)

print("\nPaired refund rows:", len(paired))

print("\nNormalized paired refunds:")
print(
    paired.groupby("ticket_id")["normalized_amount"]
    .agg(["min", "max"])
    .head(10)
)
# Build the reconciled dataset

# Keep all helpdesk rows.
# For legacy rows, keep them only when the ticket does NOT exist in helpdesk.
helpdesk_ids = set(
    tickets.loc[tickets["source_system"] == "helpdesk", "ticket_id"]
)

clean = tickets[
    (tickets["source_system"] == "helpdesk")
    | (
        (tickets["source_system"] == "legacy_fd")
        & (~tickets["ticket_id"].isin(helpdesk_ids))
    )
].copy()

# Convert legacy monetary values from Freshdesk units to INR
legacy_mask = clean["source_system"] == "legacy_fd"

clean.loc[legacy_mask, "refund_amount_inr"] = (
    clean.loc[legacy_mask, "refund_amount_inr"] / 100
)

print("\nClean rows:", len(clean))
print("Clean refund rows:", (clean["refund_amount_inr"] > 0).sum())

print(
    "\nReconciled refund total: ₹{:,.2f}".format(
        clean["refund_amount_inr"].fillna(0).sum()
    )
)

print("\nRefunds by source after reconciliation:")
print(
    clean.loc[clean["refund_amount_inr"] > 0]
    .groupby("source_system")["refund_amount_inr"]
    .agg(["count", "sum"])
)
# Save the reconciled dataset
clean.to_csv("data/clean_tickets.csv", index=False)

print("\nSaved: data/clean_tickets.csv")
