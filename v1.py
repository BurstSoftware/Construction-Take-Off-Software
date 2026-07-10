# streamlit run takeoff_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Construction Takeoff Software", layout="wide")

st.title("🏗️ Construction Takeoff Software")

# ----------------------
# PROJECT DETAILS
# ----------------------
st.header("1. Project Details")

project_name = st.text_input("Project Name")
client_name = st.text_input("Client Name")
project_location = st.text_input("Project Location")
project_type = st.selectbox("Project Type", ["Residential", "Commercial", "Industrial", "Other"])
start_date = st.date_input("Start Date")

# ----------------------
# PLAN UPLOAD
# ----------------------
st.header("2. Upload Project Drawings")
plan_files = st.file_uploader(
    "Upload PDF, DWG, or Image Plans",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

scale = st.text_input("Drawing Scale (e.g., 1/8” = 1’-0”)")
plan_type = st.selectbox("Plan Type", ["Architectural", "Structural", "MEP", "Other"])

# ----------------------
# MATERIAL INPUT TABLE
# ----------------------
st.header("3. Material Inputs")

material_data = st.data_editor(
    pd.DataFrame({
        "Material": ["Concrete", "Drywall", "Rebar"],
        "Unit": ["m³", "ft²", "ft"],
        "Quantity": [0, 0, 0],
        "Unit Cost": [150, 2.5, 0.8],
        "Waste Factor (%)": [5, 10, 3]
    }),
    num_rows="dynamic",
    use_container_width=True
)

# ----------------------
# CALCULATE COST
# ----------------------
st.header("4. Calculation Output")

if st.button("Generate Takeoff Summary"):
    df = material_data.copy()
    df["Waste Qty"] = df["Quantity"] * (df["Waste Factor (%)"] / 100)
    df["Total Qty"] = df["Quantity"] + df["Waste Qty"]
    df["Total Cost"] = df["Total Qty"] * df["Unit Cost"]

    st.subheader("📊 Takeoff Summary")
    st.dataframe(df, use_container_width=True)

    st.subheader("💰 Total Project Cost")
    st.metric("Estimated Cost", f"${df['Total Cost'].sum():,.2f}")

# ----------------------
# EXPORT
# ----------------------
st.header("5. Export Options")
export_format = st.selectbox("Export Format", ["CSV", "Excel"])
if st.button("Export Data"):
    if export_format == "CSV":
        df.to_csv("takeoff_output.csv", index=False)
        st.success("CSV Exported Successfully!")
        st.download_button("Download CSV", df.to_csv(index=False), "takeoff_output.csv")
    else:
        df.to_excel("takeoff_output.xlsx", index=False)
        st.success("Excel File Exported Successfully!")
        st.download_button("Download Excel", df.to_excel(index=False), "takeoff_output.xlsx")
