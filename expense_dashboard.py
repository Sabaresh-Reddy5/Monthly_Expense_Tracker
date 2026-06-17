import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")

df = pd.read_csv("expense_data_1.csv")

expenses = df[df["Income/Expense"] == "Expense"].copy()

expenses["Date"] = pd.to_datetime(expenses["Date"])
expenses["Month"] = expenses["Date"].dt.month_name()

category_report = expenses.groupby("Category")["Amount"].sum()

monthly_report = (
    expenses.groupby(expenses["Date"].dt.month)["Amount"]
    .sum()
    .sort_index()
)

income_total = df[df["Income/Expense"] == "Income"]["Amount"].sum()
expense_total = expenses["Amount"].sum()
net_savings = income_total - expense_total

month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

highest_month_num = monthly_report.idxmax()
lowest_month_num = monthly_report.idxmin()

highest_month = month_names[highest_month_num]
lowest_month = month_names[lowest_month_num]

top_category = category_report.idxmax()

st.title("💰 Expense Tracker Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Income", f"₹{income_total:,.0f}")
col2.metric("Total Expense", f"₹{expense_total:,.0f}")
col3.metric("Net Savings", f"₹{net_savings:,.0f}")
col4.metric("Top Category", top_category)

st.subheader("Monthly Expense Report")

monthly_df = pd.DataFrame({
    "Month": [month_names[m] for m in monthly_report.index],
    "Amount": monthly_report.values
})

st.dataframe(monthly_df, use_container_width=True)

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.bar(monthly_df["Month"], monthly_df["Amount"])
ax1.set_title("Monthly Expenses")
plt.xticks(rotation=45)

st.pyplot(fig1)

st.subheader("Category-wise Spending")

category_df = pd.DataFrame({
    "Category": category_report.index,
    "Amount": category_report.values
})

st.dataframe(category_df, use_container_width=True)

fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.pie(
    category_df["Amount"],
    labels=category_df["Category"],
    autopct="%1.1f%%"
)

st.pyplot(fig2)

st.subheader("Insights")

st.write(f"Highest Spending Month : **{highest_month}**")
st.write(f"Lowest Spending Month : **{lowest_month}**")
st.write(f"Top Spending Category : **{top_category}**")

st.subheader("Annual Dashboard Summary")

summary = pd.DataFrame({
    "Metric": [
        "Total Income",
        "Total Expense",
        "Net Savings",
        "Average Monthly Spend",
        "Highest Spending Month",
        "Lowest Spending Month",
        "Top Spending Category"
    ],
    "Value": [
        f"₹{income_total:,.0f}",
        f"₹{expense_total:,.0f}",
        f"₹{net_savings:,.0f}",
        f"₹{expense_total/12:,.2f}",
        highest_month,
        lowest_month,
        top_category
    ]
})

st.table(summary)
