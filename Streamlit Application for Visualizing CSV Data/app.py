import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def main():
    st.title("CSV Data Visualizer")
    st.write("Upload your CSV file and create interactive visualizations")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            # Display raw data
            st.subheader("Raw Data Preview")
            st.dataframe(df.head())
            
            # Data info
            st.subheader("Dataset Info")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Number of rows: {df.shape[0]}")
            with col2:
                st.write(f"Number of columns: {df.shape[1]}")
            
            # Visualization options
            st.subheader("Create Visualization")
            
            # Select chart type
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Line Chart", "Bar Chart", "Histogram", "Scatter Plot"]
            )
            
            # Get numerical columns
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            
            if chart_type in ["Line Chart", "Bar Chart"]:
                x_col = st.selectbox("Select X-axis column", df.columns)
                y_col = st.selectbox("Select Y-axis column", numeric_cols)
                
                if chart_type == "Line Chart":
                    fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                else:  # Bar Chart
                    fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                
            elif chart_type == "Histogram":
                col = st.selectbox("Select column for histogram", numeric_cols)
                bins = st.slider("Number of bins", min_value=5, max_value=50, value=20)
                fig = px.histogram(df, x=col, nbins=bins, title=f"Histogram of {col}")
                
            else:  # Scatter Plot
                x_col = st.selectbox("Select X-axis column", numeric_cols)
                y_col = st.selectbox("Select Y-axis column", numeric_cols)
                color_col = st.selectbox("Select color column (optional)", ["None"] + list(df.columns))
                
                if color_col == "None":
                    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                else:
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col} by {color_col}")
            
            # Display the plot
            st.plotly_chart(fig)
            
            # Basic statistics
            if st.checkbox("Show basic statistics"):
                st.subheader("Basic Statistics")
                st.write(df.describe())

if __name__ == "__main__":
    main()