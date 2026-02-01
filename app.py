# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Affordable Student Living & Travel in Germany")
st.markdown("Explore cost of living, rent, transport, and meal expenses across major German cities.")

# Load data
df = pd.read_csv("cities_living_cost.csv")

# Filter German cities
german_cities = [
    'Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne', 'Bonn',
    'Dusseldorf', 'Stuttgart', 'Leipzig', 'Dresden', 'Nuremberg',
    'Hannover', 'Bremen', 'Essen', 'Dortmund'
]
df_germany = df[df['City'].isin(german_cities)].reset_index(drop=True)

# Student-focused dataframe
student_cols = [
    'City',
    'Cost_index',
    'Meal, Inexpensive Restaurant',
    'Monthly Pass (Regular Price)',
    'Apartment (1 bedroom) Outside of Centre',
    'Cinema, International Release, 1 Seat'
]
df_students = df_germany[student_cols]

# Compute Total Student Cost
df_students['Total_Student_Cost'] = (
    df_students['Apartment (1 bedroom) Outside of Centre'] +
    df_students['Meal, Inexpensive Restaurant'] * 30 +
    df_students['Monthly Pass (Regular Price)']
)

# --- Sidebar for Interactivity ---
st.sidebar.header("Filters")

# Dropdown to select city
selected_city = st.sidebar.selectbox("Select a city", df_students['City'])

# Slider for Total Student Cost
min_cost = int(df_students['Total_Student_Cost'].min())
max_cost = int(df_students['Total_Student_Cost'].max())
cost_filter = st.sidebar.slider("Filter by Total Student Cost (€)", min_cost, max_cost, (min_cost, max_cost))

# Filter dataframe based on slider
filtered_df = df_students[
    (df_students['Total_Student_Cost'] >= cost_filter[0]) &
    (df_students['Total_Student_Cost'] <= cost_filter[1])
]

# --- Main Dashboard ---

st.subheader(f"Cost Overview for {selected_city}")
city_data = df_students[df_students['City'] == selected_city].iloc[0]

st.write(f"**Cost of Living Index:** {city_data['Cost_index']}")
st.write(f"**Monthly Rent:** €{city_data['Apartment (1 bedroom) Outside of Centre']}")
st.write(f"**Monthly Transport:** €{city_data['Monthly Pass (Regular Price)']}")
st.write(f"**Meal Cost (Inexpensive Restaurant):** €{city_data['Meal, Inexpensive Restaurant']}")
st.write(f"**Cinema Ticket:** €{city_data['Cinema, International Release, 1 Seat']}")
st.write(f"**Estimated Total Monthly Student Cost:** €{city_data['Total_Student_Cost']}")

# --- Visualization 1: Total Student Cost Bar Chart ---
st.subheader("Total Student Cost Across German Cities")
plt.figure(figsize=(10,5))
plt.bar(filtered_df['City'], filtered_df['Total_Student_Cost'])
plt.xticks(rotation=45)
plt.ylabel('Total Monthly Student Cost (€)')
plt.xlabel('City')
plt.tight_layout()
st.pyplot(plt)

# --- Visualization 2: Rent Comparison ---
st.subheader("Monthly Rent Comparison")
plt.figure(figsize=(10,5))
plt.bar(filtered_df['City'], filtered_df['Apartment (1 bedroom) Outside of Centre'])
plt.xticks(rotation=45)
plt.ylabel('Monthly Rent (€)')
plt.xlabel('City')
plt.tight_layout()
st.pyplot(plt)

# --- Visualization 3: Transport Cost Comparison ---
st.subheader("Monthly Transport Cost Comparison")
plt.figure(figsize=(10,5))
plt.bar(filtered_df['City'], filtered_df['Monthly Pass (Regular Price)'])
plt.xticks(rotation=45)
plt.ylabel('Monthly Transport (€)')
plt.xlabel('City')
plt.tight_layout()
st.pyplot(plt)

# Optional: Add Rent vs Transport Scatter Plot
st.subheader("Rent vs Transport Costs")
plt.figure(figsize=(8,5))
plt.scatter(filtered_df['Apartment (1 bedroom) Outside of Centre'],
            filtered_df['Monthly Pass (Regular Price)'])
for i, city in enumerate(filtered_df['City']):
    plt.text(
        filtered_df['Apartment (1 bedroom) Outside of Centre'].iloc[i],
        filtered_df['Monthly Pass (Regular Price)'].iloc[i],
        city,
        fontsize=8,
        ha='right'
    )
plt.xlabel('Monthly Rent (€)')
plt.ylabel('Monthly Transport (€)')
plt.tight_layout()
st.pyplot(plt)

