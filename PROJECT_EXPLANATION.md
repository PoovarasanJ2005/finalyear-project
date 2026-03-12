## Fingerprint Blood Group Detection - Training & Execution Plan

Hello! Since you only know the project name and want to understand how the entire process works, I'll guide you step-by-step. Let me break down the whole project for you:

### What Does This Project Do?
This project aims to detect a person's **blood group** (A+, A-, B+, B-, O+, O-, AB+, AB-) just by analyzing an image of their **fingerprint**. To do this, we use a concept from Artificial Intelligence called **Deep Learning**, specifically a Convolutional Neural Network (CNN).

### 1. The Dataset (Data Collection)
To teach the AI to recognize blood groups from fingerprints, it needs to look at thousands of examples. 
*   **Where from?** We need a dataset containing fingerprint images and their corresponding blood groups. A common public dataset for fingerprint analysis is the **SOCOFing dataset** from Kaggle, however, *standard public datasets do not usually contain blood group labels directly linked to fingerprints* because there's no proven scientific link between fingerprint patterns and blood groups.
*   **For this project:** We'll assume the project intends to use a dataset structured with folders for each blood group (A+, A-, etc.), with fingerprint images inside each folder.

### 2. Training the Model (Teaching the AI)
Training is the process where the AI learns patterns.
*   **Data Preparation:** We resize all fingerprint images to the same size (e.g., 256x256 pixels) and normalize their pixel values.
*   **The Architecture:** We build a CNN (the "brain"). It consists of:
    *   **Convolutional Layers:** These act like filters that scan the fingerprint to find edges, ridges, and unique patterns (minutiae).
    *   **Pooling Layers:** These summarize the patterns to make the model faster and more robust.
    *   **Dense Layers:** These take the summarized patterns and make the final decision (which of the 8 blood groups it belongs to).
*   **The Training Process:**
    1.  The model looks at an image and guesses the blood group.
    2.  It checks the correct answer.
    3.  If it's wrong, it adjusts its internal settings (weights) to be more accurate next time.
    4.  It repeats this thousands of times (Epochs) until its accuracy is high.
*   **Output:** Once training is done, we save the model as a file (e.g., `model_blood_group_detection_resnet.h5`).

### 3. Testing the Model (Checking Accuracy)
After training, we give the model new fingerprint images it has never seen before. We measure how many it gets right to determine its real-world accuracy. If it's good enough, it's ready to use.

### 4. Execution (Running the Web App)
You already have a pre-trained model file in your project (`test/model_blood_group_detection_resnet.h5`). I have created a web application that uses this model.

Here is the exact step-by-step to run it on your computer:

#### Step A: Setting up the right Python Environment
We discovered your Python 3.14 was too new. We've set up a virtual environment (`venv310`) that uses the correct older version of Python and installed all required packages inside it.

#### Step B: Starting the Web Server
We need to start the application. Open your Command Prompt (or PowerShell), ensure you are in the project folder `E:\fingerprint-based-blood-group-detection-main`, and run this command:

```powershell
.\venv310\Scripts\python web_app/app.py
```
*Wait a moment. You will see text scrolling, and eventually, it should say `Running on http://0.0.0.0:5000`.*

#### Step C: Using the Web Page
1.  Open your internet browser (Chrome, Edge, etc.).
2.  In the address bar, type: `http://localhost:5000` and press Enter.
3.  You will see the "BloodGroup AI" web page.
4.  Click the upload box to select a fingerprint image from your computer (you can use the `O- blood group.BMP` file located in your `test` folder to test).
5.  Click **"Detect Blood Group"**.
6.  The website sends the image to our Python code, which passes it to the AI model. The AI makes a prediction, and the website shows you the result on the screen!

**Next Steps:** Let's execute the web app right now so you can see it working! I will run the command for you.
