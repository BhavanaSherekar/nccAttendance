import streamlit as st
import pandas as pd
import os
from datetime import datetime
from attendance import take_attendance

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NCC Attendance System",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 28px;
    font-weight: 700;
}
.sub-text {
    text-align: center;
    color: #9aa0a6;
    font-size: 14px;
}
.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="main-title">NCC FACE RECOGNITION ATTENDANCE</div>
    <div class="sub-text">Attendance Management Portal</div>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- OPTION SELECTOR ----------------
option = st.radio(
    "",
    ["Take Attendance", "View Cadet List"],
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- TAKE ATTENDANCE ----------------
if option == "Take Attendance":
    st.markdown(
        """
        <div class="card">
            <div class="section-title">Take Attendance</div>
            <ul>
                <li>Ensure the cadet's face is clearly visible</li>
                <li>Attendance is marked automatically</li>
                <li>Press <b>Q</b> to close the camera</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Click the button below to start the camera")

    if st.button("START ATTENDANCE", use_container_width=True):
        st.success("Camera started. Marking attendance...")
        take_attendance()
        st.success("Attendance completed successfully")

# ---------------- VIEW CADET LIST ----------------
elif option == "View Cadet List":
    st.markdown(
        """
        <div class="card">
            <div class="section-title">Cadet Attendance List</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    date = datetime.now().strftime("%d-%m-%Y")
    file_path = f"Attendance/Attendance_{date}.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.dataframe(df, use_container_width=True)

        st.download_button(
            label="DOWNLOAD ATTENDANCE CSV",
            data=df.to_csv(index=False),
            file_name=f"Attendance_{date}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No attendance recorded for today.")
