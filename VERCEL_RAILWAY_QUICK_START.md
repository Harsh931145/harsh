# ⚡ Vercel + Railway - Quick Start (30 mins)

**The fastest way to deploy your Petpooja Exam Dashboard to the cloud!**

---

## 🎯 What You Need

1. **GitHub Account** - Free at https://github.com
2. **Your Project** - Already on your computer
3. **30 Minutes** - Follow step-by-step
4. **NVIDIA API Key** - Already have it!

---

## 📝 Step-by-Step Checklist

### ☑️ Phase 1: Push to GitHub (10 mins)

```powershell
# 1. Open PowerShell in project folder
cd C:\Users\Petpooja-607\Desktop\pkt

# 2. Initialize git
git init

# 3. Add all files
git add .

# 4. Commit
git commit -m "Initial commit"

# 5. Create repo on GitHub
# Go to https://github.com/new
# Name: petpooja-exam-dashboard
# Click "Create repository"

# 6. Push to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/petpooja-exam-dashboard.git
git branch -M main
git push -u origin main
```

**✅ Done!** Your code is on GitHub.

---

### ☑️ Phase 2: Deploy Backend (Railway) (10 mins)

**Step 1: Sign Up**
1. Go to https://railway.app/
2. Click "Start a New Project"
3. Sign in with GitHub
4. Authorize Railway

**Step 2: Deploy**
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `petpooja-exam-dashboard`
4. Railway detects Python app
5. **Important:** Set Root Directory to `backend`

**Step 3: Configure**
1. Click on your service
2. Go to "Variables" tab
3. Add these:
   ```
   META_API_KEY = nvapi-YOUR_KEY_HERE
   META_MODEL = meta/muse-glimmer-30b
   HOST = 0.0.0.0
   ```
4. Go to "Settings" tab
5. Scroll to "Networking"
6. Click "Generate Domain"
7. **COPY THIS URL** (you'll need it!)

**Step 4: Test**
- Open: `https://YOUR-APP.railway.app/docs`
- Should see FastAPI docs

**✅ Done!** Backend is live.

---

### ☑️ Phase 3: Deploy Frontend (Vercel) (10 mins)

**Step 1: Sign Up**
1. Go to https://vercel.com/
2. Click "Sign Up"
3. Sign in with GitHub
4. Authorize Vercel

**Step 2: Import**
1. Click "Add New..." → "Project"
2. Find your GitHub repo
3. Click "Import"

**Step 3: Configure**
1. Framework: **Create React App**
2. Root Directory: Click "Edit" → Select **`frontend`**
3. Build Command: `npm run build`
4. Output Directory: `build`

**Step 4: Environment Variable**
1. Expand "Environment Variables"
2. Add:
   - Name: `REACT_APP_API_URL`
   - Value: `https://YOUR-APP.railway.app` (from Railway)
3. Click "Add"

**Step 5: Deploy**
1. Click "Deploy"
2. Wait 2-3 minutes
3. Click "Visit" when done

**✅ Done!** Frontend is live.

---

## 🔧 Fix CORS (Important!)

Your frontend needs permission to call your backend.

**Update backend/main.py:**

```python
# Find this section (around line 20):
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://YOUR-VERCEL-URL.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Push update:**
```powershell
git add backend/main.py
git commit -m "Update CORS"
git push
```

Railway will auto-redeploy in 2 minutes.

---

## ✅ Test Your Deployment

1. **Open Vercel URL**: `https://your-app.vercel.app`
2. **Upload a PDF**: Click "Manage Documents"
3. **Ask a question**: Type or paste screenshot
4. **Get answer**: Should work in 3-5 seconds

---

## 🎉 You're Live!

**Your URLs:**
- **Frontend** (share this): `https://your-app.vercel.app`
- **Backend**: `https://your-app.railway.app`
- **API Docs**: `https://your-app.railway.app/docs`

**Share with users!** They can access from anywhere! 🌍

---

## 💰 Cost

### Free Trial:
- **Vercel**: FREE forever (hobby plan)
- **Railway**: $5 credit (about 500 hours)

### After Trial:
- **Vercel**: Still FREE for most use cases
- **Railway**: ~$5-15/month

### Total: ~$5-15/month for unlimited users!

---

## 🔄 How to Update

Just push to GitHub:

```powershell
# Make your changes
# ...

# Commit and push
git add .
git commit -m "Your changes"
git push

# Railway and Vercel auto-deploy! ✨
```

No manual deployment needed!

---

## 🐛 Common Issues

### Issue: "CORS Error"
**Fix:** Update backend CORS with your Vercel URL

### Issue: "API Error" 
**Fix:** Check `REACT_APP_API_URL` in Vercel environment variables

### Issue: "Module not found" on Railway
**Fix:** Verify Root Directory is set to `backend`

### Issue: Build fails on Vercel
**Fix:** Verify Root Directory is set to `frontend`

---

## 📞 Need Help?

**Full guide:** Read `DEPLOY_VERCEL_RAILWAY.md` for detailed instructions

**Quick check:**
- ✅ Backend working? Test: `/docs` endpoint
- ✅ Frontend working? Open Vercel URL
- ✅ Connected? Submit test question
- ✅ CORS updated? Check backend main.py

---

## 🎯 Summary

| Service | URL | Purpose |
|---------|-----|---------|
| **Railway** | your-backend.railway.app | Hosts Python API |
| **Vercel** | your-app.vercel.app | Hosts React UI |
| **GitHub** | github.com/you/repo | Stores code |

**Automatic Deployment Flow:**
```
You push to GitHub
    ↓
GitHub notifies Railway & Vercel
    ↓
Both auto-deploy your changes
    ↓
Live in 2-5 minutes! ✨
```

---

## ✨ What You Get

- ✅ **Live URLs** - Access from anywhere
- ✅ **HTTPS** - Automatic SSL certificates
- ✅ **Auto-deploy** - Push to GitHub = instant deployment
- ✅ **Scalable** - Handles unlimited users
- ✅ **Professional** - Production-ready hosting
- ✅ **FREE** - Free tier available!

---

**Congratulations! Your exam dashboard is now on the cloud!** 🚀

Share your Vercel URL with all users and start helping them prepare for exams! 🎓

---

*Need detailed instructions? See: `DEPLOY_VERCEL_RAILWAY.md`*
