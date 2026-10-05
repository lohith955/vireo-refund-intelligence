import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------------------------
# 1. LOAD RECONCILED DATA
# --------------------------------------------------

tickets = pd.read_csv("data/clean_tickets.csv")

# Keep refund tickets with a reason code and text
refunds = tickets[
    (tickets["refund_amount_inr"] > 0)
    & (tickets["refund_reason_code"].notna())
].copy()

# Combine customer message + agent notes
refunds["text"] = (
    refunds["customer_message"].fillna("")
    + " "
    + refunds["agent_notes"].fillna("")
)

# Remove empty text
refunds = refunds[refunds["text"].str.strip() != ""]


print("\n" + "=" * 70)
print("AI REFUND REASON CLASSIFIER")
print("=" * 70)

print("Refund records:", len(refunds))
print("Reason classes:", refunds["refund_reason_code"].nunique())


# --------------------------------------------------
# 2. TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    refunds["text"],
    refunds["refund_reason_code"],
    test_size=0.20,
    random_state=42,
    stratify=refunds["refund_reason_code"]
)


# --------------------------------------------------
# 3. TF-IDF TEXT FEATURES
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2,
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# --------------------------------------------------
# 4. TRAIN CLASSIFIER
# --------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)


# --------------------------------------------------
# 5. VALIDATION
# --------------------------------------------------

predictions = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 70)
print("MODEL VALIDATION")
print("=" * 70)

print("Test records:", len(y_test))
print("Accuracy: {:.2%}".format(accuracy))
print("Error rate: {:.2%}".format(1 - accuracy))

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# --------------------------------------------------
# 6. FLAG POTENTIAL REASON-CODE MISMATCHES
# --------------------------------------------------

results = pd.DataFrame({
    "actual_reason": y_test.values,
    "predicted_reason": predictions,
    "text": X_test.values
})

mismatches = results[
    results["actual_reason"] != results["predicted_reason"]
].copy()

print("\n" + "=" * 70)
print("POTENTIAL REASON-CODE MISMATCHES")
print("=" * 70)

print("Mismatches:", len(mismatches))

print(
    mismatches[
        [
            "actual_reason",
            "predicted_reason",
            "text"
        ]
    ].head(20).to_string(index=False)
)


# --------------------------------------------------
# 7. GW-OTHER REVIEW
# --------------------------------------------------

gw_other = results[
    results["actual_reason"] == "GW-OTHER"
].copy()

print("\n" + "=" * 70)
print("GW-OTHER VALIDATION")
print("=" * 70)

print("GW-OTHER test records:", len(gw_other))

if len(gw_other) > 0:
    gw_correct = (
        gw_other["actual_reason"]
        == gw_other["predicted_reason"]
    ).sum()

    print(
        "GW-OTHER correctly classified: {} / {}".format(
            gw_correct,
            len(gw_other)
        )
    )

    print(
        "GW-OTHER accuracy: {:.2%}".format(
            gw_correct / len(gw_other)
        )
    )
print("\n" + "=" * 70)
print("FINAL AI VALIDATION SUMMARY")
print("=" * 70)

print("Overall accuracy: {:.2%}".format(accuracy))
print("Overall error rate: {:.2%}".format(1 - accuracy))
print("GW-OTHER accuracy: {:.2%}".format(
    gw_correct / len(gw_other)
    if len(gw_other) > 0 else 0
))
print("GW-OTHER error rate: {:.2%}".format(
    1 - (gw_correct / len(gw_other))
    if len(gw_other) > 0 else 0
))