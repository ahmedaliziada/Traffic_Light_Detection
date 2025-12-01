# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### 2. Set Up Project
```bash
# Clone or download the project
cd Traffic_Light_Detection

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

### 5. Use the Application
1. Open your browser at `http://localhost:8501`
2. Upload an image with traffic lights
3. View the detection results!

## 🔧 Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'torch'`
**Solution**: 
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**Problem**: Model download fails
**Solution**: Check your internet connection. The YOLOv5 model (~14MB) will download automatically on first run.

**Problem**: `ImportError: No module named 'cv2'`
**Solution**: 
```bash
pip install opencv-python
```

**Problem**: Streamlit won't start
**Solution**: 
```bash
pip install --upgrade streamlit
streamlit run app.py
```

## 📝 Project Commands

```bash
# Run the application
streamlit run app.py

# Run on custom port
streamlit run app.py --server.port 8080

# Run tests
python -m pytest tests/

# Check Python packages
pip list

# Update dependencies
pip install -r requirements.txt --upgrade
```

## 🎯 Next Steps

- Try uploading different traffic light images
- Adjust detection parameters in `config/config.py`
- Explore the codebase structure
- Contribute improvements!

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [YOLOv5 Documentation](https://docs.ultralytics.com/)
- [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
