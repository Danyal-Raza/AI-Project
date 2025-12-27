# Real-Time Phishing: Setup Guide 🛡️

Follow these steps to reproduce the training in Google Colab, set up the Flask API, and use the browser extension.

---

## 1. Train the Model in Google Colab

### Step A: Download the Dataset
1. Go to [Phishing Site URLs](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls).
2. Download the `phishing-site-urls.csv` file to your local computer.

### Step B: Run the Notebook
1. Open [Google Colab](https://colab.research.google.com/).
2. Click **File > Upload Notebook** and select `AI_Model.ipynb`.
3. In the left sidebar of Colab, click the **Folder icon** 📂.
4. Drag and drop your downloaded `phishing-site-urls.csv` into the file area.
5. Go to **Runtime > Run all**.

### Step C: Export the Model
Once the script finishes, a code cell will generate `phishing_rf_model.joblib`. 
1. Refresh the file sidebar in Colab.
2. Right-click `phishing_rf_model.joblib` and select **Download**.

---

## 2. Run the Local Flask API

### Step A: Setup Environment
1. Create a folder on your PC and move `Real_time_Phishing.py` and `phishing_rf_model.joblib` into it.
2. Open your terminal/command prompt in that folder.
3. Install dependencies:
   ```bash
   pip install flask flask-cors pandas joblib scikit-learn
   ```

### Step B: Start the Server
1. Run the script:
   ```bash
   python Real_time_Phishing.py
   ```
2. Keep this terminal open. The API is now running at http://127.0.0.1:5000.

## 3. Add the Browser Extension
1. Open Google Chrome (or any Chromium browser).
2. Go to Browser Extensions.
3. Enable Developer mode (toggle in the top-right corner).
4. Click Load unpacked.
5. Select the folder containing your extension files (manifest.json, popup.html, etc.).
6. Click the Extension icon in your browser toolbar and pin the 'Real-Time Phishing'.

## 🧪 Testing
1. Click on any URL.
2. The extension will send the URL to your local Python server, which uses the .joblib model to return a "Safe" or "Phishing" verdict.
3. This will generate an alert with the probabilty score of phishing.
4. If you want to visit the link, then click on 'Ok'.

## 📂 Project Structure
1. AI_Model.ipynb: Training script for Colab.
2. Real_time_Phishing.py: Flask backend.
3. phishing_rf_model.joblib: The brain of the project (ML model).

### Important Tips for your users:
* **The "Localhost" Link:** Remind users that the Flask app must be running for the browser extension to work. If they close the terminal, the extension will show a connection error.
* **Dataset Name:** If your notebook expects a specific filename (like `phishing_site_urls.csv`), make sure to tell users to rename their Kaggle download to match that name before uploading to Colab.
