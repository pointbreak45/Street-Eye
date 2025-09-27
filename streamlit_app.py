"""
Streamlit Web Application for Vehicle Detection and Counting System
Professional interface for traffic analysis and vehicle counting
"""

import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import sys

# Import our custom vehicle detection system
from main import VehicleDetectionSystem

def main():
    """
    Main Streamlit application
    """
    st.set_page_config(
        page_title="Vehicle Detection & Counter",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🚗 Professional Vehicle Detection & Counter")
    st.markdown("---")
    st.markdown("**Real-time vehicle detection and traffic analysis using YOLOv11**")
    
    # Sidebar
    st.sidebar.header("📋 Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Video File",
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Upload a traffic video for analysis"
    )
    
    # Line position setting
    line_position = st.sidebar.slider(
        "Counting Line Position", 
        min_value=100, 
        max_value=800, 
        value=430,
        help="Y-coordinate for the counting line"
    )
    
    # Model selection
    model_option = st.sidebar.selectbox(
        "YOLO Model",
        ["yolo11l.pt", "yolo11m.pt", "yolo11s.pt"],
        help="Choose YOLOv11 model variant"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📹 Video Analysis")
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_video_path = f"temp_{uploaded_file.name}"
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ Video uploaded: {uploaded_file.name}")
            
            # Run analysis button
            if st.button("🚀 Start Analysis", type="primary"):
                with st.spinner("🔄 Analyzing video... This may take a few minutes."):
                    try:
                        # Initialize detection system
                        detector = VehicleDetectionSystem(
                            model_path=model_option,
                            line_position=line_position
                        )
                        
                        # Run detection
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("🔍 Processing video frames...")
                        progress_bar.progress(25)
                        
                        counts_df, category_counts = detector.detect_and_count(temp_video_path)
                        
                        progress_bar.progress(75)
                        status_text.text("💾 Saving results...")
                        
                        # Save results
                        detector.save_results(counts_df, category_counts)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        
                        # Display results
                        st.success("🎉 Analysis completed successfully!")
                        
                        # Show summary statistics
                        total_vehicles = sum(category_counts.values())
                        duration_minutes = len(counts_df) / 60 if len(counts_df) > 0 else 1
                        
                        st.metric("Total Vehicles", total_vehicles)
                        st.metric("Analysis Duration", f"{duration_minutes:.1f} min")
                        st.metric("Avg. Traffic Rate", f"{total_vehicles/duration_minutes:.1f}/min")
                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_video_path):
                            os.remove(temp_video_path)
            
        else:
            st.info("👆 Please upload a video file to begin analysis")
            
            # Show example
            st.markdown("### 📝 How to use:")
            st.markdown("""
            1. **Upload Video**: Choose a traffic video file (MP4, AVI, MOV, MKV)
            2. **Configure Settings**: Adjust counting line position and model
            3. **Start Analysis**: Click the analysis button and wait for results
            4. **View Results**: Check the outputs folder for detailed results
            """)
    
    with col2:
        st.header("📊 Results")
        
        # Check if analysis results exist
        if os.path.exists("outputs/traffic_data.csv"):
            st.subheader("📈 Latest Analysis")
            
            # Load and display data
            df = pd.read_csv("outputs/traffic_data.csv")
            
            # Quick stats
            total_vehicles = df['total'].sum()
            peak_traffic = df['total'].max()
            avg_traffic = df['total'].mean()
            
            st.metric("Peak Traffic", f"{peak_traffic} vehicles/sec")
            st.metric("Average Traffic", f"{avg_traffic:.1f} vehicles/sec")
            
            # Display breakdown
            st.subheader("🚗 Vehicle Breakdown")
            latest_data = df.iloc[-1] if not df.empty else {}
            
            categories = ['cars', 'bikes', 'buses', 'trucks', 'others']
            for cat in categories:
                if cat in latest_data:
                    st.metric(cat.title(), int(latest_data[cat]))
            
            # Plot
            if os.path.exists("outputs/traffic_plot.png"):
                st.subheader("📊 Traffic Flow Chart")
                image = Image.open("outputs/traffic_plot.png")
                st.image(image, caption="Traffic Analysis Results")
            
            # Download links
            st.subheader("💾 Download Results")
            
            # CSV download
            with open("outputs/traffic_data.csv", "rb") as file:
                st.download_button(
                    label="📊 Download CSV Data",
                    data=file,
                    file_name="traffic_data.csv",
                    mime="text/csv"
                )
            
            # Summary download
            if os.path.exists("outputs/analysis_summary.txt"):
                with open("outputs/analysis_summary.txt", "rb") as file:
                    st.download_button(
                        label="📝 Download Summary",
                        data=file,
                        file_name="analysis_summary.txt",
                        mime="text/plain"
                    )
            
            # Plot download
            if os.path.exists("outputs/traffic_plot.png"):
                with open("outputs/traffic_plot.png", "rb") as file:
                    st.download_button(
                        label="📈 Download Plot",
                        data=file,
                        file_name="traffic_plot.png",
                        mime="image/png"
                    )
                    
        else:
            st.info("📋 No analysis results yet. Run an analysis to see results here.")
    
    # Footer
    st.markdown("---")
    st.markdown("### 🔧 Technical Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🤖 AI Model**
        - YOLOv11 Object Detection
        - Real-time Tracking
        - Multi-class Recognition
        """)
    
    with col2:
        st.markdown("""
        **📊 Data Analysis**
        - Time-series Logging
        - Category-wise Counting
        - Statistical Summary
        """)
    
    with col3:
        st.markdown("""
        **💾 Outputs**
        - Processed Video
        - CSV Data Export
        - Visualization Charts
        """)

if __name__ == "__main__":
    main()