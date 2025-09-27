"""
Setup script for Vehicle Detection and Counting System
Helps users quickly set up the environment and download required files
"""

import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version check passed: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please install manually:")
        print("   pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["outputs", "test videos"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    print("✅ All directories created!")

def check_model_file():
    """Check if YOLO model file exists"""
    model_file = "yolo11l.pt"
    
    if os.path.exists(model_file):
        print(f"✅ YOLO model found: {model_file}")
        return True
    else:
        print(f"⚠️  YOLO model not found: {model_file}")
        print("   Please download it from: https://docs.ultralytics.com/models/yolo11/#performance-metrics")
        print("   Look for the 'Performance' section and download YOLOv11l model")
        return False

def check_test_video():
    """Check if test video exists"""
    test_video = "test videos/test video_1.mp4"
    
    if os.path.exists(test_video):
        print(f"✅ Test video found: {test_video}")
        return True
    else:
        print(f"⚠️  Test video not found: {test_video}")
        print("   Please place your traffic video in the 'test videos' folder")
        print("   Or update the video path in main.py")
        return False

def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED!")
    print("=" * 60)
    print("\n📋 NEXT STEPS:")
    print("1. Download YOLO model (if not done): yolo11l.pt")
    print("2. Add your test video to 'test videos' folder")
    print("3. Run the system:")
    print("   • Command line: python main.py")
    print("   • Web interface: streamlit run streamlit_app.py")
    print("   • Example usage: python example_usage.py")
    print("\n📁 Results will be saved in the 'outputs' folder")
    print("🌐 For web interface, open: http://localhost:8501")
    print("\n💡 TIP: Use the web interface for easier operation!")

def main():
    """Main setup function"""
    print("🚀 Vehicle Detection System Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create directories
    create_directories()
    
    # Check for model and video files
    model_exists = check_model_file()
    video_exists = check_test_video()
    
    # Display next steps
    display_next_steps()
    
    if not model_exists or not video_exists:
        print("\n⚠️  ATTENTION: Some files are missing. Please check the warnings above.")
    else:
        print("\n🎯 Everything is ready! You can start using the system now.")

if __name__ == "__main__":
    main()