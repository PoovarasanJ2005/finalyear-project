# Fingerprint Blood Group Detection Web App

This is a full real-time web application for detecting blood group from fingerprint images using a ResNet deep learning model.

## 1. System Requirements (Prerequisites)

### Software (S/W)
- **Programming Language**: **Python 3.10 or 3.11** (Highly Recommended).
  > ⚠️ **Python 3.12+ (and 3.14+) is NOT compatible with TensorFlow yet.** Please uninstall newer versions and install **Python 3.10**.
  
  **How to Install Correct Python:**
  1.  Uninstall your current Python version.
  2.  Download **Python 3.10.11** from [python.org/downloads/release/python-31011/](https://www.python.org/downloads/release/python-31011/).
  3.  Run the installer.
  4.  **CRITICALLY IMPORTANT**: Check the box **"Add Python to PATH"** at the bottom of the installer window.
  5.  Restart your terminal/CMD.

### Hardware (H/W)
- **Processor**: Intel Core i5/i7 or AMD Ryzen 5/7 (Recommended).
- **RAM**: Minimum 8GB (TensorFlow requires significant memory).
- **Storage**: ~500MB free space for model and dependencies.

## 2. Installation & Setup (One-Time Only)

1.  **Open Project Folder**:
    - Navigate to the project folder (`e:\fingerprint-based-blood-group-detection-main`) in Command Prompt or PowerShell.

2.  **Verify Python Version**:
    - The system has automatically created a dedicated environment with the correct Python version for you inside `venv310_real`.

3.  **Install Dependencies**:
    - The dependencies should already be installed in this specialized environment, but you can verify it by running:
      ```powershell
      .\venv310_real\Scripts\python -m pip install -r web_app/requirements.txt
      ```

## 3. Run Command

To start the web application server, you MUST use the specialized environment by running this exact command:

```powershell
.\venv310_real\Scripts\python web_app/app.py
```

- You should see output indicating the server is running on `http://0.0.0.0:5000` or `http://127.0.0.1:5000`.
- The model will load automatically (this may take a few seconds).

## 4. Usage & Test Procedure

1.  **Open Browser**:
    - Go to `http://localhost:5000` in your web browser.

2.  **Upload Image**:
    - Click on the upload box or drag and drop a **Fingerprint Image** (JPG, PNG, BMP).
    - You can use sample images from the original dataset or download online samples.

3.  **Detect**:
    - Click the **"Detect Blood Group"** button.
    - Wait for the AI to process (usually takes <1 second).

4.  **View Result**:
    - The predicted Blood Group (e.g., A+, O-) and Confidence Score will be displayed.

## Troubleshooting

- **"Model not loaded" error**: Ensure `web_app/model/model_blood_group_detection_resnet.h5` exists.
- **Port already in use**: If port 5000 is busy, modify the line `app.run(port=5000)` in `web_app/app.py` to a different port (e.g., 5001).
