# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from utils import train_category_model, predict_missing_categories
from sqlalchemy import create_engine
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# -----------------------
# Page setup
# -----------------------
st.set_page_config(page_title="AI Expense Tracker", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4B0082;'>💰 AI-Powered Expense Tracker</h1>", unsafe_allow_html=True)

# -----------------------
# Load Data
# -----------------------
uploaded_file = st.file_uploader("📂 Upload Expense CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using generated sample data...")
    df = pd.read_csv("sample_expenses.csv")

# Convert Date column and add Month
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# -----------------------
# AI Category Prediction
# -----------------------
model, vectorizer = train_category_model(df.copy())
df = predict_missing_categories(df, model, vectorizer)

# -----------------------
# Save to SQLite
# -----------------------
engine = create_engine("sqlite:///expenses.db")
df.to_sql("expenses", engine, if_exists="replace", index=False)
df = pd.read_sql("expenses", engine)
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")
selected_categories = st.sidebar.multiselect("Categories", df['Category'].unique(), default=df['Category'].unique())
df = df[df['Category'].isin(selected_categories)]

min_amount, max_amount = int(df['Amount'].min()), int(df['Amount'].max())
amount_range = st.sidebar.slider("Filter by Amount", min_value=min_amount, max_value=max_amount, value=(min_amount,max_amount))
df = df[(df['Amount']>=amount_range[0]) & (df['Amount']<=amount_range[1])]

months = ["All"] + sorted(df['Month'].unique().tolist())
selected_month = st.sidebar.selectbox("Month", months)
if selected_month != "All":
    df = df[df['Month'] == selected_month]

# -----------------------
# Summary Metrics
# -----------------------
total = df['Amount'].sum()
avg = df['Amount'].mean()
top_cat = df.groupby('Category')['Amount'].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("Total Spent", f"₹{total:,.0f}", delta=f"₹{total-avg:,.0f}", delta_color="inverse")
col2.metric("Average Transaction", f"₹{avg:,.0f}", delta_color="normal")
col3.metric("Top Category", top_cat)

# -----------------------
# Tabs Layout
# -----------------------
tab1, tab2, tab3 = st.tabs(["Dashboard", "Insights", "Prediction"])

# -----------------------
# Tab1: Dashboard
# -----------------------
with tab1:
    st.subheader("📊 Spending Charts")
    
    # Pie Chart by Category
    cat_data = df.groupby('Category')['Amount'].sum().reset_index()
    fig1 = px.pie(cat_data, names='Category', values='Amount', title="Spending by Category",
                  color='Category', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Line Chart Monthly Trend
    month_data = df.groupby('Month')['Amount'].sum().reset_index()
    fig2 = px.line(month_data, x='Month', y='Amount', markers=True, title="Monthly Spending Trend",
                   color_discrete_sequence=["#4B0082"])
    st.plotly_chart(fig2, use_container_width=True)
    
    # Weekly Spending
    df['Week'] = df['Date'].dt.isocalendar().week
    weekly = df.groupby('Week')['Amount'].sum().reset_index()
    fig_week = px.bar(weekly, x='Week', y='Amount', title="Weekly Spending",
                      color='Amount', color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig_week)
    
    # Category Trends Over Time
    category_trends = df.groupby(['Month','Category'])['Amount'].sum().reset_index()
    fig_trend = px.line(category_trends, x='Month', y='Amount', color='Category', title="Category Trends Over Time",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_trend)

# -----------------------
# Tab2: AI Insights
# -----------------------
with tab2:
    st.subheader("🤖 AI Insights Summary")
    
    # Monthly comparison
    monthly_category = df.groupby(['Month','Category'])['Amount'].sum().reset_index()
    months_sorted = sorted(df['Month'].unique())
    if len(months_sorted) > 1:
        last_month = months_sorted[-2]
        current_month = months_sorted[-1]

        prev = monthly_category[monthly_category['Month']==last_month].set_index('Category')['Amount']
        curr = monthly_category[monthly_category['Month']==current_month].set_index('Category')['Amount']

        for cat in curr.index:
            prev_val = prev.get(cat, 0)
            change = ((curr[cat]-prev_val)/prev_val*100) if prev_val else 100
            st.metric(label=f"{cat} Spending Change", value=f"₹{curr[cat]:,.0f}", delta=f"{change:.0f}%")
    
    # Top 3 categories overall
    top3 = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(3)
    st.write("🏆 Top 3 Categories Overall:")
    for i, (cat, amt) in enumerate(top3.items(),1):
        st.write(f"{i}. {cat}: ₹{amt:,.0f}")

# -----------------------
# Tab3: Prediction
# -----------------------
with tab3:
    st.subheader("🧠 Predict Next Month Spending")
    
    month_data['Month_Num'] = np.arange(len(month_data))
    X = month_data[['Month_Num']]
    y = month_data['Amount']
    ml_model = LinearRegression()
    ml_model.fit(X, y)
    pred_next = ml_model.predict([[len(month_data)]])[0]
    st.success(f"Predicted Spending for Next Month: ₹{pred_next:,.0f}")

    # Plot actual vs predicted
    fig3, ax = plt.subplots()
    ax.plot(month_data['Month_Num'], y, marker='o', label='Actual', color="#4B0082")
    ax.plot(len(month_data), pred_next, 'r*', markersize=15, label='Predicted')
    ax.legend()
    st.pyplot(fig3)

# -----------------------
# PDF Report Download
# -----------------------
def create_pdf(df, filename="Expense_Report.pdf"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "💰 AI Expense Tracker - Report")
    
    y = 720
    for i, row in df.iterrows():
        line = f"{row['Date'].strftime('%Y-%m-%d')} | {row['Description']} | {row['Category']} | ₹{row['Amount']}"
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    buffer.seek(0)
    return buffer

pdf = create_pdf(df)
st.download_button("📄 Download PDF Report", pdf, file_name="Expense_Report.pdf", mime="application/pdf")
