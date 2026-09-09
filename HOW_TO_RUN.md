# 🚀 How to Run the Exam Dashboard

## ⚡ Quick Start (Easiest Method)

### Step 1: Start Backend Server

1. Open **Command Prompt** (not PowerShell)
2. Navigate to backend folder:
   ```cmd
   cd c:\Users\Petpooja-607\Desktop\pkt\backend
   ```
3. Run the server:
   ```cmd
   python main.py
   ```
4. Wait for message: **"Uvicorn running on http://0.0.0.0:8001"**
5. **Keep this window open!**

### Step 2: Start Frontend (New Window)

1. Open a **new Command Prompt**
2. Navigate to frontend folder:
   ```cmd
   cd c:\Users\Petpooja-607\Desktop\pkt\frontend
   ```
3. Install dependencies (first time only):
   ```cmd
   npm install
   ```
4. Start the development server:
   ```cmd
   npm start
   ```
5. Your browser should open automatically to **http://localhost:3000**

---

## 🎯 Using the Dashboard

1. **Upload Study Materials**
   - Click "Manage Documents" button
   - Upload your PDF exam materials
   - Wait for "Document uploaded successfully!"

2. **Ask Questions**
   - Type your question in the search box
   - OR click the camera icon to upload a screenshot
   - Click "Get Answer"
   - See precise answers with confidence scores!

---

## ⚠️ Troubleshooting

### Port Already in Use

If you see "port 8001 already in use":

**Option 1**: Kill the process
```cmd
netstat -ano | findstr :8001
taskkill /PID <process_id> /F
```

**Option 2**: Use a different port
- Edit `backend/.env` and change `PORT=8001` to `PORT=8002`
- Edit `frontend/.env` and change url to `http://localhost:8002`
- Restart both servers

### "Module not found" errors

```cmd
cd backend
pip install -r requirements.txt
```

### Frontend won't start

```cmd
cd frontend
npm install
```

### API Key Error

- Edit `backend/.env`
- Make sure `OPENAI_API_KEY=sk-proj-...` has your valid key
- Restart backend

---

## 📌 Important Notes

- **Backend runs on**: http://localhost:8001
- **Frontend runs on**: http://localhost:3000
- **Use Command Prompt (cmd)**, not PowerShell, to avoid script execution policy issues
- Both servers must be running simultaneously
- Don't close the Command Prompt windows while using the app

---

## 🛑 Stop the Servers

Press **Ctrl+C** in each Command Prompt window

---

**Need help?** Check SETUP.md for detailed instructions.
