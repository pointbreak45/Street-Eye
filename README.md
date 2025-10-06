# Street Eye: AI Vehicle Detection & Counter

An advanced, real-time vehicle detection and counting system using YOLOv11 and Streamlit. Designed for accurate traffic analysis and easy web deployment.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-orange.svg)](https://ultralytics.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Project Preview](Outputs/processed_video.mp4)

## ✨ Key Features

-   **State-of-the-Art Detection**: Utilizes the YOLOv11 model for high-accuracy vehicle recognition.
-   **Multi-Class Counting**: Accurately counts Cars, Bikes, Buses, and Trucks.
-   **Interactive Dashboard**: A clean and professional web interface built with Streamlit.
-   **Real-time Analytics**: Provides traffic flow statistics and vehicle breakdown charts.
-   **Data Export**: Easily save analysis results as CSV files, processed videos, and summary reports.
-   **Deployment Ready**: Optimized with a "Demo Mode" for lightweight deployment on cloud platforms like Streamlit Cloud or Heroku without needing a GPU.

## 🛠️ Tech Stack

-   **Object Detection**: YOLOv11, PyTorch
-   **Computer Vision**: OpenCV
-   **Web Framework**: Streamlit
-   **Data Handling & Visualization**: Pandas, Matplotlib
-   **Core Language**: Python 3.8+

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

-   Python 3.8 or higher
-   `pip` package manager

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/pointbreak45/Street-Eye.git](https://github.com/your-username/Street-Eye.git)
    cd Street-Eye
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🖥️ Usage

This application has two modes: a lightweight **Demo Mode** for easy showcasing and a **Live Inference Mode** for processing your own videos.

### 1. Demo Mode (Recommended for quick start)

This mode runs instantly using pre-processed results and is perfect for web deployment where GPU resources are unavailable.

```bash
streamlit run streamlit_app.py
```

Navigate to `http://localhost:8501` in your web browser to see the interactive dashboard.

### 2. Live Inference Mode

This mode allows you to process your own video files. It is resource-intensive and works best on a machine with a compatible GPU.

1.  Place your video file (e.g., `my_video.mp4`) in the `test videos/` directory.
2.  Modify `main.py` to point to your video file.
3.  Run the main detection script:
    ```bash
    python main.py
    ```
    The processed video and analysis files will be saved in the `outputs/` directory.

## 📁 Project Structure

```
Street-Eye/
├── streamlit_app.py      # The Streamlit web application for the dashboard
├── main.py               # Core script for video processing and vehicle detection
├── requirements.txt      # Python dependencies
├── yolo11l.pt            # Pre-trained YOLOv11 model weights
├── test videos/          # Directory for input video files
│   └── test_video_1.mp4
└── outputs/              # Directory for generated results
    ├── processed_video.mp4
    ├── traffic_data.csv
    └── analysis_summary.txt
```

## 🎨 Future Enhancements

-   [ ] Real-time webcam and IP camera stream support.
-   [ ] Vehicle speed estimation.
-   [ ] Multi-lane detection with lane-specific counts.
-   [ ] Anomaly detection (e.g., accidents, stopped vehicles).

## 🤝 Contributing

Contributions are welcome! Please feel free to fork the repository, make improvements, and submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📜 License

This project is distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Srujan - sruja2401@gmail.com

Project Link: [https://github.com/your-username/Street-Eye](https://github.com/your-username/Street-Eye)
