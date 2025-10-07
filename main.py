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
    Professional Vehicle Detection and Counting System using YOLO
    """
    
    def __init__(self, model_path='yolo11l.pt', line_position=430, use_tracking=True):
        """
        Initialize the vehicle detection system
        """
        self.model = YOLO(model_path)
        self.class_list = self.model.names
        self.line_y_red = line_position
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
            'car': [2],
            'bike': [1, 3],
            'bus': [5],
            'truck': [7],
            'others': [6]
        }
        
        # Initialize tracking variables
        self.tracked_vehicles = set()
        self.time_series_data = []
        self.start_time = None
        self.detection_counter = 0
        
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

    def detect_and_count(self, video_path, output_folder='outputs'):
        """
        Main function to detect and count vehicles in video
        """
        print("🚗 Starting Vehicle Detection and Counting...")
        
        os.makedirs(output_folder, exist_ok=True)
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / fps
        
        print(f"📹 Video Info: {frame_width}x{frame_height}, {fps} FPS, {video_duration:.1f}s duration")
        
        output_video_path = os.path.join(output_folder, 'processed_video.mp4')
        
        fourcc = cv2.VideoWriter_fourcc(*'avc1') 
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

        if not out.isOpened():
            print("\n" + "="*50)
            print("CRITICAL ERROR: cv2.VideoWriter failed to open.")
            print("This means the 'avc1' (H.264) codec is not available in your local OpenCV.")
            print("Please check your OpenCV installation. The output video will be incorrect.")
            print("="*50 + "\n")
        else:
            print("✅ Video writer initialized successfully with web-compatible H.264 codec.")

        category_counts = defaultdict(int)
        frame_count = 0
        self.start_time = time.time()
        current_second = 0
        second_counts = {'cars': 0, 'bikes': 0, 'buses': 0, 'trucks': 0, 'others': 0}
        
        print("🔄 Processing video frames...")

        cv2.namedWindow("Vehicle Detection System", cv2.WINDOW_NORMAL)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            current_time_in_video = frame_count / fps
            
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
            
            if results[0].boxes is not None and len(results[0].boxes) > 0:
                boxes = results[0].boxes.xyxy.cpu()
                
                if self.use_tracking and hasattr(results[0].boxes, 'id') and results[0].boxes.id is not None:
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                else:
                    track_ids = list(range(self.detection_counter, self.detection_counter + len(boxes)))
                    self.detection_counter += len(boxes)
                    
                class_indices = results[0].boxes.cls.int().cpu().tolist()
                
                for box, track_id, class_idx in zip(boxes, track_ids, class_indices):
                    x1, y1, x2, y2 = map(int, box)
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    class_name = self.class_list[class_idx]
                    category = self.categorize_vehicle(class_name)
                    
                    color = self._get_category_color(category)
                    cv2.circle(frame, (cx, cy), 4, color, -1)
                    
                    id_text = f"ID: {track_id}" if self.use_tracking else f"DET: {track_id}"
                    cv2.putText(frame, f"{id_text} {category.upper()}", 
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    if track_id not in self.tracked_vehicles:
                        self.tracked_vehicles.add(track_id)
                        category_counts[category] += 1
                        plural_category = self.category_plurals.get(category, category + 's')
                        second_counts[plural_category] += 1
            
            if int(current_time_in_video) > current_second:
                total_current = sum(second_counts.values())
                self.time_series_data.append({
                    'time_in_seconds': current_second, 'cars': second_counts['cars'],
                    'bikes': second_counts['bikes'], 'buses': second_counts['buses'],
                    'trucks': second_counts['trucks'], 'others': second_counts['others'],
                    'total': total_current
                })
                current_second = int(current_time_in_video)
                second_counts = {'cars': 0, 'bikes': 0, 'buses': 0, 'trucks': 0, 'others': 0}
            
            self._draw_counts_on_frame(frame, category_counts)
            
            progress = (frame_count / total_frames) * 100
            mode_text = "TRACKING" if self.use_tracking else "DETECTION"
            cv2.putText(frame, f"Progress: {progress:.1f}% | Mode: {mode_text}", 
                        (50, frame_height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            out.write(frame)
            
            # --- CHANGE 1: This line is now UNCOMMENTED to show the window ---
            cv2.imshow("Vehicle Detection System", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        total_final = sum(second_counts.values())
        self.time_series_data.append({
            'time_in_seconds': current_second, 'cars': second_counts['cars'],
            'bikes': second_counts['bikes'], 'buses': second_counts['buses'],
            'trucks': second_counts['trucks'], 'others': second_counts['others'],
            'total': total_final
        })
        
        cap.release()
        out.release()

        # --- CHANGE 2: This line is now UNCOMMENTED to close the window properly ---
        cv2.destroyAllWindows()
        
        print(f"✅ Video processing complete! Saved to {output_video_path}")
        
        df = pd.DataFrame(self.time_series_data)
        return df, category_counts

    def _get_category_color(self, category):
        """
        Get color for each vehicle category
        """
        colors = {
            'car': (0, 255, 0), 'bike': (255, 0, 0), 'bus': (0, 255, 255),
            'truck': (255, 0, 255), 'others': (128, 128, 128)
        }
        return colors.get(category, (0, 255, 0))

    def _draw_counts_on_frame(self, frame, category_counts):
        """
        Draw vehicle counts on the frame
        """
        y_offset = 30
        total = sum(category_counts.values())
        
        cv2.putText(frame, "VEHICLE COUNTS:", (50, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_offset += 35
        
        for category in ['car', 'bike', 'bus', 'truck', 'others']:
            count = category_counts[category]
            color = self._get_category_color(category)
            cv2.putText(frame, f"{category.upper()}: {count}", (50, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            y_offset += 25
        
        cv2.putText(frame, f"TOTAL: {total}", (50, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    def save_results(self, counts_df, category_counts, output_folder='outputs'):
        """
        Save analysis results to files
        """
        print("💾 Saving analysis results...")
        
        csv_path = os.path.join(output_folder, 'traffic_data.csv')
        counts_df.to_csv(csv_path, index=False)
        print(f"📊 Data saved to {csv_path}")
        
        self._generate_traffic_plot(counts_df, output_folder)
        self._generate_summary(counts_df, category_counts, output_folder)
        
        print("✅ All results saved successfully!")

    def _generate_traffic_plot(self, counts_df, output_folder):
        """
        Generate traffic flow visualization
        """
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        ax1.plot(counts_df['time_in_seconds'], counts_df['cars'], color='green', label='Cars', linewidth=2)
        ax1.plot(counts_df['time_in_seconds'], counts_df['bikes'], color='cyan', label='Bikes', linewidth=2)
        ax1.plot(counts_df['time_in_seconds'], counts_df['buses'], color='yellow', label='Buses', linewidth=2)
        ax1.plot(counts_df['time_in_seconds'], counts_df['trucks'], color='magenta', label='Trucks', linewidth=2)
        ax1.plot(counts_df['time_in_seconds'], counts_df['others'], color='gray', label='Others', linewidth=2)
        ax1.set_title('Vehicle Detection by Category Over Time', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Vehicles Detected per Second')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(counts_df['time_in_seconds'], counts_df['total'], color='red', linewidth=3, label='Total Traffic')
        ax2.fill_between(counts_df['time_in_seconds'], counts_df['total'], alpha=0.3, color='red')
        ax2.set_title('Total Traffic Flow Over Time', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Total Vehicles per Second')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
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
        duration_seconds = len(counts_df) if not counts_df.empty else 1
        
        if not counts_df.empty:
            busiest_idx = counts_df['total'].idxmax()
            busiest_time = counts_df.loc[busiest_idx, 'time_in_seconds']
            busiest_count = counts_df.loc[busiest_idx, 'total']
        else:
            busiest_time = 0
            busiest_count = 0
        
        percentages = {cat: (cnt / total_vehicles) * 100 if total_vehicles > 0 else 0 for cat, cnt in category_counts.items()}
        
        summary = f"""=== VEHICLE DETECTION ANALYSIS SUMMARY ===
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 OVERALL STATISTICS:
• Analysis Duration: {duration_seconds / 60:.1f} minutes
• Total Vehicles Detected: {total_vehicles}
• Average Traffic Rate: {total_vehicles / (duration_seconds / 60) if duration_seconds > 0 else 0:.1f} vehicles/minute

🚗 VEHICLE BREAKDOWN:
• Cars: {category_counts.get('car', 0)} ({percentages.get('car', 0):.1f}%)
• Bikes: {category_counts.get('bike', 0)} ({percentages.get('bike', 0):.1f}%)
• Buses: {category_counts.get('bus', 0)} ({percentages.get('bus', 0):.1f}%)
• Trucks: {category_counts.get('truck', 0)} ({percentages.get('truck', 0):.1f}%)
• Others: {category_counts.get('others', 0)} ({percentages.get('others', 0):.1f}%)

⚡ TRAFFIC INSIGHTS:
• Peak Activity: {busiest_count} vehicles detected at {busiest_time} seconds
• Most Common Vehicle: {max(category_counts, key=category_counts.get) if category_counts else 'None'}

=== END OF SUMMARY ===
"""
        
        summary_path = os.path.join(output_folder, 'analysis_summary.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary.strip())
        
        print(f"📝 Summary saved to {summary_path}")

def main():
    """
    Main function to run the vehicle detection system
    """
    print("🚀 Professional Vehicle Detection System")
    print("========================================")
    
    # Initialize system
    detector = VehicleDetectionSystem(model_path='yolo11l.pt')
    
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