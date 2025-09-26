import streamlit as st
import pandas as pd

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Attendance Dashboard 📊",
    page_icon="📘",
    layout="centered",
)

# -------------------------------
# Header
# -------------------------------
st.markdown("""
# 📘 Attendance Dashboard
Track your attendance, plan your classes, and stay on target!
""", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# Input section
# -------------------------------
st.subheader("📝 Enter Your Details")
col1, col2 = st.columns(2)

with col1:
    attended = st.number_input("Classes Attended", min_value=0, step=1, value=0)
    target_percentage = st.number_input(
        "Your Target (%)", min_value=1, max_value=100, value=75, step=1
    )

with col2:
    total = st.number_input("Total Classes", min_value=1, step=1, value=1)
    future_classes = st.number_input(
        "Upcoming Classes to Project", min_value=1, step=1, value=10
    )

st.markdown("---")

# -------------------------------
# Calculations and metrics
# -------------------------------
if total > 0:
    percentage = (attended / total) * 100

    # Display current attendance and target using Streamlit metrics
    st.subheader("📊 Current Attendance")
    col1, col2 = st.columns(2)
    col1.metric("Current %", f"{percentage:.2f}%")
    col2.metric("Target %", f"{target_percentage}%")

    # Eligibility status
    if percentage >= target_percentage:
        st.success(f"🎉 You are above your target of {target_percentage}%!")
    else:
        st.error(f"⚠️ You are below your target of {target_percentage}%.")

    # -------------------------------
    # Predictions section
    # -------------------------------
    st.subheader("📅 Predictions")
    col1, col2 = st.columns(2)

    # Classes needed to reach target
    with col1:
        if percentage < target_percentage:
            needed = 0
            future_attended = attended
            future_total = total
            while (future_attended / future_total) * 100 < target_percentage:
                needed += 1
                future_attended += 1
                future_total += 1
            st.metric("Classes Needed ✅", needed, f"Attend consecutively to reach {target_percentage}%")
        else:
            st.metric("Great Job! 🎉", "Above target!", f"Current: {percentage:.2f}%")

    # Classes you can afford to miss
    with col2:
        if percentage >= target_percentage:
            can_miss = 0
            future_attended = attended
            future_total = total
            while (future_attended / future_total) * 100 >= target_percentage:
                can_miss += 1
                future_total += 1
            can_miss -= 1
            st.metric("Classes You Can Miss ⚠️", can_miss, f"Still maintain {target_percentage}%")
        else:
            st.metric("Attention ❌", "Below target", f"Attend more classes to reach {target_percentage}%")

    # -------------------------------
    # Attendance projection chart (Streamlit native)
    # -------------------------------
    st.subheader("📈 Attendance Projection")

    data = {
        "Scenario": ["Current %", "Target %", f"{future_classes} Attend All", f"{future_classes} Miss All"],
        "Percentage": [
            percentage,
            target_percentage,
            (attended + future_classes) / (total + future_classes) * 100,
            attended / (total + future_classes) * 100
        ]
    }

    df = pd.DataFrame(data).set_index("Scenario")
    st.bar_chart(df, height=400)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown('Made with ❤️ using Streamlit', unsafe_allow_html=True)