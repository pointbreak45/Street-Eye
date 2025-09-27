"""
Example usage of the Vehicle Detection System
This demonstrates how to use the modular functions for different applications
"""

from main import VehicleDetectionSystem
import os

def run_simple_analysis():
    """
    Simple example of running vehicle detection analysis
    """
    print("🚗 Running Simple Vehicle Detection Analysis")
    print("=" * 50)
    
    # Initialize the detection system
    detector = VehicleDetectionSystem(
        model_path='yolo11l.pt',
        line_position=430
    )
    
    # Path to your video file
    video_path = './test videos/test video_1.mp4'
    
    # Check if video exists
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        print("Please ensure your video file is in the correct location.")
        return
    
    try:
        # Run detection and counting
        print("🔄 Starting detection...")
        counts_df, category_counts = detector.detect_and_count(video_path)
        
        # Save results
        print("💾 Saving results...")
        detector.save_results(counts_df, category_counts)
        
        print("\n✅ Analysis completed successfully!")
        print(f"📊 Total vehicles detected: {sum(category_counts.values())}")
        print("📁 Check the 'outputs' folder for detailed results.")
        
        return counts_df, category_counts
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return None, None

def generate_summary_only(counts_df, category_counts):
    """
    Example of generating only the summary (useful for web apps)
    """
    if counts_df is None or category_counts is None:
        print("No data to generate summary from.")
        return
    
    detector = VehicleDetectionSystem()
    detector._generate_summary(counts_df, category_counts, 'outputs')
    print("📝 Summary generated!")

def main():
    """
    Main function demonstrating different use cases
    """
    print("🎯 Vehicle Detection System - Example Usage")
    print("=" * 60)
    
    # Example 1: Full analysis
    print("\n1️⃣ Running full analysis...")
    counts_df, category_counts = run_simple_analysis()
    
    # Example 2: Generate summary only (for web apps)
    if counts_df is not None:
        print("\n2️⃣ Generating additional summary...")
        generate_summary_only(counts_df, category_counts)
    
    # Example 3: Display some statistics
    if counts_df is not None and not counts_df.empty:
        print("\n3️⃣ Quick Statistics:")
        print(f"   📊 Total time analyzed: {len(counts_df)} seconds")
        print(f"   🚗 Peak traffic: {counts_df['total'].max()} vehicles/second")
        print(f"   📈 Average traffic: {counts_df['total'].mean():.1f} vehicles/second")
        
        # Category breakdown
        print("\n   📋 Vehicle breakdown:")
        for category, count in category_counts.items():
            print(f"      {category.capitalize()}: {count}")
    
    print("\n🎉 Example completed! Check outputs folder for all results.")

if __name__ == "__main__":
    main()