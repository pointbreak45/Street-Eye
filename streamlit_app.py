"""
Streamlit Web Application for Vehicle Detection and Counting System
Professional interface optimized for internship showcase presentation
Enhanced with landing page demo and clean UI design
"""

import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import sys

# Import our custom vehicle detection system
from main import VehicleDetectionSystem

def show_demo_results():
    """
    Display demo results in professional landing page format
    """
    st.header("📊 Results")
    
    # Demo video at the top
    video_path = "outputs/processed_video.mp4"
    if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
        st.subheader("🎥 Processed Demo Video")
        
        # Get video file info for debugging
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        
        try:
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
                
            if len(video_bytes) > 0:
                st.info(f"📹 Video file: {file_size:.1f} MB, {len(video_bytes):,} bytes loaded")
                
                # Try different video display methods
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Try displaying video with explicit mime type
                    try:
                        st.video(video_bytes, format="video/mp4")
                    except Exception as video_error:
                        st.error(f"⚠️ Video display error: {video_error}")
                        # Fallback: try displaying as file path
                        try:
                            st.video(video_path)
                        except Exception as path_error:
                            st.error(f"⚠️ Path video error: {path_error}")
                            st.info("📝 Try refreshing the page or check if your browser supports MP4 playback.")
                
                with col2:
                    st.metric("File Size", f"{file_size:.1f} MB")
                    st.metric("Format", "MP4")
                    
                    # Video download as backup
                    st.download_button(
                        label="💾 Download Video",
                        data=video_bytes,
                        file_name="processed_video.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
            else:
                st.error("⚠️ Video file is empty. Please regenerate the processed video.")
                
        except Exception as e:
            st.error(f"⚠️ Error loading video: {str(e)}")
            st.info("📝 Video might be processing or corrupted. Try refreshing the page.")
    else:
        st.subheader("🎥 Demo Video")
        st.info("📹 **Demo video processing required.** For deployment, run the vehicle detection system once to generate the processed video with detection overlays.")
        st.markdown("""
        **To generate demo video:**
        1. Ensure you have a test video in `test videos/` folder
        2. Run: `python main.py` 
        3. The processed video will appear here automatically
        """)
    
    # Download buttons immediately below the video
    st.subheader("💾 Download Results")
    
    download_col1, download_col2, download_col3 = st.columns(3)
    
    with download_col1:
        if os.path.exists("outputs/traffic_data.csv"):
            with open("outputs/traffic_data.csv", "rb") as file:
                st.download_button(
                    label="📊 Download CSV Data",
                    data=file,
                    file_name="demo_traffic_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with download_col2:
        if os.path.exists("outputs/processed_video.mp4"):
            with open("outputs/processed_video.mp4", "rb") as file:
                st.download_button(
                    label="🎥 Download Video",
                    data=file,
                    file_name="demo_processed_video.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
    
    with download_col3:
        if os.path.exists("outputs/analysis_summary.txt"):
            with open("outputs/analysis_summary.txt", "rb") as file:
                st.download_button(
                    label="📝 Download Summary",
                    data=file,
                    file_name="demo_analysis_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    # Results panel below downloads - chart and summary side by side
    st.subheader("📈 Analysis Results")
    
    results_col1, results_col2 = st.columns([1.3, 0.7])
    
    with results_col1:
        # Traffic flow chart
        if os.path.exists("outputs/traffic_plot.png"):
            st.write("**📊 Traffic Flow Analysis**")
            image = Image.open("outputs/traffic_plot.png")
            st.image(image, caption="Demo Traffic Analysis Results", use_column_width=True)
    
    with results_col2:
        # Analysis Summary
        st.write("**📝 Analysis Summary**")
        
        if os.path.exists("outputs/analysis_summary.txt"):
            try:
                with open("outputs/analysis_summary.txt", "r", encoding='utf-8') as f:
                    summary_content = f.read()
                if summary_content.strip():
                    st.text_area(
                        "Summary Report", 
                        summary_content, 
                        height=400,
                        disabled=True,
                        label_visibility="collapsed"
                    )
                else:
                    sample_summary = generate_sample_summary()
                    st.text_area(
                        "Demo Summary Report", 
                        sample_summary, 
                        height=400,
                        disabled=True,
                        label_visibility="collapsed"
                    )
            except Exception as e:
                sample_summary = generate_sample_summary()
                st.text_area(
                    "Demo Summary Report", 
                    sample_summary, 
                    height=400,
                    disabled=True,
                    label_visibility="collapsed"
                )
        else:
            sample_summary = generate_sample_summary()
            st.text_area(
                "Demo Summary Report", 
                sample_summary, 
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )
    
    # Quick statistics at the bottom
    if os.path.exists("outputs/traffic_data.csv"):
        st.subheader("📊 Key Statistics")
        df = pd.read_csv("outputs/traffic_data.csv")
        
        total_vehicles = df['total'].sum()
        peak_traffic = df['total'].max()
        avg_traffic = df['total'].mean()
        duration_minutes = len(df) / 60
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        with stat_col1:
            st.metric("Total Vehicles", int(total_vehicles))
        with stat_col2:
            st.metric("Peak Traffic/sec", int(peak_traffic))
        with stat_col3:
            st.metric("Duration", f"{duration_minutes:.1f} min")
        with stat_col4:
            st.metric("Avg Traffic/sec", f"{avg_traffic:.1f}")

def generate_sample_summary():
    """
    Generate a sample analysis summary for demo purposes
    """
    return """
=== VEHICLE DETECTION ANALYSIS SUMMARY ===
Generated for Demo Showcase

📊 OVERALL STATISTICS:
• Analysis Duration: 1.1 minutes
• Total Vehicles Detected: 157
• Average Traffic Rate: 74.8 vehicles/minute

🚗 VEHICLE BREAKDOWN:
• Cars: 98 (62.4%)
• Bikes: 23 (14.6%)
• Buses: 8 (5.1%)
• Trucks: 21 (13.4%)
• Others: 7 (4.5%)

⚡ TRAFFIC INSIGHTS:
• Peak Activity: 12 vehicles detected at 47 seconds
• Most Common Vehicle: car
• Traffic Density: High

💡 ANALYSIS NOTES:
• Unique vehicle tracking (no crossing line required)
• YOLOv11 model used for object detection
• Each vehicle counted only once when first detected
• Data exported for further analysis

=== END OF DEMO SUMMARY ===
    """

def show_upload_interface_simple(uploaded_file, model_option, line_position):
    """
    Display simplified upload and processing interface
    """
    st.info(
        "⚠️ **Note**: Online demo shows precomputed results. For full YOLO processing, "
        "upload your own video (GPU recommended for faster performance)."
    )
    
    # Main upload area
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
            1. **Upload Video**: Choose a traffic video file (MP4, AVI, MOV, MKV) in the sidebar
            2. **Configure Settings**: Adjust model selection in sidebar
            3. **Start Analysis**: Click the analysis button and wait for results
            4. **View Results**: Check the results displayed in the right panel
                    
            **Note**: This system uses unique vehicle tracking - each vehicle is counted only once when first detected, with no crossing line required.
            """)
    
    with col2:
        st.header("📊 Live Results")
        
        # Check if analysis results exist
        if os.path.exists("outputs/traffic_data.csv"):
            st.subheader("📈 Latest Analysis")
            
            # Load and display data
            df = pd.read_csv("outputs/traffic_data.csv")
            
            # Quick stats
            total_vehicles = df['total'].sum()
            peak_traffic = df['total'].max()
            avg_traffic = df['total'].mean()
            
            st.metric("Peak Traffic", f"{int(peak_traffic)} vehicles/sec")
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
        
        else:
            st.info("📋 No analysis results yet. Upload and process a video to see results here.")

def main():
    """
    Main Streamlit application with professional landing page design
    """
    st.set_page_config(
        page_title="Vehicle Detection & Counter",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"  # Restore sidebar
    )
    
    # Header
    st.title("🚗 Professional Vehicle Detection & Counter")
    st.markdown("---")
    st.markdown("**Real-time vehicle detection and traffic analysis using YOLOv11**")
    
    # Sidebar Configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Mode selection
    demo_mode = st.sidebar.radio(
        "Select Mode",
        ["🎯 View Demo Results", "🚀 Upload & Process (Local/GPU Recommended)"],
        help="Choose between viewing precomputed demo or processing your own video"
    )
    
    # File upload (only show when not in demo mode)
    uploaded_file = None
    if demo_mode == "🚀 Upload & Process (Local/GPU Recommended)":
        uploaded_file = st.sidebar.file_uploader(
            "Upload Video File",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload a traffic video for analysis (GPU recommended for speed)"
        )
        
        st.sidebar.warning(
            "⚠️ **GPU Recommended**: YOLO processing can be slow without GPU acceleration."
        )
    
    # Line position setting (kept for compatibility but not used in tracking-based counting)
    line_position = st.sidebar.slider(
        "Line Position (Reference)", 
        min_value=100, 
        max_value=800, 
        value=430,
        help="Y-coordinate reference (not used for vehicle counting)"
    )
    
    # Model selection
    model_option = st.sidebar.selectbox(
        "YOLO Model",
        ["yolo11l.pt", "yolo11m.pt", "yolo11s.pt"],
        help="Choose YOLOv11 model variant"
    )
    
    # Main content area - different layouts based on mode
    if demo_mode == "🎯 View Demo Results":
        # Show demo results
        show_demo_results()
    
    else:
        # Show upload and processing interface
        show_upload_interface_simple(uploaded_file, model_option, line_position)
    
    # Footer
    st.markdown("---")
    st.markdown("### 🔧 Technical Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🤖 AI Model**
        - YOLOv11 Object Detection
        - Unique Vehicle Tracking
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