# Streamlit Dashboard Demo

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
streamlit run dashboard.py
```

## Sample Exercises

1. Filters
   - Change text input to dropdown selector
   - Add sidebar with multiple product selection
   - Add date range filtering
   - Filter data based on selections
   ```python
   with st.sidebar:
       selected_products = st.multiselect("Select Products:", df['product_name'].unique())
       date_range = st.date_input("Date Range:", value=(df['date'].min(), df['date'].max()))
   
   filtered_data = df[
       (df['product_name'].isin(selected_products)) &
       (df['date'] >= date_range[0]) & 
       (df['date'] <= date_range[1])
   ]
   ```

2. Charts
   - Create chart type selector (line, bar, area, scatter)
   - Add multiple chart types with conditional rendering
   - Customize styling and colors
   ```python
   chart_type = st.selectbox("Chart Type:", ["Line", "Bar", "Area", "Scatter"])
   
   fig = go.Figure()
   for product in selected_products:
       product_data = filtered_data[filtered_data['product_name'] == product]
       
       if chart_type == "Line":
           fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['demand'], 
                                   name=f'{product} - Demand', line=dict(color='red')))
       elif chart_type == "Bar":
           fig.add_trace(go.Bar(x=product_data['date'], y=product_data['demand'], 
                               name=f'{product} - Demand', marker_color='red'))
   ```

3. *Metrics
   - Create metrics cards with key statistics
   - Add sliders and checkboxes for interactive controls
   - Show/hide elements based on user input
   - Display summary statistics
   ```python
   col1, col2, col3 = st.columns(3)
   with col1:
       st.metric("Total Demand", f"{filtered_data['demand'].sum():,.0f}")
   with col2:
       st.metric("Total Forecast", f"{filtered_data['forecast'].sum():,.0f}")
   
   show_stats = st.checkbox("Show Statistics", value=True)
   if show_stats:
       with st.expander("Summary Statistics"):
           stats = filtered_data.groupby('product_name').agg(['sum', 'mean']).round(2)
           st.dataframe(stats)
   ```

4. Data Table
   - Add interactive data table with sorting
   - Create download functionality for filtered data
   ```python
   st.dataframe(filtered_data, use_container_width=True)
   
   csv = filtered_data.to_csv(index=False)
   st.download_button(label="Download CSV", data=csv, file_name="data.csv", mime="text/csv")
   ```

5. Layout
   - Use columns for side-by-side elements
   - Add expandable sections for better organization
   - Create professional dashboard layout
   ```python
   col1, col2 = st.columns([2, 1])
   with col1:
       st.plotly_chart(fig, use_container_width=True)
   with col2:
       with st.expander("Filters"):
           # filter controls
       with st.expander("Metrics"):
           # metric cards
   ```



```
