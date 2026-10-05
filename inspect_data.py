import pandas as pd

tickets = pd.read_csv("data/tickets.csv")

print("Rows:", len(tickets))
print("\nColumns:")
print(tickets.columns.tolist())

print("\nFirst 5 rows:")
print(tickets.head())

print("\nData types:")
print(tickets.dtypes)

print("\nRefund rows:", (tickets["refund_amount_inr"] > 0).sum())

print("\nRefund reason codes:")
print(tickets.loc[tickets["refund_amount_inr"] > 0, "refund_reason_code"].value_counts())

print("\nSource systems:")
print(tickets["source_system"].value_counts())

print("\nDuplicate ticket IDs:", tickets["ticket_id"].duplicated(keep=False).sum())