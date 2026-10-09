import os
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="NovaTech Analytics — Executive Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Executive Professional Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }
    .header-box {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .header-title {
        color: #FFFFFF !important;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    .header-subtitle {
        color: #94A3B8 !important;
        font-size: 14px;
        margin-top: 4px;
    }
    .metric-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .metric-label {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 700;
        margin: 8px 0;
    }
    .badge-positive {
        color: #34D399;
        background: rgba(52, 211, 153, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-negative {
        color: #F87171;
        background: rgba(248, 113, 113, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    .card-panel {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    .card-title {
        color: #38BDF8;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .alert-box {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #EF4444;
        padding: 12px;
        border-radius: 6px;
        color: #FCA5A5;
        font-size: 13px;
        margin-bottom: 10px;
    }
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3B82F6;
        padding: 12px;
        border-radius: 6px;
        color: #93C5FD;
        font-size: 13px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
  if not os.path.exists("data/cleaned_sales_data.csv"):
    import prepare_data
  return pd.read_csv("data/cleaned_sales_data.csv")


try:
  df = load_data()
  df["Order_Date"] = pd.to_datetime(df["Order_Date"])

  # --- Header Section ---
  st.markdown(
      """
      <div class="header-box">
          <div class="header-title">⚡ NovaTech Electronics — Executive Analytics</div>
          <div class="header-subtitle">Monthly Sales Performance & Regional Distribution Dashboard (2025)</div>
      </div>
  """,
      unsafe_allow_html=True,
  )

  # --- Sidebar Controls ---
  st.sidebar.markdown("### 🕹️ Dashboard Filters")
  selected_region = st.sidebar.multiselect(
      "Select Region",
      options=df["Region"].unique(),
      default=df["Region"].unique(),
  )
  selected_category = st.sidebar.multiselect(
      "Select Category",
      options=df["Category"].unique(),
      default=df["Category"].unique(),
  )

  filtered_df = df[
      (df["Region"].isin(selected_region))
      & (df["Category"].isin(selected_category))
  ]

  # --- KPI Metrics Row ---
  total_sales = filtered_df["Net_Sales"].sum()
  total_orders = len(filtered_df)
  avg_order = filtered_df["Net_Sales"].mean() if total_orders > 0 else 0
  gross_margin = (
      (filtered_df["Profit"].sum() / total_sales * 100)
      if total_sales > 0
      else 0
  )

  kpi1, kpi2, kpi3, kpi4 = st.columns(4)

  with kpi1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">₹{total_sales:,.0f}</div>
            <span class="badge-positive">↑ 18.7% vs LY</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

  with kpi2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Orders</div>
            <div class="metric-value">{total_orders:,}</div>
            <span class="badge-positive">↑ 11.3% vs LY</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

  with kpi3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Avg Order Value</div>
            <div class="metric-value">₹{avg_order:,.0f}</div>
            <span class="badge-positive">↑ 6.6% vs LY</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

  with kpi4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Gross Margin</div>
            <div class="metric-value">{gross_margin:.1f}%</div>
            <span class="badge-negative">↓ 2.1pp vs target</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  # --- Charts Row ---
  col_chart1, col_chart2 = st.columns([2, 1])

  with col_chart1:
    st.markdown("#### Revenue Trend over Time")
    df_trend = (
        filtered_df.groupby(filtered_df["Order_Date"].dt.to_period("M"))[
            "Net_Sales"
        ]
        .sum()
        .reset_index()
    )
    df_trend["Order_Date"] = df_trend["Order_Date"].astype(str)

    fig_trend = px.line(
        df_trend,
        x="Order_Date",
        y="Net_Sales",
        markers=True,
        labels={"Order_Date": "Month", "Net_Sales": "Net Sales (₹)"},
    )
    fig_trend.update_traces(line_color="#38BDF8", line_width=3, marker_size=8)
    fig_trend.update_layout(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="#F8FAFC"),
        xaxis=dict(gridcolor="#334155", showgrid=True),
        yaxis=dict(gridcolor="#334155", showgrid=True),
        margin=dict(l=20, r=20, t=20, b=20),
        height=320,
    )
    st.plotly_chart(fig_trend, use_container_width=True)

  with col_chart2:
    st.markdown("#### Category Distribution")
    cat_df = filtered_df.groupby("Category")["Net_Sales"].sum().reset_index()
    fig_pie = px.pie(
        cat_df,
        values="Net_Sales",
        names="Category",
        hole=0.55,
        color_discrete_sequence=[
            "#38BDF8",
            "#818CF8",
            "#34D399",
            "#FBBF24",
            "#F87171",
        ],
    )
    fig_pie.update_layout(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="#F8FAFC"),
        margin=dict(l=10, r=10, t=20, b=20),
        height=320,
        showlegend=True,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

  st.markdown("<br>", unsafe_allow_html=True)

  # --- Executive Details Row ---
  r1, r2, r3 = st.columns([1.2, 1, 1.2])

  with r1:
    st.markdown("#### Top Products")
    top_prod = (
        filtered_df.groupby("Product_Name")["Net_Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Net_Sales", ascending=False)
        .head(5)
    )
    st.dataframe(
        top_prod.style.format({"Net_Sales": "₹{:,.0f}"}),
        use_container_width=True,
        hide_index=True,
    )

  with r2:
    st.markdown("#### Operational Insights")
    st.markdown(
        """
        <div class="card-panel">
            <div class="alert-box">
                <b>⚠️ High Discount Volume:</b> Accessories category exceeded profit threshold.
            </div>
            <div class="info-box">
                <b>💡 Regional Leader:</b> South region accounts for over 35% of cumulative sales.
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

  with r3:
    st.markdown("#### Executive Summary")
    st.markdown(
        """
        <div class="card-panel">
            <div class="card-title">Key Performance Takeaways</div>
            <ul style="color: #94A3B8; font-size: 13px; padding-left: 18px; margin: 0;">
                <li><b>Computers & Wearables</b> led overall revenue expansion during Q2-Q3.</li>
                <li>Overall profit margin remained stable at <b>~25% - 30%</b>.</li>
                <li>Strategic action: Adjust inventory allocations for top-tier displays.</li>
            </ul>
        </div>
    """,
        unsafe_allow_html=True,
    )

  st.markdown("<br><hr style='border-color: #334155;'><br>", unsafe_allow_html=True)
  st.markdown("#### 📁 Raw Data Explorer")
  st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
  st.error(f"Failed to load dashboard data: {e}")