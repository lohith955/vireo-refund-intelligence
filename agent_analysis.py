import pandas as pd

# Load reconciled data
tickets = pd.read_csv("data/clean_tickets.csv")

# Load agent roster
agents = pd.read_csv("data/agents.csv")

# Keep refund tickets only
refunds = tickets[tickets["refund_amount_inr"] > 0].copy()

# Convert dates
refunds["created_at"] = pd.to_datetime(refunds["created_at"])
agents["from_date"] = pd.to_datetime(agents["from_date"])
agents["to_date"] = pd.to_datetime(agents["to_date"])

# Match each refund to the agent roster active on that ticket date
refunds["ticket_date"] = refunds["created_at"].dt.normalize()

refunds = refunds.merge(
    agents,
    on="agent_id",
    how="left"
)

refunds = refunds[
    (refunds["ticket_date"] >= refunds["from_date"])
    &
    (
        refunds["to_date"].isna()
        | (refunds["ticket_date"] <= refunds["to_date"])
    )
].copy()

# --------------------------------------------------
# 1. TOP AGENTS BY REFUND VALUE
# --------------------------------------------------

agent_summary = (
    refunds.groupby(
        ["agent_id", "name", "team", "tier"]
    )
    .agg(
        refund_tickets=("ticket_id", "count"),
        refund_amount_inr=("refund_amount_inr", "sum"),
        average_refund=("refund_amount_inr", "mean"),
    )
    .sort_values("refund_amount_inr", ascending=False)
    .reset_index()
)

print("\n" + "=" * 70)
print("TOP AGENTS BY REFUND VALUE")
print("=" * 70)

print(
    agent_summary.head(10).to_string(index=False)
)

# --------------------------------------------------
# 2. TOP REASONS FOR TOP 10 AGENTS
# --------------------------------------------------

top_agents = agent_summary.head(10)["agent_id"].tolist()

top_agent_reasons = (
    refunds[refunds["agent_id"].isin(top_agents)]
    .groupby(
        ["agent_id", "name", "team", "tier", "refund_reason_code"]
    )
    .agg(
        refund_tickets=("ticket_id", "count"),
        refund_amount_inr=("refund_amount_inr", "sum"),
    )
    .sort_values(
        ["agent_id", "refund_amount_inr"],
        ascending=[True, False]
    )
    .reset_index()
)

print("\n" + "=" * 70)
print("TOP REFUND REASONS FOR TOP 10 AGENTS")
print("=" * 70)

print(
    top_agent_reasons.to_string(index=False)
)

# --------------------------------------------------
# 3. GW-OTHER BY AGENT
# --------------------------------------------------

gw_other = (
    refunds[
        refunds["refund_reason_code"] == "GW-OTHER"
    ]
    .groupby(
        ["agent_id", "name", "team", "tier"]
    )
    .agg(
        refund_tickets=("ticket_id", "count"),
        refund_amount_inr=("refund_amount_inr", "sum"),
        average_refund=("refund_amount_inr", "mean"),
    )
    .sort_values("refund_amount_inr", ascending=False)
    .reset_index()
)

print("\n" + "=" * 70)
print("GW-OTHER BY AGENT")
print("=" * 70)

print(
    gw_other.head(15).to_string(index=False)
)

# --------------------------------------------------
# 4. TIER 1 VS TIER 2
# --------------------------------------------------

tier_summary = (
    refunds.groupby("tier")
    .agg(
        refund_tickets=("ticket_id", "count"),
        refund_amount_inr=("refund_amount_inr", "sum"),
        average_refund=("refund_amount_inr", "mean"),
    )
    .reset_index()
)

print("\n" + "=" * 70)
print("REFUNDS BY TIER")
print("=" * 70)

print(
    tier_summary.to_string(index=False)
)

# --------------------------------------------------
# TOTAL RECONCILED REFUNDS
# --------------------------------------------------

print("\n" + "=" * 70)
print("TOTAL RECONCILED REFUNDS")
print("=" * 70)

print(
    "₹{:,.2f}".format(
        refunds["refund_amount_inr"].sum()
    )
)