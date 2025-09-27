"""
Test script to verify the Vehicle Detection System installation
Run this to check if all dependencies are properly installed
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    tests = [
        ("cv2", "OpenCV"),
        ("pandas", "Pandas"),
        ("matplotlib.pyplot", "Matplotlib"),
        ("numpy", "NumPy"),
        ("ultralytics", "Ultralytics YOLO"),
        ("torch", "PyTorch"),
        ("streamlit", "Streamlit")
    ]
    
    all_passed = True
    
    for package, name in tests:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_file_structure():
    """Test if the project structure is correct"""
    print("\n📁 Testing file structure...")
    
    import os
    
    required_files = [
        "main.py",
        "streamlit_app.py", 
        "requirements.txt",
        "README.md",
        "setup.py",
        "example_usage.py"
    ]
    
    required_dirs = [
        "outputs"
    ]
    
    all_files_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            all_files_exist = False
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/ directory")
        else:
            print(f"❌ {directory}/ directory - Missing")
            all_files_exist = False
    
    return all_files_exist

def test_system_functionality():
    """Test basic system functionality"""
    print("\n⚙️ Testing system functionality...")
    
    try:
        from main import VehicleDetectionSystem
        print("✅ VehicleDetectionSystem class import")
        
        # Try to initialize (without model file)
        detector = VehicleDetectionSystem()
        print("✅ VehicleDetectionSystem initialization")
        
        # Test categorization function
        category = detector.categorize_vehicle("car")
        if category == "car":
            print("✅ Vehicle categorization function")
        else:
            print("❌ Vehicle categorization function")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ System functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔬 VEHICLE DETECTION SYSTEM - INSTALLATION TEST")
    print("=" * 55)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test file structure
    structure_ok = test_file_structure()
    
    # Test system functionality
    system_ok = test_system_functionality()
    
    # Final result
    print("\n" + "=" * 55)
    print("📊 TEST RESULTS:")
    print("=" * 55)
    
    if imports_ok and structure_ok and system_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your installation is ready to use!")
        print("\n🚀 Next steps:")
        print("1. Download YOLO model: yolo11l.pt")
        print("2. Add test video to 'test videos' folder")
        print("3. Run: python main.py or streamlit run streamlit_app.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️  Please check the errors above and fix them.")
        print("\n🔧 Common fixes:")
        if not imports_ok:
            print("   • Run: pip install -r requirements.txt")
        if not structure_ok:
            print("   • Run: python setup.py")
        if not system_ok:
            print("   • Check main.py for syntax errors")
    
    print("\n💡 For help, check the README.md file!")

if __name__ == "__main__":
    main()