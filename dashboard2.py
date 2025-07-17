import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data import df

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Dashboard")

# Apply all README changes in order

# === FILTERS SECTION ===
# Change 1: Replace text input with multiselect dropdown
# Change 2: Move product selection to sidebar
# Change 3: Add date range filter to sidebar
with st.sidebar:
    selected_products = st.multiselect("Select Products:", df['product_name'].unique(), default=["Product 1"])
    date_range = st.date_input("Date Range:", value=(df['date'].min(), df['date'].max()))

# Change 4: Update data filtering for multiple products
filtered_data = df[
    (df['product_name'].isin(selected_products)) &
    (df['date'] >= pd.to_datetime(date_range[0])) & 
    (df['date'] <= pd.to_datetime(date_range[1]))
]

# === CHARTS SECTION ===
# Change 1: Add chart type selector at the top
chart_type = st.selectbox("Chart Type:", ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot"])

# Change 2: Replace single chart type with conditional chart types
fig = go.Figure()
for product in selected_products:
    product_data = filtered_data[filtered_data['product_name'] == product]
    
    if chart_type == "Line Chart":
        fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['demand'], 
                                name=f'{product} - Demand', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['forecast'], 
                                name=f'{product} - Forecast', line=dict(color='blue')))
    elif chart_type == "Bar Chart":
        fig.add_trace(go.Bar(x=product_data['date'], y=product_data['demand'], 
                            name=f'{product} - Demand', marker_color='red'))
        fig.add_trace(go.Bar(x=product_data['date'], y=product_data['forecast'], 
                            name=f'{product} - Forecast', marker_color='blue'))
    elif chart_type == "Area Chart":
        fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['demand'], 
                                name=f'{product} - Demand', fill='tonexty', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['forecast'], 
                                name=f'{product} - Forecast', fill='tonexty', line=dict(color='blue')))
    elif chart_type == "Scatter Plot":
        fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['demand'], 
                                name=f'{product} - Demand', mode='markers', marker=dict(color='red', size=8)))
        fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['forecast'], 
                                name=f'{product} - Forecast', mode='markers', marker=dict(color='blue', size=8)))

# Change 3: Update chart title and add unique key
fig.update_layout(title=f'Products: {", ".join(selected_products)}', xaxis_title='Date', yaxis_title='Quantity', height=400, yaxis=dict(range=[0, None]))

# === LAYOUT SECTION ===
# Change 1: Create side-by-side layout for chart and data table (wider table)
col1, col2 = st.columns([1, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True, key="layout_chart")
with col2:
    # Format date column to show only date without time
    display_data = filtered_data.copy()
    display_data['date'] = display_data['date'].dt.date
    st.dataframe(display_data, use_container_width=True)
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="data.csv", mime="text/csv")

# Change 2: Move metrics below the chart and table across full width
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Demand", f"{filtered_data['demand'].sum():,.0f}")
with col2:
    st.metric("Total Forecast", f"{filtered_data['forecast'].sum():,.0f}")
with col3:
    st.metric("Average Demand", f"{filtered_data['demand'].mean():,.0f}")

show_stats = st.checkbox("Show Statistics", value=True)
if show_stats:
    with st.expander("Summary Statistics"):
        stats = filtered_data.groupby('product_name')[['demand', 'forecast']].agg(['sum', 'mean']).round(2)
        st.dataframe(stats) 