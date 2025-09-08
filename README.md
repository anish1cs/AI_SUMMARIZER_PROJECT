AI Article Summarizer
This is a full-stack web application that summarizes web articles and extracts key takeaways using the Google Gemini API.

Project Structure
/frontend: Contains the single-file HTML, CSS, and JavaScript for the user interface.

/backend: Contains the Python Flask server that handles API requests, article scraping, and communication with the Gemini API.

How to Run Locally
Navigate to the backend directory: cd backend

Create and activate a virtual environment.

Install dependencies: pip install -r requirements.txt

Add your Gemini API key to a .env file.

Run the server: python app.py

Open the frontend/index.html file with a live server extension.
---

### **Part 3: Run and Test Locally**

Before deploying, let's make sure it works on your machine.

1.  **Set Up Backend:**
    * Open a terminal in VS Code.
    * Navigate into the backend folder: `cd backend`
    * Create a Python virtual environment: `python -m venv venv`
    * Activate it:
        * Windows: `.\venv\Scripts\activate`
        * macOS/Linux: `source venv/bin/activate`
    * Install all the required packages: `pip install -r requirements.txt`
    * **Edit the `.env` file** and paste your real Gemini API key inside the quotes.
    * Run the backend server: `python app.py`
    * The terminal should say `Running on http://127.0.0.1:5001`. Keep this terminal running.

2.  **Run Frontend:**
    * In VS Code, right-click the `frontend/index.html` file.
    * Select "Open with Live Server".
    * Your app will open in a browser. Paste in a URL and test the "Summarize" and "Get Key Takeaways" buttons. It should work perfectly.

---

### **Part 4: Push to a New GitHub Repository**

1.  Go to [GitHub](https://github.com/) and create a **new, empty, public repository**. Do not add a README or .gitignore. Let's call it `ai-summarizer-render`.
2.  Copy the repository URL (e.g., `https://github.com/your-username/ai-summarizer-render.git`).
3.  In your VS Code terminal (make sure you are in the main `AI_SUMMARIZER_PROJECT` folder), run these commands:
    ```bash
    git init
    git add .
    git commit -m "Initial project commit"
    git branch -M main
    git remote add origin YOUR_GITHUB_REPO_URL_HERE
    git push -u origin main
    ```

---

### **Part 5: Deploy on Render (Step-by-Step)**

This is the final stage. We will create two services.

#### **A. Deploy the Backend (Web Service)**

1.  Log in to Render and click **New +** > **Web Service**.
2.  Connect your new GitHub repository.
3.  Fill in these exact settings:
    * **Name:** `ai-summarizer-backend`
    * **Root Directory:** `backend`
    * **Environment:** `Python 3`
    * **Build Command:** `pip install -r requirements.txt`
    * **Start Command:** `gunicorn app:app`
    * **Instance Type:** **Free**
4.  Click **Advanced Settings** and add these two **Environment Variables**:
    * **Key 1:** `GEMINI_API_KEY`
        * **Value 1:** Paste your Gemini API key here.
    * **Key 2:** `FRONTEND_URL`
        * **Value 2:** We will fill this in later. For now, you can leave it blank or put a placeholder.
5.  Click **Create Web Service**. Wait for the deployment to finish. When it's live, **copy its URL** (e.g., `https://ai-summarizer-backend.onrender.com`).

#### **B. Deploy the Frontend (Static Site)**

1.  Go back to the Render Dashboard and click **New +** > **Static Site**.
2.  Connect the same GitHub repository.
3.  Fill in these settings:
    * **Name:** `ai-summarizer-frontend`
    * **Root Directory:** `frontend`
4.  Click **Create Static Site**. This will deploy very quickly. When it's live, **copy its URL** (e.g., `https://ai-summarizer-frontend.onrender.com`). This is your main app URL.

#### **C. The Final Connection**

1.  **Update Backend Environment:**
    * Go back to your `ai-summarizer-backend` service on Render.
    * Go to the **Environment** tab.
    * Edit the `FRONTEND_URL` variable and paste in your live **frontend URL** that you just copied. Save changes. This will cause your backend to restart.

2.  **Update Frontend Code:**
    * In your local VS Code, open `frontend/index.html`.
    * Go to the `<script>` tag at the bottom and find the `API_BASE_URL` variable.
    * Replace the local URL with your live **backend URL**.
        ```javascript
        // BEFORE
        const API_BASE_URL = 'http://127.0.0.1:5001/api';

        // AFTER
        const API_BASE_URL = 'https://ai-summarizer-backend.onrender.com/api';
        ```
3.  **Push the Final Change:**
    * Save the `index.html` file.
    * In your terminal, commit and push this final change:
        ```bash
        git add .
        git commit -m "Update API URL for production"
        git push
