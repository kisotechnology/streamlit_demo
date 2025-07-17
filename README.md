# Streamlit Dashboard Demo

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start with the simple dashboard:
```bash
streamlit run dashboard.py
```

## Exercise 1: Add Multiple Product Selection

**Step 1**: Replace the product selection
- **DELETE these lines:**
```python
selected_product = st.text_input("Enter Product Name:", value="Product 1")
if selected_product not in df['product_name'].unique():
    st.error("Invalid product name. Please enter a valid product name.")
    st.stop()
```
- **ADD this sidebar code:**
```python
with st.sidebar:
    selected_products = st.multiselect("Select Products:", df['product_name'].unique(), default=["Product 1"])
```

**Step 2**: Update the data filtering
- **DELETE this line:**
```python
product_data = df[df['product_name'] == selected_product]
```
- **ADD this line:**
```python
filtered_data = df[df['product_name'].isin(selected_products)]
```

**Step 3**: Update the chart to show multiple products
- **DELETE these lines:**
```python
fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['demand'], name='Demand', line=dict(color='red')))
fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['forecast'], name='Forecast', line=dict(color='blue')))
```
- **ADD this loop:**
```python
for product in selected_products:
    product_subset = filtered_data[filtered_data['product_name'] == product]
    fig.add_trace(go.Scatter(x=product_subset['date'], y=product_subset['demand'], 
                            name=f'{product} - Demand', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=product_subset['date'], y=product_subset['forecast'],
                            name=f'{product} - Forecast', line=dict(color='blue')))
```

**Step 4**: Update the chart title
- **DELETE this line:**
```python
fig.update_layout(title=f'{selected_product}', xaxis_title='Date', yaxis_title='Demand (units)', height=400, yaxis=dict(range=[0, None]))
```
- **ADD this line:**
```python
fig.update_layout(title=f'Products: {", ".join(selected_products)}', xaxis_title='Date', yaxis_title='Quantity', height=400, yaxis=dict(range=[0, None]))
```

**Step 5**: Update the summary table
- **DELETE this code:**
```python
summary = pd.DataFrame({
    'Metric': ['Total Demand', 'Total Forecast', 'Avg Demand', 'Avg Forecast'],
    'Value': [product_data['demand'].sum(), product_data['forecast'].sum(), 
              product_data['demand'].mean(), product_data['forecast'].mean()]
})
st.table(summary)
```
- **ADD this code:**
```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Demand", f"{filtered_data['demand'].sum():,.0f}")
with col2:
    st.metric("Total Forecast", f"{filtered_data['forecast'].sum():,.0f}")
with col3:
    st.metric("Average Demand", f"{filtered_data['demand'].mean():,.0f}")
```

## Exercise 2: Add Date Range Filtering

**Goal**: Add date range selection to the sidebar

**Step 1**: Add date range to sidebar
- **FIND this line in the sidebar:**
```python
selected_products = st.multiselect("Select Products:", df['product_name'].unique(), default=["Product 1"])
```
- **ADD this line after it:**
```python
date_range = st.date_input("Date Range:", value=(df['date'].min(), df['date'].max()))
```

**Step 2**: Update data filtering to include date range
- **DELETE this line:**
```python
filtered_data = df[df['product_name'].isin(selected_products)]
```
- **ADD this line:**
```python
filtered_data = df[
    (df['product_name'].isin(selected_products)) &
    (df['date'] >= pd.to_datetime(date_range[0])) & 
    (df['date'] <= pd.to_datetime(date_range[1]))
]
```

## Exercise 3: Add Chart Type Selector

**Goal**: Add dropdown to switch between different chart types

**Step 1**: Add chart type selector
- **ADD this line before the chart creation:**
```python
chart_type = st.selectbox("Chart Type:", ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot"])
```

**Step 2**: Replace simple chart with conditional chart types
- **DELETE this chart loop:**
```python
for product in selected_products:
    product_subset = filtered_data[filtered_data['product_name'] == product]
    fig.add_trace(go.Scatter(x=product_subset['date'], y=product_subset['demand'], 
                            name=f'{product} - Demand', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=product_subset['date'], y=product_subset['forecast'],
                            name=f'{product} - Forecast', line=dict(color='blue')))
```
- **ADD this conditional chart code:**
```python
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
```

## Exercise 4: Add Interactive Data Table

**Goal**: Replace summary table with interactive data table and download functionality

**Step 1**: Remove the old summary table
- **DELETE this code:**
```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Demand", f"{filtered_data['demand'].sum():,.0f}")
with col2:
    st.metric("Total Forecast", f"{filtered_data['forecast'].sum():,.0f}")
with col3:
    st.metric("Average Demand", f"{filtered_data['demand'].mean():,.0f}")
```

**Step 2**: Add interactive data table
- **ADD this code:**
```python
# Format date column to show only date without time
display_data = filtered_data.copy()
display_data['date'] = display_data['date'].dt.date
st.dataframe(display_data, use_container_width=True)
```

**Step 3**: Add download functionality
- **ADD this code after the dataframe:**
```python
csv = filtered_data.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name="data.csv", mime="text/csv")
```

## Exercise 5: Create Professional Layout

**Goal**: Organize chart and table side by side, with metrics below

**Step 1**: Create side-by-side layout
- **DELETE this line:**
```python
st.plotly_chart(fig, use_container_width=True)
```
- **DELETE this code:**
```python
# Format date column to show only date without time
display_data = filtered_data.copy()
display_data['date'] = display_data['date'].dt.date
st.dataframe(display_data, use_container_width=True)
csv = filtered_data.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name="data.csv", mime="text/csv")
```
- **ADD this layout code:**
```python
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
```

**Step 2**: Add metrics section below
- **ADD this code after the layout:**
```python
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Demand", f"{filtered_data['demand'].sum():,.0f}")
with col2:
    st.metric("Total Forecast", f"{filtered_data['forecast'].sum():,.0f}")
with col3:
    st.metric("Average Demand", f"{filtered_data['demand'].mean():,.0f}")
```

**Step 3**: Add expandable statistics
- **ADD this code after the metrics:**
```python
show_stats = st.checkbox("Show Statistics", value=True)
if show_stats:
    with st.expander("Summary Statistics"):
        stats = filtered_data.groupby('product_name')[['demand', 'forecast']].agg(['sum', 'mean']).round(2)
        st.dataframe(stats)
```


