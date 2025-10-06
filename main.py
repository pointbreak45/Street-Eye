"""
Professional Vehicle Detection and Counting System
Enhanced version with data analytics, visualization, and modular design
Author: Vehicle Detection Team
Date: 2025
"""

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Check and import required packages
try:
    import cv2
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from ultralytics import YOLO
    from collections import defaultdict
    from datetime import datetime
    import time
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("💡 Please install dependencies:")
    print("   pip install -r requirements.txt")
    print("   or run: python setup.py")
    exit(1)

class VehicleDetectionSystem:
    """
    Professional Vehicle Detection and Counting System using YOLOv11
    """
    
    def __init__(self, model_path='yolo11l.pt', line_position=430, use_tracking=True):
        """
        Initialize the vehicle detection system
        
        Args:
            model_path (str): Path to YOLOv11 model weights
            line_position (int): Y-coordinate reference (not used for counting)
            use_tracking (bool): Whether to use object tracking for unique IDs
        """
        self.model = YOLO(model_path)
        self.class_list = self.model.names
        self.line_y_red = line_position  # Kept for compatibility but not used for counting
        self.use_tracking = use_tracking
        
        # Test if tracking is available
        if self.use_tracking:
            try:
                import lap
                print("✅ Object tracking enabled with unique IDs")
            except ImportError:
                print("⚠️  lap package not available, using detection-only mode")
                self.use_tracking = False
        else:
            print("✅ Detection-only mode enabled")
        
        # Vehicle category mapping
        self.vehicle_categories = {
            'car': [2],           # Car
            'bike': [1, 3],       # Bicycle, Motorcycle  
            'bus': [5],           # Bus
            'truck': [7],         # Truck
            'others': [6]         # Train and others
        }
        
        # Initialize tracking variables
        self.tracked_vehicles = set()  # Track unique vehicle IDs that have been counted
        self.time_series_data = []
        self.start_time = None
        self.detection_counter = 0  # For detection-only mode
        
        # Category to plural mapping for CSV columns
        self.category_plurals = {
            'car': 'cars',
            'bike': 'bikes', 
            'bus': 'buses',
            'truck': 'trucks',
            'others': 'others'
        }
        
    def categorize_vehicle(self, class_name):
        """
        Categorize detected vehicle into predefined categories
        
        Args:
            class_name (str): Original YOLO class name
            
        Returns:
            str: Vehicle category
        """
        class_mapping = {
            'bicycle': 'bike',
            'car': 'car', 
            'motorcycle': 'bike',
            'bus': 'bus',
            'train': 'others',
            'truck': 'truck'
        }
        return class_mapping.get(class_name.lower(), 'others')
    
    def _get_video_fourcc(self, codec='avc1'):
        """
        Get video fourcc code with web browser compatibility
        
        Args:
            codec (str): Video codec string (default: 'avc1' for H.264)
            
        Returns:
            int: fourcc code for video writer
        """
        # Use H.264 codec for better web browser compatibility
        try:
            # Try cv2.VideoWriter_fourcc if available
            fourcc_func = getattr(cv2, 'VideoWriter_fourcc', None)
            if fourcc_func:
                return fourcc_func(*codec)
            elif hasattr(cv2.VideoWriter, 'fourcc'):
                return cv2.VideoWriter.fourcc(*codec)
            else:
                # Fallback to H.264 hex code
                return 0x31637661  # 'avc1' as hex for H.264
        except Exception:
            print("⚠️  Using H.264 fallback codec for web compatibility")
            return 0x31637661  # 'avc1' as hex
    
    def detect_and_count(self, video_path, output_folder='outputs'):
        """
        Main function to detect and count vehicles in video
        
        Args:
            video_path (str): Path to input video
            output_folder (str): Folder to save outputs
            
        Returns:
            pd.DataFrame: Time series data of vehicle counts
        """
        print("🚗 Starting Vehicle Detection and Counting...")
        
        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Initialize video capture
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / fps
        
        print(f"📹 Video Info: {frame_width}x{frame_height}, {fps} FPS, {video_duration:.1f}s duration")
        
        # Setup video writer with web browser compatibility
        output_video_path = os.path.join(output_folder, 'processed_video.mp4')
        fourcc = self._get_video_fourcc('avc1')  # Use H.264 for web compatibility
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
        
        # Verify video writer initialization
        if not out.isOpened():
            print("⚠️  H.264 codec failed, trying alternative codec...")
            fourcc = self._get_video_fourcc('mp4v')
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
        
        # Initialize counters
        category_counts = defaultdict(int)
        frame_count = 0
        self.start_time = time.time()
        current_second = 0
        second_counts = {'cars': 0, 'bikes': 0, 'buses': 0, 'trucks': 0, 'others': 0}
        
        print("🔄 Processing video frames...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            current_time_in_video = frame_count / fps
            
            # Run YOLO detection/tracking based on availability
            if self.use_tracking:
                try:
                    results = self.model.track(frame, persist=True, classes=[1,2,3,5,6,7], verbose=False)
                except Exception as tracking_error:
                    print(f"\n⚠️  Tracking failed: {tracking_error}")
                    print("💡 Switching to detection-only mode...")
                    self.use_tracking = False
                    results = self.model(frame, classes=[1,2,3,5,6,7], verbose=False)
            else:
                results = self.model(frame, classes=[1,2,3,5,6,7], verbose=False)
            
            # Note: Red line counting logic removed - now counting all detections per frame
            
            if results[0].boxes is not None and len(results[0].boxes) > 0:
                boxes = results[0].boxes.xyxy.cpu()
                
                # Handle track IDs based on mode
                if self.use_tracking and hasattr(results[0].boxes, 'id') and results[0].boxes.id is not None:
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                else:
                    # Generate sequential IDs for detection-only mode
                    track_ids = list(range(self.detection_counter, self.detection_counter + len(boxes)))
                    self.detection_counter += len(boxes)
                    
                class_indices = results[0].boxes.cls.int().cpu().tolist()
                # Process each detection
                for box, track_id, class_idx in zip(boxes, track_ids, class_indices):
                    x1, y1, x2, y2 = map(int, box)
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    class_name = self.class_list[class_idx]
                    category = self.categorize_vehicle(class_name)
                    
                    # Draw detection - bounding box and label with unique ID
                    color = self._get_category_color(category)
                    cv2.circle(frame, (cx, cy), 4, color, -1)
                    
                    # Show ID and category
                    id_text = f"ID: {track_id}" if self.use_tracking else f"DET: {track_id}"
                    cv2.putText(frame, f"{id_text} {category.upper()}", 
                               (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Count unique vehicles only once (no red line needed)
                    if track_id not in self.tracked_vehicles:
                        self.tracked_vehicles.add(track_id)
                        category_counts[category] += 1
                        # Use proper plural form for second counts
                        plural_category = self.category_plurals.get(category, category + 's')
                        second_counts[plural_category] += 1
            
            # Log data every second
            if int(current_time_in_video) > current_second:
                total_current = sum(second_counts.values())
                self.time_series_data.append({
                    'time_in_seconds': current_second,
                    'cars': second_counts['cars'],
                    'bikes': second_counts['bikes'], 
                    'buses': second_counts['buses'],
                    'trucks': second_counts['trucks'],
                    'others': second_counts['others'],
                    'total': total_current
                })
                current_second = int(current_time_in_video)
                # Reset counters for next second
                second_counts = {'cars': 0, 'bikes': 0, 'buses': 0, 'trucks': 0, 'others': 0}
            
            # Display counts on frame
            self._draw_counts_on_frame(frame, category_counts)
            
            # Add progress info and mode
            progress = (frame_count / total_frames) * 100
            mode_text = "TRACKING" if self.use_tracking else "DETECTION"
            cv2.putText(frame, f"Progress: {progress:.1f}% | Mode: {mode_text}", 
                       (50, frame_height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            out.write(frame)
            cv2.imshow("Professional Vehicle Detection System", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Add final second data
        total_final = sum(second_counts.values())
        self.time_series_data.append({
            'time_in_seconds': current_second,
            'cars': second_counts['cars'],
            'bikes': second_counts['bikes'],
            'buses': second_counts['buses'], 
            'trucks': second_counts['trucks'],
            'others': second_counts['others'],
            'total': total_final
        })
        
        # Cleanup
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        # Post-process video for web compatibility
        self._optimize_video_for_web(output_video_path)
        
        print(f"✅ Video processing complete! Saved to {output_video_path}")
        
        # Create DataFrame
        df = pd.DataFrame(self.time_series_data)
        return df, category_counts
    
    def _get_category_color(self, category):
        """
        Get color for each vehicle category
        """
        colors = {
            'car': (0, 255, 0),      # Green
            'bike': (255, 0, 0),     # Blue  
            'bus': (0, 255, 255),    # Yellow
            'truck': (255, 0, 255),  # Magenta
            'others': (128, 128, 128) # Gray
        }
        return colors.get(category, (0, 255, 0))
    
    def _optimize_video_for_web(self, video_path):
        """
        Optimize video for web browser compatibility using ffmpeg if available
        
        Args:
            video_path (str): Path to the video file to optimize
        """
        try:
            import subprocess
            
            # Check if ffmpeg is available
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # Create optimized version
                temp_path = video_path.replace('.mp4', '_temp.mp4')
                cmd = [
                    'ffmpeg', '-i', video_path,
                    '-c:v', 'libx264',  # H.264 codec
                    '-preset', 'fast',   # Fast encoding
                    '-crf', '23',        # Good quality
                    '-movflags', '+faststart',  # Web optimization
                    '-y',                # Overwrite output
                    temp_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    # Replace original with optimized version
                    os.replace(temp_path, video_path)
                    print("✅ Video optimized for web browser compatibility")
                else:
                    print("⚠️  Video optimization failed, using original")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            else:
                print("ℹ️  ffmpeg not available, skipping video optimization")
        except Exception as e:
            print(f"⚠️  Video optimization failed: {e}")
    
    def _draw_counts_on_frame(self, frame, category_counts):
        """
        Draw vehicle counts on the frame
        """
        y_offset = 30
        total = sum(category_counts.values())
        
        # Title
        cv2.putText(frame, "VEHICLE COUNTS:", (50, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_offset += 35
        
        # Individual counts
        for category in ['car', 'bike', 'bus', 'truck', 'others']:
            count = category_counts[category]
            color = self._get_category_color(category)
            cv2.putText(frame, f"{category.upper()}: {count}", (50, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            y_offset += 25
        
        # Total
        cv2.putText(frame, f"TOTAL: {total}", (50, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    def save_results(self, counts_df, category_counts, output_folder='outputs'):
        """
        Save analysis results to files
        
        Args:
            counts_df (pd.DataFrame): Time series data
            category_counts (dict): Total category counts
            output_folder (str): Output directory
        """
        print("💾 Saving analysis results...")
        
        # Save CSV data
        csv_path = os.path.join(output_folder, 'traffic_data.csv')
        counts_df.to_csv(csv_path, index=False)
        print(f"📊 Data saved to {csv_path}")
        
        # Generate and save plot
        self._generate_traffic_plot(counts_df, output_folder)
        
        # Generate and save summary
        self._generate_summary(counts_df, category_counts, output_folder)
        
        print("✅ All results saved successfully!")
    
    def _generate_traffic_plot(self, counts_df, output_folder):
        """
        Generate traffic flow visualization
        """
        plt.figure(figsize=(12, 8))
        
        # Plot individual categories
        plt.subplot(2, 1, 1)
        plt.plot(counts_df['time_in_seconds'], counts_df['cars'], 'g-', label='Cars', linewidth=2)
        plt.plot(counts_df['time_in_seconds'], counts_df['bikes'], 'b-', label='Bikes', linewidth=2)
        plt.plot(counts_df['time_in_seconds'], counts_df['buses'], 'y-', label='Buses', linewidth=2)
        plt.plot(counts_df['time_in_seconds'], counts_df['trucks'], 'm-', label='Trucks', linewidth=2)
        plt.plot(counts_df['time_in_seconds'], counts_df['others'], 'gray', label='Others', linewidth=2)
        
        plt.title('Vehicle Detection by Category Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Vehicles Detected per Second')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot total traffic flow
        plt.subplot(2, 1, 2)
        plt.plot(counts_df['time_in_seconds'], counts_df['total'], 'r-', linewidth=3, label='Total Traffic')
        plt.fill_between(counts_df['time_in_seconds'], counts_df['total'], alpha=0.3, color='red')
        
        plt.title('Total Traffic Flow Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Total Vehicles per Second')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        plot_path = os.path.join(output_folder, 'traffic_plot.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 Traffic plot saved to {plot_path}")
    
    def _generate_summary(self, counts_df, category_counts, output_folder):
        """
        Generate text summary of analysis
        """
        total_vehicles = sum(category_counts.values())
        duration_minutes = len(counts_df) / 60 if len(counts_df) > 0 else 1
        
        # Find busiest moment
        if not counts_df.empty:
            busiest_idx = counts_df['total'].idxmax()
            busiest_time = counts_df.loc[busiest_idx, 'time_in_seconds']
            busiest_count = counts_df.loc[busiest_idx, 'total']
        else:
            busiest_time = 0
            busiest_count = 0
        
        # Calculate percentages
        percentages = {}
        for category, count in category_counts.items():
            if total_vehicles > 0:
                percentages[category] = (count / total_vehicles) * 100
            else:
                percentages[category] = 0
        
        # Generate summary text
        summary = f"""
=== VEHICLE DETECTION ANALYSIS SUMMARY ===
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 OVERALL STATISTICS:
• Analysis Duration: {duration_minutes:.1f} minutes
• Total Vehicles Detected: {total_vehicles}
• Average Traffic Rate: {total_vehicles/duration_minutes:.1f} vehicles/minute

🚗 VEHICLE BREAKDOWN:
• Cars: {category_counts['car']} ({percentages['car']:.1f}%)
• Bikes: {category_counts['bike']} ({percentages['bike']:.1f}%)
• Buses: {category_counts['bus']} ({percentages['bus']:.1f}%)
• Trucks: {category_counts['truck']} ({percentages['truck']:.1f}%)
• Others: {category_counts['others']} ({percentages['others']:.1f}%)

⚡ TRAFFIC INSIGHTS:
• Peak Activity: {busiest_count} vehicles detected at {busiest_time} seconds
• Most Common Vehicle: {max(category_counts, key=category_counts.get) if category_counts else 'None'}
• Traffic Density: {'High' if total_vehicles/duration_minutes > 30 else 'Medium' if total_vehicles/duration_minutes > 15 else 'Low'}

💡 ANALYSIS NOTES:
• Unique vehicle tracking (no crossing line required)
• YOLOv11 model used for object detection
• Each vehicle counted only once when first detected
• Data exported for further analysis

=== END OF SUMMARY ===
        """
        
        summary_path = os.path.join(output_folder, 'analysis_summary.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"📝 Summary saved to {summary_path}")
        print("\n" + "="*50)
        print("QUICK SUMMARY:")
        print(f"In {duration_minutes:.1f} minutes: {total_vehicles} vehicles detected")
        if total_vehicles > 0:
            dominant_category = max(category_counts, key=category_counts.get)
            print(f"{percentages[dominant_category]:.0f}% {dominant_category}s, busiest at {busiest_time}s")
        print("="*50)

def main():
    """
    Main function to run the vehicle detection system
    """
    print("🚀 Professional Vehicle Detection System")
    print("========================================")
    
    # Initialize system
    detector = VehicleDetectionSystem()
    
    # Set video path (update this to your video file)
    video_path = './test videos/test video_1.mp4'
    
    try:
        # Run detection and counting
        counts_df, category_counts = detector.detect_and_count(video_path)
        
        # Save all results
        detector.save_results(counts_df, category_counts)
        
        print("\n🎉 Analysis Complete! Check the 'outputs' folder for results.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your video path and model file.")

if __name__ == "__main__":
    main()
