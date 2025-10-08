"""
Streamlit Web Application for Vehicle Detection and Counting System
Optimized for Cloud Deployment (Instant Loading)
"""

import streamlit as st
import os
import pandas as pd
from PIL import Image

# --------------------------------------------
# Lazy Import - heavy modules are imported later
# --------------------------------------------

def lazy_import_detection():
    """Import the heavy detection module only when needed."""
    global VehicleDetectionSystem
    from main import VehicleDetectionSystem


# ======================================================
# DEMO DISPLAY
# ======================================================
def show_demo_results():
    st.header("📊 Results Showcase")

    video_path = "outputs/processed_video.mp4"
    if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
        st.subheader("🎥 Demo Processed Video")
        with open(video_path, "rb") as v:
            st.video(v.read())
    else:
        st.info("Demo video not found. Run locally to generate `outputs/processed_video.mp4`")

    # Download buttons
    st.subheader("💾 Download Results")
    c1, c2, c3 = st.columns(3)
    with c1:
        if os.path.exists("outputs/traffic_data.csv"):
            with open("outputs/traffic_data.csv", "rb") as f:
                st.download_button("📊 Download CSV", f, file_name="traffic_data.csv")
    with c2:
        if os.path.exists("outputs/processed_video.mp4"):
            with open("outputs/processed_video.mp4", "rb") as f:
                st.download_button("🎥 Download Video", f, file_name="processed_video.mp4")
    with c3:
        if os.path.exists("outputs/analysis_summary.txt"):
            with open("outputs/analysis_summary.txt", "rb") as f:
                st.download_button("📝 Download Summary", f, file_name="analysis_summary.txt")

    # Chart + Summary
    st.subheader("📈 Analysis Overview")
    col1, col2 = st.columns([1.3, 0.7])
    with col1:
        if os.path.exists("outputs/traffic_plot.png"):
            st.image("outputs/traffic_plot.png", caption="Traffic Flow Chart", use_column_width=True)
    with col2:
        if os.path.exists("outputs/analysis_summary.txt"):
            with open("outputs/analysis_summary.txt", "r", encoding="utf-8") as f:
                st.text_area("Summary", f.read(), height=400, disabled=True)
        else:
            st.text_area("Summary", "Demo summary unavailable.", height=400, disabled=True)


# ======================================================
# UPLOAD & ANALYSIS INTERFACE
# ======================================================
def show_upload_interface(uploaded_file, model_option):
    st.info("⚠️ Online demo shows precomputed results. For full YOLO processing, run locally with GPU.")

    if uploaded_file:
        st.success(f"✅ Video uploaded: {uploaded_file.name}")
        if st.button("🚀 Start Analysis", type="primary"):
            with st.spinner("🔄 Processing..."):
                lazy_import_detection()  # Import YOLO only when needed
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                try:
                    detector = VehicleDetectionSystem(model_path=model_option)
                    df, cat_counts = detector.detect_and_count(temp_path)
                    detector.save_results(df, cat_counts)
                    st.success("🎉 Analysis completed!")
                    st.metric("Total Vehicles", int(df['total'].sum()))
                    st.metric("Peak Traffic/sec", int(df['total'].max()))
                    st.metric("Avg Traffic/sec", f"{df['total'].mean():.1f}")
                except Exception as e:
                    st.error(f"❌ Error during analysis: {e}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
    else:
        st.info("👆 Upload a traffic video file to begin analysis.")


# ======================================================
# MAIN APP
# ======================================================
def main():
    st.set_page_config(page_title="Vehicle Detection & Counter", page_icon="🚗", layout="wide")
    st.title("🚗 Vehicle Detection & Counter")
    st.markdown("---")

    # Default landing view
    view_mode = st.radio(
        "Select Mode",
        ["🎯 View Demo Results", "🚀 Upload & Process (Local/GPU Recommended)"],
        horizontal=True
    )

    if view_mode == "🎯 View Demo Results":
        show_demo_results()
    else:
        uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov", "mkv"])
        model_option = st.selectbox("Select YOLO Model", ["yolo11s.pt", "yolo11m.pt", "yolo11l.pt"])
        show_upload_interface(uploaded_file, model_option)

    st.markdown("---")
    st.caption("🧠 Powered by YOLOv11 | Optimized for Internship Showcase | Streamlit Cloud Ready")


# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    main()
