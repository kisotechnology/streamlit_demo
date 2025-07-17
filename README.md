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

1. Change text input to dropdown selector
   - Replace `st.text_input()` with `st.selectbox("Select Product:", df['product_name'].unique())`
   ```python
   selected_product = st.selectbox("Select Product:", df['product_name'].unique())
   ```

2. Add a sidebar with filters
   - Use `st.sidebar.selectbox()` to move product selection to sidebar
   ```python
   with st.sidebar:
       selected_product = st.selectbox("Select Product:", df['product_name'].unique())
   ```

3. Add multiple selection
   - Change to `st.multiselect()` to show multiple products at once
   - Update chart to display all selected products
   ```python
   selected_products = st.multiselect("Select Products:", df['product_name'].unique())
   # Then loop through selected_products in your chart
   for product in selected_products:
       product_data = df[df['product_name'] == product]
       # Add chart traces for each product
   ```

4. Add date range filter
   - Add `st.date_input()` in sidebar for date filtering
   - Filter data based on selected date range
   ```python
   date_range = st.date_input("Date Range:", value=(df['date'].min(), df['date'].max()))
   filtered_data = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]
   ```

5. Change line chart to bar chart
   - Replace `go.Scatter()` with `go.Bar()`
   - Add `barmode='group'` to layout
   ```python
   fig.add_trace(go.Bar(x=dates, y=values, name='Data'))
   fig.update_layout(barmode='group')
   ```

6. Add different chart types
   - Create area chart with `go.Scatter(fill='tonexty')`
   - Add scatter plot with `go.Scatter(mode='markers')`
   ```python
   # Area chart
   fig.add_trace(go.Scatter(x=dates, y=values, fill='tonexty'))
   # Scatter plot
   fig.add_trace(go.Scatter(x=dates, y=values, mode='markers'))
   ```

7. Customize chart styling
   - Change colors: `line=dict(color='green')`
   - Add markers: `mode='lines+markers'`
   - Add color scheme selector
   ```python
   fig.add_trace(go.Scatter(x=dates, y=values, line=dict(color='green'), mode='lines+markers'))
   color_scheme = st.selectbox("Color Scheme:", ["Default", "Dark", "Light"])
   ```

8. Add metric
   - Create metrics cards with `st.metric()`
   - Display trend indicators (up/down arrows)
   ```python
   col1, col2, col3 = st.columns(3)
   with col1:
       st.metric("Total Demand", f"{total_demand:,.0f}")
   with col2:
       st.metric("Total Forecast", f"{total_forecast:,.0f}")
   ```

9. Add data table
   - Use `st.dataframe()` to show raw data
   - Add sorting and filtering capabilities
   ```python
   st.dataframe(filtered_data, use_container_width=True)
   ```

10. Add download functionality
   - Use `st.download_button()` to export data as CSV
   - Allow downloading filtered data
   ```python
   csv = filtered_data.to_csv(index=False)
   st.download_button(label="Download CSV", data=csv, file_name="data.csv", mime="text/csv")
   ```

11. Improve layout
    - Use `st.columns()` for side-by-side elements
    - Add `st.expander()` for collapsible sections
   ```python
   col1, col2 = st.columns(2)
   with col1:
       # content for left column
   with st.expander("Click to expand"):
       # collapsible content
   ```

12. Add sliders and inputs
    - Date range slider with `st.slider()`
    - Number input for threshold values
    - Checkbox for toggling features
   ```python
   threshold = st.slider("Threshold:", min_value=0, max_value=1000, value=500)
   show_metrics = st.checkbox("Show Metrics", value=True)
   ```

13. Add conditional display
    - Show/hide elements based on user input
    - Use `st.checkbox()` to toggle chart types
   ```python
   if show_metrics:
       st.metric("Value", value)
   ```

14. Add chart type selector
    - Create dropdown to switch between line, bar, area, scatter charts
    - Update chart rendering based on selection
   ```python
   chart_type = st.selectbox("Chart Type:", ["Line", "Bar", "Area", "Scatter"])
   if chart_type == "Line":
       fig.add_trace(go.Scatter(x=dates, y=values))
   elif chart_type == "Bar":
       fig.add_trace(go.Bar(x=dates, y=values))
   ```

15. Add summary statistics
    - Create expandable section with demand and forecast statistics
    - Show aggregated data by product
   ```python
   with st.expander("Summary Statistics"):
       stats = filtered_data.groupby('product_name').agg(['sum', 'mean']).round(2)
       st.dataframe(stats)
   ```



```
