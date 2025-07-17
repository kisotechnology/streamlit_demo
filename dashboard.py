import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data import df

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Dashboard")

st.sidebar.text("sidebar")

#selected_product = st.selectbox("Select Product:", df['product_name'].unique())
selected_product = st.text_input("Enter Product Name:", value=df['product_name'].unique()[0])
if selected_product not in df['product_name'].unique():
    st.error("Invalid product name. Please enter a valid product name.")
    st.stop()
product_data = df[df['product_name'] == selected_product]

fig = go.Figure()
fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['demand'], name='Demand', line=dict(color='red')))
fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['forecast'], name='Forecast', line=dict(color='blue')))
fig.update_layout(title=f'{selected_product}', xaxis_title='Date', yaxis_title='Quantity', height=400)

st.plotly_chart(fig, use_container_width=True)

summary = pd.DataFrame({
    'Metric': ['Total Demand', 'Total Forecast', 'Avg Demand', 'Avg Forecast'],
    'Value': [product_data['demand'].sum(), product_data['forecast'].sum(), 
              product_data['demand'].mean(), product_data['forecast'].mean()]
})
st.table(summary)
