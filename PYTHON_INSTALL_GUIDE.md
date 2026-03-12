# How to Install Python on Windows (Important!)

Your system currently has **Python 3.14.3**, which is **too new** and **not yet compatible** with the required AI libraries (TensorFlow).

**You MUST install an older, stable version (Python 3.10) for this app to work.**

## 1. Uninstall Current Python
1.  Go to **Windows Settings > Apps > Installed apps**.
2.  Search for "Python".
3.  Uninstall **Python 3.14.3** (and any other Python versions).

## 2. Download Python 3.10 (REQUIRED)
1.  Click this link to download Python 3.10.11:
    👉 [**Download Python 3.10.11 Installer**](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)

## 3. Install Python (CRITICAL STEP!)
1.  Run the downloaded installer (`python-3.10.11-amd64.exe`).
2.  **VERY IMPORTANT**: On the first screen, **CHECK THE BOX** that says:
    👉 **[x] Add Python 3.10 to PATH**
3.  Click **"Install Now"**.
4.  Wait for it to finish and click **"Close"**.

## 4. Verify Installation
1.  Close any open Command Prompts.
2.  Open a **new** Command Prompt.
3.  Type:
    ```cmd
    python --version
    ```
4.  It **MUST** say `Python 3.10.x`. If it says 3.14 again, you didn't uninstall the old one correctly.

## 5. Continue Setup
Go back to `RUN_GUIDE.md` and run the installation command again:
```cmd
python -m pip install -r web_app/requirements.txt
```
