# 🚀 Deploy to Vercel + Railway - Step by Step Guide

**Modern cloud deployment with free tier available!**

---

## 📋 Overview

- **Backend** → Railway (Python/FastAPI hosting)
- **Frontend** → Vercel (React hosting)
- **Time**: 30-45 minutes
- **Cost**: FREE tier available (then ~$5-10/month)
- **Users**: Unlimited

### What You'll Get:
- ✅ Live URLs accessible from anywhere
- ✅ Automatic HTTPS (SSL)
- ✅ Professional hosting
- ✅ Easy updates (just push changes)
- ✅ No server management needed

---

## 🎯 Prerequisites

Before starting, make sure you have:
- [ ] GitHub account (create at https://github.com)
- [ ] Git installed on your computer
- [ ] Backend and frontend working locally
- [ ] NVIDIA API key (for Meta Muse)

---

## Part 1: Prepare Your Project (10 minutes)

### Step 1.1: Create GitHub Repository

1. Go to https://github.com
2. Click **"New"** button (or the + icon)
3. Repository name: `petpooja-exam-dashboard`
4. Description: `AI-powered exam preparation for Petpooja products`
5. Select: **Private** (recommended)
6. Click **"Create repository"**

### Step 1.2: Initialize Git in Your Project

Open PowerShell/Terminal in your project folder:

```powershell
# Navigate to project
cd C:\Users\Petpooja-607\Desktop\pkt

# Initialize git (if not already done)
git init

# Add .gitignore (already exists)
# Make sure .env files are ignored!
```

### Step 1.3: Verify .gitignore

Check that `c:\Users\Petpooja-607\Desktop\pkt\.gitignore` contains:

```
# Environment variables
.env
.env.local
.env.production
*.env

# Node modules
node_modules/
frontend/node_modules/
backend/__pycache__/

# Build files
frontend/build/
frontend/.next/
dist/

# Knowledge base (don't upload PDFs to git)
knowledgebase/*.pdf
uploaded_documents/

# FAISS index
*.faiss
*.pkl

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

### Step 1.4: Create Backend Railway Configuration

Create `backend/railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `backend/runtime.txt`:
```
python-3.10.13
```

### Step 1.5: Create Frontend Vercel Configuration

Create `frontend/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

Update `frontend/package.json` - add this to scripts:
```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "vercel-build": "react-scripts build"
  }
}
```

### Step 1.6: Commit to GitHub

```powershell
# Add all files
git add .

# Commit
git commit -m "Initial commit - Petpooja Exam Dashboard"

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/petpooja-exam-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**✅ Checkpoint:** Your code is now on GitHub!

---

## Part 2: Deploy Backend to Railway (15 minutes)

### Step 2.1: Create Railway Account

1. Go to https://railway.app/
2. Click **"Start a New Project"** or **"Login"**
3. Sign up with GitHub (recommended)
4. Authorize Railway to access GitHub

### Step 2.2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. If first time:
   - Click **"Configure GitHub App"**
   - Select your repository: `petpooja-exam-dashboard`
   - Save
4. Select your repository from the list
5. Railway will ask which folder - select **backend** folder

### Step 2.3: Configure Backend Service

1. After Railway detects your project, click on the service
2. Go to **"Settings"** tab
3. Set **Root Directory**: `/backend`
4. Set **Start Command**: 
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Click **"Save Changes"**

### Step 2.4: Add Environment Variables

1. Go to **"Variables"** tab
2. Click **"+ New Variable"**
3. Add these variables:

```
META_API_KEY=nvapi-YOUR_ACTUAL_KEY_HERE
META_MODEL=meta/muse-glimmer-30b
HOST=0.0.0.0
KNOWLEDGE_BASE_PATH=/app/knowledgebase
```

4. Click **"Add"** for each variable

### Step 2.5: Deploy Backend

1. Go to **"Deployments"** tab
2. Railway will automatically start deploying
3. Wait 2-5 minutes for deployment
4. Watch the logs - you should see:
   ```
   ✅ Using Meta Muse Glimmer (FREE via NVIDIA!)
   🤖 Meta Muse Glimmer initialized
   INFO: Uvicorn running on http://0.0.0.0:XXXX
   ```

### Step 2.6: Get Backend URL

1. Go to **"Settings"** tab
2. Scroll to **"Networking"**
3. Click **"Generate Domain"**
4. Copy the URL (example: `petpooja-backend.railway.app`)
5. **Save this URL!** You'll need it for frontend

**Test Backend:**
Open: `https://YOUR-BACKEND.railway.app/docs`
You should see FastAPI documentation page.

**✅ Checkpoint:** Backend is live on Railway!

---

## Part 3: Deploy Frontend to Vercel (15 minutes)

### Step 3.1: Create Vercel Account

1. Go to https://vercel.com/
2. Click **"Sign Up"**
3. Sign up with GitHub (recommended)
4. Authorize Vercel

### Step 3.2: Import Project

1. Click **"Add New..."** → **"Project"**
2. Click **"Import"** next to your GitHub repository
3. Select **"Import"** again
4. Vercel detects it's a monorepo

### Step 3.3: Configure Frontend Settings

1. **Framework Preset**: Select **"Create React App"**
2. **Root Directory**: Click **"Edit"** → Select **"frontend"**
3. **Build Command**: 
   ```
   npm run build
   ```
4. **Output Directory**: 
   ```
   build
   ```
5. **Install Command**: 
   ```
   npm install
   ```

### Step 3.4: Add Environment Variables

1. Expand **"Environment Variables"** section
2. Add variable:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://YOUR-BACKEND.railway.app` (from Step 2.6)
3. Click **"Add"**

### Step 3.5: Deploy Frontend

1. Click **"Deploy"**
2. Vercel will:
   - Install dependencies
   - Build the React app
   - Deploy to their CDN
3. Wait 2-3 minutes
4. Watch the build logs

### Step 3.6: Get Frontend URL

1. After successful deployment, you'll see:
   ```
   🎉 Your project is live!
   ```
2. Copy the URL (example: `petpooja-exam.vercel.app`)
3. Click **"Visit"** to open your dashboard

**✅ Checkpoint:** Frontend is live on Vercel!

---

## Part 4: Configure CORS (Important!)

### Step 4.1: Update Backend CORS Settings

You need to allow your Vercel frontend to access Railway backend.

1. Open `backend/main.py` locally
2. Find the CORS middleware section (around line 20-27)
3. Update `allow_origins`:

```python
# CORS middleware
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

4. Save the file
5. Commit and push:

```powershell
git add backend/main.py
git commit -m "Update CORS for Vercel deployment"
git push
```

6. Railway will automatically redeploy (wait 2-3 minutes)

---

## Part 5: Test Your Deployment

### Step 5.1: Access Your Dashboard

1. Open your Vercel URL: `https://YOUR-APP.vercel.app`
2. You should see the Exam Preparation Assistant

### Step 5.2: Upload Test Document

1. Click **"📚 Manage Documents"**
2. Upload a test PDF (any Petpooja documentation)
3. Wait for processing
4. Verify it appears in the list

### Step 5.3: Test Question

**Text Question:**
1. Type: "What is Petpooja POS?"
2. Click "Get Answer"
3. Wait 3-5 seconds
4. Verify answer appears

**Screenshot Test:**
1. Take any screenshot (Win+Shift+S)
2. Paste in search box (Ctrl+V)
3. Ask a question
4. Verify answer appears

### Step 5.4: Check Network Tab

1. Press F12 in browser
2. Go to **"Network"** tab
3. Submit a question
4. Check that API call to Railway backend succeeds
5. Status should be **200 OK**

**✅ Checkpoint:** Everything is working!

---

## Part 6: Custom Domain (Optional)

### For Vercel (Frontend):

1. Go to Vercel dashboard
2. Click your project
3. Go to **"Settings"** → **"Domains"**
4. Click **"Add"**
5. Enter your domain (e.g., `exam.petpooja.com`)
6. Follow DNS setup instructions
7. Wait for SSL certificate (automatic)

### For Railway (Backend):

1. Go to Railway dashboard
2. Click your backend service
3. Go to **"Settings"** → **"Networking"**
4. Click **"Custom Domain"**
5. Enter your domain (e.g., `api-exam.petpooja.com`)
6. Add CNAME record in your DNS
7. Wait for SSL certificate

---

## Part 7: Continuous Deployment

### Automatic Updates

Now when you make changes:

```powershell
# Make your changes to code
# ...

# Commit and push
git add .
git commit -m "Your change description"
git push

# Railway and Vercel automatically redeploy!
```

**No manual deployment needed!** ✨

---

## 📊 Deployment URLs Summary

After completion, save these:

```
Frontend (Vercel): https://YOUR-APP.vercel.app
Backend (Railway):  https://YOUR-BACKEND.railway.app
API Docs:          https://YOUR-BACKEND.railway.app/docs

GitHub Repo:       https://github.com/YOUR_USERNAME/petpooja-exam-dashboard
```

---

## 💰 Pricing

### Vercel (Frontend):
- **Free Tier**:
  - 100 GB bandwidth/month
  - Unlimited projects
  - Automatic HTTPS
  - Good for: 100-1000 users
- **Pro**: $20/month (if needed)

### Railway (Backend):
- **Free Trial**: $5 credit
- **Hobby**: $5/month (500 hours)
- **Usage-based**: ~$0.000231/min
- **Estimate**: $5-15/month for moderate use

### Total Estimated Cost:
- **Free tier**: $0-5/month (trial credit)
- **After trial**: $5-20/month
- **Unlimited users!**

---

## 🔒 Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` files
- ✅ Use Railway/Vercel variable management
- ✅ Rotate API keys periodically

### 2. CORS Configuration
- ✅ Only allow your Vercel domains
- ✅ Don't use wildcard `*` in production

### 3. Rate Limiting
Consider adding rate limiting to prevent abuse.

### 4. Authentication (Future)
For production, add user authentication.

---

## 🐛 Troubleshooting

### Issue: "Failed to load resource" (CORS Error)

**Solution:**
1. Check backend CORS settings include Vercel URL
2. Verify frontend `.env` has correct Railway URL
3. Redeploy both services

### Issue: "Module not found" on Railway

**Solution:**
1. Check `backend/requirements.txt` is complete
2. Verify Root Directory is set to `/backend`
3. Check Railway build logs

### Issue: "Build failed" on Vercel

**Solution:**
1. Check Root Directory is set to `frontend`
2. Verify `package.json` has `build` script
3. Check Vercel build logs for specific error

### Issue: Backend crashes on Railway

**Solution:**
1. Check Railway logs for error
2. Verify environment variables are set
3. Test locally first: `python main.py`
4. Check `runtime.txt` has correct Python version

### Issue: Frontend shows "API Error"

**Solution:**
1. Verify `REACT_APP_API_URL` is set correctly
2. Check Railway backend is running
3. Test backend directly: `https://YOUR-BACKEND.railway.app/docs`
4. Check browser console for exact error

---

## 📈 Monitoring & Maintenance

### Railway Dashboard:
- Monitor CPU/RAM usage
- Check deployment logs
- View metrics and analytics
- Set up alerts

### Vercel Dashboard:
- Monitor bandwidth usage
- Check build times
- View deployment history
- Analytics (on Pro plan)

### Recommended Monitoring:
1. Check logs daily (first week)
2. Monitor API usage
3. Track error rates
4. Review user feedback

---

## 🔄 Updating Your Deployment

### To Update Code:

```powershell
# Make changes locally
# Test locally first!

# Commit and push
git add .
git commit -m "Description of changes"
git push

# Railway and Vercel auto-deploy!
# Wait 2-5 minutes for deployment
```

### To Update Environment Variables:

**Railway:**
1. Go to Variables tab
2. Edit or add variables
3. Service automatically restarts

**Vercel:**
1. Go to Settings → Environment Variables
2. Edit or add variables
3. Redeploy from Deployments tab

### To Rollback:

**Railway:**
1. Go to Deployments
2. Click on previous deployment
3. Click "Redeploy"

**Vercel:**
1. Go to Deployments
2. Find previous deployment
3. Click "..." → "Promote to Production"

---

## ✅ Final Checklist

Before sharing with users:

- [ ] Backend deployed on Railway
- [ ] Frontend deployed on Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Test question works
- [ ] Screenshot paste works
- [ ] PDFs can be uploaded
- [ ] Answers are accurate
- [ ] No errors in console
- [ ] URLs bookmarked
- [ ] Domain configured (optional)
- [ ] Users informed of URL
- [ ] User guide distributed

---

## 🎉 Success!

Your Petpooja Exam Dashboard is now:
- ✅ Live on the internet
- ✅ Accessible from anywhere
- ✅ Automatically HTTPS secured
- ✅ Auto-deploying on git push
- ✅ Scalable to unlimited users
- ✅ Professional hosting

**Share your URLs:**
- Frontend: `https://YOUR-APP.vercel.app`
- Share with all users!

---

## 📞 Support & Resources

### Documentation:
- Railway Docs: https://docs.railway.app/
- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/

### Community:
- Railway Discord: https://discord.gg/railway
- Vercel Discord: https://discord.gg/vercel

### Your Project Docs:
- USER_GUIDE_SIMPLE.md (for users)
- README.md (overview)
- DEPLOYMENT_GUIDE.md (all deployment options)

---

**Congratulations on your cloud deployment!** 🚀🎓

*Last updated: September 2026*  
*Version: 1.0*
