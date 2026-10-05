import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




st.set_page_config(
    page_title="Vireo Command Center",
    page_icon="V",
    layout="wide",
    initial_sidebar_state="expanded"
)




@st.cache_data
def load_data():

    tickets = pd.read_csv("data/clean_tickets.csv")
    agents = pd.read_csv("data/agents.csv")

    tickets["created_at"] = pd.to_datetime(tickets["created_at"])
    agents["from_date"] = pd.to_datetime(agents["from_date"])
    agents["to_date"] = pd.to_datetime(agents["to_date"])

    return tickets, agents


tickets, agents = load_data()


# =========================================================
# REFUND DATA
# =========================================================

refunds = tickets[
    tickets["refund_amount_inr"] > 0
].copy()


# =========================================================
# GLOBAL CALCULATIONS
# =========================================================

total_refund = refunds["refund_amount_inr"].sum()

refund_count = len(refunds)

gw = refunds[
    refunds["refund_reason_code"] == "GW-OTHER"
]

gw_amount = gw["refund_amount_inr"].sum()

gw_share = (
    gw_amount / total_refund * 100
    if total_refund > 0
    else 0
)

duplicate_ids = 638

clean_tickets = len(tickets)

policy_violations = len(
    tickets[
        (tickets["refund_amount_inr"] > 0)
        & (tickets["replacement_issued"] == True)
    ]
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0,190,255,0.08),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(120,70,255,0.08),
                transparent 25%
            ),
            #080b12;
    }

    section[data-testid="stSidebar"] {
        background: #0c1018;
        border-right: 1px solid #202735;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #8f9aaa;
        font-size: 15px;
        margin-bottom: 20px;
    }

    .footer {
        text-align: center;
        color: #586274;
        font-size: 11px;
        padding: 35px 0 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## VIREO")

st.sidebar.caption(
    "REFUND INTELLIGENCE SYSTEM"
)

page = st.sidebar.radio(
    "COMMAND CENTER",
    [
        "Executive Overview",
        "Refund Intelligence",
        "Agent Intelligence",
        "AI Audit",
        "Control Scanner",
        "Board Room"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### SYSTEM STATUS")

st.sidebar.success("DATA RECONCILED")
st.sidebar.success("AI MODEL READY")
st.sidebar.success("CONTROL CHECK COMPLETE")

st.sidebar.divider()

st.sidebar.caption("Vireo Audio")
st.sidebar.caption("Applied AI Analysis")
st.sidebar.caption("Task 1 — Refund Intelligence")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">VIREO COMMAND CENTER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Refund intelligence • reconciliation • agent analytics • AI audit'
    '</div>',
    unsafe_allow_html=True
)

st.success("● SYSTEM ONLINE")


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    st.header("Executive Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Reconciled Refunds",
            f"₹{total_refund / 100000:.2f}L"
        )
        st.caption("Finance-ready total")

    with c2:
        st.metric(
            "Refund Tickets",
            f"{refund_count:,}"
        )
        st.caption("After reconciliation")

    with c3:
        st.metric(
            "GW-OTHER Share",
            f"{gw_share:.1f}%"
        )
        st.caption("Requires reason-code review")

    with c4:
        st.metric(
            "Policy Violations",
            f"{policy_violations}"
        )
        st.caption("Refund + replacement")

    st.divider()

    # -----------------------------------------------------
    # MONTHLY REFUND TREND
    # -----------------------------------------------------

    monthly = (
        refunds
        .assign(
            month=refunds["created_at"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("month")
        .agg(
            refund_amount=(
                "refund_amount_inr",
                "sum"
            ),
            tickets=(
                "ticket_id",
                "count"
            )
        )
        .reset_index()
    )

    st.subheader("Refund Pulse")

    st.caption(
        "Monthly reconciled refund movement"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["refund_amount"],
            mode="lines+markers",
            line=dict(width=4),
            marker=dict(size=8),
            fill="tozeroy"
        )
    )

    fig.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce2eb"),
        xaxis_title=None,
        yaxis_title="Refund Amount (₹)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # INSIGHTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.warning(
            f"""
            ### ⚠ GW-OTHER DATA QUALITY

            **{gw_share:.1f}%** of total refund value is classified
            as GW-OTHER.

            Total GW-OTHER value:

            **₹{gw_amount / 100000:.2f}L**

            AI validation classified only **10.1%** of GW-OTHER
            test records correctly.

            **Action:** Review reason-code usage before using
            GW-OTHER for management decisions.
            """
        )

    with col2:

        st.success(
            f"""
            ### ✓ RECONCILIATION CONTROL

            **₹{total_refund / 100000:.2f}L** validated.

            **{duplicate_ids}** migration duplicate IDs were identified.

            Paired legacy/helpdesk refund values were normalized
            and reconciled.

            **Result:** Finance-ready refund dataset created.
            """
        )


# =========================================================
# REFUND INTELLIGENCE
# =========================================================

elif page == "Refund Intelligence":

    st.header("Refund Intelligence")

    st.caption(
        "Understand where refund money is going."
    )

    reason = (
        refunds
        .groupby("refund_reason_code")
        .agg(
            tickets=("ticket_id", "count"),
            amount=("refund_amount_inr", "sum"),
            average=("refund_amount_inr", "mean")
        )
        .sort_values(
            "amount",
            ascending=False
        )
        .reset_index()
    )

    # -----------------------------------------------------
    # KPI
    # -----------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Total Refund Value",
            f"₹{total_refund / 100000:.2f}L"
        )

    with c2:
        st.metric(
            "Refund Tickets",
            f"{refund_count:,}"
        )

    with c3:
        st.metric(
            "Largest Reason",
            "GW-OTHER"
        )

    st.divider()

    
    st.subheader("Refund Value by Reason")

    fig = px.bar(
        reason,
        x="refund_reason_code",
        y="amount",
        text="amount"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce2eb"),
        xaxis_title=None,
        yaxis_title="Refund Amount (₹)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # TWO COLUMNS
    # -----------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("Reason Distribution")

        fig2 = px.pie(
            reason,
            names="refund_reason_code",
            values="amount",
            hole=0.55
        )

        fig2.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dce2eb")
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    with right:

        st.subheader("Reason Summary")

        display_reason = reason.copy()

        display_reason["amount"] = (
            display_reason["amount"]
            .map(lambda x: f"₹{x:,.0f}")
        )

        display_reason["average"] = (
            display_reason["average"]
            .map(lambda x: f"₹{x:,.0f}")
        )

        display_reason.columns = [
            "Reason Code",
            "Tickets",
            "Refund Value",
            "Average Refund"
        ]

        st.dataframe(
            display_reason,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# AGENT INTELLIGENCE
# =========================================================

elif page == "Agent Intelligence":

    st.header("Agent Intelligence")

    st.caption(
        "Refund activity enriched with roster and team context."
    )

    # -----------------------------------------------------
    # ROSTER ENRICHMENT
    # -----------------------------------------------------

    refunds_agent = refunds.copy()

    refunds_agent["ticket_date"] = (
        refunds_agent["created_at"]
        .dt.normalize()
    )

    refunds_agent = refunds_agent.merge(
        agents,
        on="agent_id",
        how="left"
    )

    refunds_agent = refunds_agent[
        (
            refunds_agent["ticket_date"]
            >= refunds_agent["from_date"]
        )
        &
        (
            refunds_agent["to_date"].isna()
            |
            (
                refunds_agent["ticket_date"]
                <= refunds_agent["to_date"]
            )
        )
    ].copy()

    agent_summary = (
        refunds_agent
        .groupby(
            [
                "agent_id",
                "name",
                "team",
                "tier"
            ]
        )
        .agg(
            refunds=(
                "ticket_id",
                "count"
            ),
            refund_value=(
                "refund_amount_inr",
                "sum"
            ),
            average_refund=(
                "refund_amount_inr",
                "mean"
            )
        )
        .sort_values(
            "refund_value",
            ascending=False
        )
        .reset_index()
    )

    # -----------------------------------------------------
    # AGENT KPIs
    # -----------------------------------------------------

    top_agent = agent_summary.iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Agents with Refund Activity",
            f"{len(agent_summary):,}"
        )

    with c2:
        st.metric(
            "Highest Refund Value",
            f"₹{top_agent['refund_value'] / 100000:.2f}L"
        )

    with c3:
        st.metric(
            "Top Agent",
            top_agent["name"]
        )

    st.divider()

    # =====================================================
    # FIXED REFUND LEADERBOARD
    # =====================================================

    st.subheader("🏆 Refund Leaderboard")

    st.caption(
        "Ranked by reconciled refund value. High volume does not "
        "automatically indicate misconduct."
    )

    top = agent_summary.head(10).reset_index(drop=True)

    for i, row in top.iterrows():

        col1, col2, col3, col4 = st.columns(
            [0.6, 2.8, 2.0, 1.8]
        )

        with col1:

            if i == 0:
                st.markdown("### 🥇")

            elif i == 1:
                st.markdown("### 🥈")

            elif i == 2:
                st.markdown("### 🥉")

            else:
                st.markdown(
                    f"### #{i + 1}"
                )

        with col2:

            st.markdown(
                f"**{row['name']}**"
            )

            st.caption(
                f"{row['team']} • {row['tier']}"
            )

        with col3:

            st.metric(
                "Refund Value",
                f"₹{row['refund_value'] / 100000:.2f}L"
            )

        with col4:

            st.metric(
                "Refunds",
                f"{row['refunds']:,}"
            )

        st.divider()

    st.info(
        "Important: Returns Desk processes the majority of refunds, "
        "so high refund volume should not be interpreted as agent "
        "misconduct."
    )

    # -----------------------------------------------------
    # AGENT TABLE
    # -----------------------------------------------------

    st.subheader("Agent Analysis")

    display = agent_summary.copy()

    display["refund_value"] = (
        display["refund_value"]
        .map(lambda x: f"₹{x:,.0f}")
    )

    display["average_refund"] = (
        display["average_refund"]
        .map(lambda x: f"₹{x:,.0f}")
    )

    display.columns = [
        "Agent ID",
        "Agent",
        "Team",
        "Tier",
        "Refund Tickets",
        "Refund Value",
        "Average Refund"
    ]

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # TIER ANALYSIS
    # -----------------------------------------------------

    st.subheader("Tier Context")

    tier_summary = (
        refunds_agent
        .groupby("tier")
        .agg(
            refund_tickets=(
                "ticket_id",
                "count"
            ),
            refund_amount_inr=(
                "refund_amount_inr",
                "sum"
            ),
            average_refund=(
                "refund_amount_inr",
                "mean"
            )
        )
        .reset_index()
    )

    tier_display = tier_summary.copy()

    tier_display["refund_amount_inr"] = (
        tier_display["refund_amount_inr"]
        .map(lambda x: f"₹{x:,.0f}")
    )

    tier_display["average_refund"] = (
        tier_display["average_refund"]
        .map(lambda x: f"₹{x:,.0f}")
    )

    tier_display.columns = [
        "Tier",
        "Refund Tickets",
        "Refund Value",
        "Average Refund"
    ]

    st.dataframe(
        tier_display,
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "Policy note: Tier2 agents should not be compared directly "
        "with Tier1 agents on volume metrics."
    )


# =========================================================
# AI AUDIT
# =========================================================

elif page == "AI Audit":

    st.header("AI Reason-Code Audit")

    st.caption(
        "TF-IDF + Logistic Regression validation of refund reason codes."
    )

    # -----------------------------------------------------
    # AI KPI CARDS
    # -----------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Overall Accuracy",
            "55.98%"
        )

        st.caption(
            "Model validation"
        )

    with c2:

        st.metric(
            "Overall Error",
            "44.02%"
        )

        st.caption(
            "Classification error"
        )

    with c3:

        st.metric(
            "GW-OTHER Accuracy",
            "10.10%"
        )

        st.caption(
            "198 test records"
        )

    st.divider()

    # =====================================================
    # AI FINDING
    # =====================================================

    st.subheader("⚠ AI Finding")

    st.warning(
        """
        **GW-OTHER is not a clean analytical category.**

        The model found that many tickets labelled GW-OTHER contain
        language associated with other legitimate reason categories,
        including:

        - DUP-PAYMENT
        - WTY-BUYBACK
        - RETURN-QC-OK
        - CANCEL
        - DOA-REPL

        This indicates significant reason-code noise or misuse.
        """
    )

    # =====================================================
    # MODEL PERFORMANCE
    # =====================================================

    st.subheader("Model Performance")

    performance = pd.DataFrame(
        {
            "Metric": [
                "Overall Accuracy",
                "Overall Error",
                "GW-OTHER Accuracy",
                "GW-OTHER Error",
                "GW-OTHER Test Records"
            ],
            "Value": [
                "55.98%",
                "44.02%",
                "10.10%",
                "89.90%",
                "198"
            ]
        }
    )

    st.dataframe(
        performance,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # AI DECISION
    # =====================================================

    st.subheader("AI Decision Framework")

    decision = pd.DataFrame(
        {
            "Area": [
                "Financial reconciliation",
                "Reason-code validation",
                "Automatic refund reclassification",
                "Exception detection"
            ],
            "Recommendation": [
                "USE",
                "USE",
                "DO NOT USE AUTOMATICALLY",
                "USE"
            ],
            "Reason": [
                "Reconciliation is deterministic.",
                "AI can identify suspicious reason-code patterns.",
                "Model accuracy is not strong enough for automatic financial changes.",
                "Low-confidence or inconsistent cases can be flagged for review."
            ]
        }
    )

    st.dataframe(
        decision,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        """
        Recommended approach:

        **Use AI as a reason-code quality and exception detector,
        not as an automatic financial reclassification engine.**
        """
    )


# =========================================================
# CONTROL SCANNER
# =========================================================

elif page == "Control Scanner":

    st.header("Control Scanner")

    st.caption(
        "Data integrity and policy control checks."
    )

    # -----------------------------------------------------
    # CONTROL KPIs
    # -----------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Clean Tickets",
            f"{clean_tickets:,}"
        )

        st.caption(
            "Post reconciliation"
        )

    with c2:

        st.metric(
            "Migration IDs",
            f"{duplicate_ids:,}"
        )

        st.caption(
            "Duplicate IDs reconciled"
        )

    with c3:

        st.metric(
            "Policy Violations",
            f"{policy_violations}"
        )

        st.caption(
            "Refund + replacement"
        )

    st.divider()

    # =====================================================
    # CONTROL RESULT
    # =====================================================

    if policy_violations == 0:

        st.success(
            """
            ### ✓ CONTROL CHECK PASSED

            No tickets were identified with both a refund and
            replacement under the available refund/replacement fields.

            Migration duplicates were isolated before financial analysis.
            """
        )

    else:

        st.error(
            f"""
            ### ⚠ CONTROL EXCEPTION

            **{policy_violations}** ticket(s) contain both a refund
            and replacement.

            These records require review.
            """
        )

    # =====================================================
    # RECONCILIATION SUMMARY
    # =====================================================

    st.subheader("Reconciliation Summary")

    reconciliation = pd.DataFrame(
        {
            "Control": [
                "Migration duplicate IDs",
                "Paired refund rows",
                "Normalized legacy values",
                "Clean ticket rows",
                "Reconciled refund total"
            ],
            "Result": [
                "638",
                "250",
                "Yes",
                "11,600",
                f"₹{total_refund:,.0f}"
            ],
            "Status": [
                "IDENTIFIED",
                "MATCHED",
                "PASSED",
                "CREATED",
                "FINANCE READY"
            ]
        }
    )

    st.dataframe(
        reconciliation,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # RECONCILIATION LOGIC
    # =====================================================

    st.subheader("Reconciliation Logic")

    steps = [
        (
            "01",
            "Identify migration duplicates",
            "638 unique ticket IDs appeared across both source systems."
        ),
        (
            "02",
            "Normalize legacy monetary values",
            "Legacy refund values were converted to the current rupee scale."
        ),
        (
            "03",
            "Validate paired records",
            "250 paired refund rows matched after normalization."
        ),
        (
            "04",
            "Create clean dataset",
            "11,600 clean ticket rows remained for analysis."
        )
    ]

    for number, title, description in steps:

        with st.container(border=True):

            col1, col2 = st.columns([0.7, 5])

            with col1:

                st.markdown(
                    f"### {number}"
                )

            with col2:

                st.markdown(
                    f"**{title}**"
                )

                st.caption(
                    description
                )


# =========================================================
# BOARD ROOM
# =========================================================

elif page == "Board Room":

    st.header("Board Room")

    st.caption(
        "Executive view — what leadership needs to know."
    )

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    st.subheader(
        "Vireo Refund Intelligence — Executive Brief"
    )

    st.info(
        "Reconciled support-ticket analysis prepared for management reporting."
    )

    # =====================================================
    # BOARD KPIs
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Refund Value",
            f"₹{total_refund / 100000:.2f}L"
        )

    with c2:

        st.metric(
            "Refund Tickets",
            f"{refund_count:,}"
        )

    with c3:

        st.metric(
            "GW-OTHER Share",
            f"{gw_share:.1f}%"
        )

    with c4:

        st.metric(
            "Policy Violations",
            f"{policy_violations}"
        )

    st.divider()

    # =====================================================
    # KEY FINDINGS
    # =====================================================

    st.subheader("Key Findings")

    findings = [
        (
            "01",
            "Reconciled refund value",
            f"Total reconciled refunds are ₹{total_refund:,.0f}."
        ),
        (
            "02",
            "Peak refund month",
            "November 2025 was the peak refund month at approximately ₹5.76L."
        ),
        (
            "03",
            "GW-OTHER concentration",
            f"GW-OTHER represents {gw_share:.1f}% of total refund value."
        ),
        (
            "04",
            "Migration duplicates",
            "638 migration duplicate IDs were identified and reconciled."
        ),
        (
            "05",
            "Policy control",
            "No refund + replacement policy violations were detected."
        ),
        (
            "06",
            "AI finding",
            "AI validation indicates that GW-OTHER has poor classification quality."
        )
    ]

    for number, title, description in findings:

        with st.container(border=True):

            col1, col2 = st.columns([0.7, 5])

            with col1:

                st.markdown(
                    f"### {number}"
                )

            with col2:

                st.markdown(
                    f"**{title}**"
                )

                st.caption(
                    description
                )

    st.divider()

    # =====================================================
    # RECOMMENDED ACTIONS
    # =====================================================

    st.subheader("Recommended Actions")

    recommendations = [
        (
            "01",
            "Improve reason-code governance",
            "Require clearer reason-code selection and review GW-OTHER usage."
        ),
        (
            "02",
            "Keep reconciliation before reporting",
            "Do not use raw legacy export values for financial reporting."
        ),
        (
            "03",
            "Use AI as an audit layer",
            "Flag suspicious reason-code/text mismatches for human review."
        ),
        (
            "04",
            "Segment agent analysis",
            "Compare agents within comparable teams and tiers."
        )
    ]

    for number, title, description in recommendations:

        with st.container(border=True):

            col1, col2 = st.columns([0.7, 5])

            with col1:

                st.markdown(
                    f"### {number}"
                )

            with col2:

                st.markdown(
                    f"**{title}**"
                )

                st.caption(
                    description
                )

    st.divider()

    # =====================================================
    # BOARD DECISION
    # =====================================================

    st.subheader("Board Decision")

    st.success(
        """
        **The reconciled dataset is suitable for management reporting.**

        However, **GW-OTHER should not be treated as a reliable
        analytical category without additional reason-code governance.**

        The recommended operating model is:

        **Reconcile → Validate → AI Audit → Human Review → Report**
        """
    )

    # =====================================================
    # BOARD TAKEAWAY
    # =====================================================

    st.subheader("Executive Takeaway")

    st.markdown(
        """
        ### The financial dataset is under control.

        The main remaining data-quality risk is **reason-code accuracy**,
        particularly the heavy use of **GW-OTHER**.

        AI is most valuable here as an **audit and exception-detection
        layer**, rather than as an autonomous financial decision maker.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        VIREO AUDIO • REFUND INTELLIGENCE SYSTEM • APPLIED AI ANALYSIS
    </div>
    """,
    unsafe_allow_html=True
)