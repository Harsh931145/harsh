# Petpooja Exam Dashboard - Deployment Guide

## Table of Contents
1. [Local Deployment (Single User)](#local-deployment)
2. [Network Deployment (Multiple Users - Same Network)](#network-deployment)
3. [Cloud Deployment (Internet Access)](#cloud-deployment)
4. [User Guide](#user-guide)

---

## Local Deployment (Single User)

Perfect for: Testing, personal use, single computer

### Prerequisites
- ✅ Python 3.8+ installed
- ✅ Node.js 14+ installed
- ✅ Git installed (optional)

### Step-by-Step Setup

#### 1. Prepare the Project
```bash
# Navigate to project folder
cd C:\Users\Petpooja-607\Desktop\pkt

# Check structure
dir
# Should see: backend, frontend, knowledgebase folders
```

#### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure API key
# Open backend/.env and add your NVIDIA API key:
# META_API_KEY=nvapi-YOUR_KEY_HERE

# Test backend
python main.py
# Should see: "✅ Using Meta Muse Glimmer"
# Backend runs on: http://localhost:8001
```

#### 3. Frontend Setup
```bash
# Open new terminal
cd C:\Users\Petpooja-607\Desktop\pkt\frontend

# Install Node dependencies
npm install

# Start frontend
npm start
# Frontend runs on: http://localhost:3000
```

#### 4. Access Dashboard
- Open browser: **http://localhost:3000**
- Upload PDFs in "Manage Documents"
- Start asking questions!

### Creating Desktop Shortcuts

#### Backend Shortcut
1. Right-click `backend/start_backend.bat`
2. Create shortcut
3. Move to Desktop
4. Rename: "Petpooja Exam - Backend"

#### Frontend Shortcut
Create `frontend/start_frontend.bat`:
```batch
@echo off
cd /d "%~dp0"
npm start
pause
```

---

## Network Deployment (Multiple Users - Same Network)

Perfect for: Office, lab, classroom (5-20 users)

### Architecture
```
Server Computer (Windows)
├── Backend: http://SERVER_IP:8001
├── Frontend: http://SERVER_IP:3000
└── Users access via browser on same network
```

### Step 1: Find Server IP Address
```bash
# On server computer, open CMD
ipconfig

# Look for IPv4 Address, example:
# IPv4 Address: 192.168.1.100
```

### Step 2: Configure Backend for Network Access

Edit `backend/main.py` (already configured):
```python
# Line 27-28
PORT=8001
HOST=0.0.0.0  # Allows network access
```

### Step 3: Configure Frontend for Network Access

Edit `frontend/.env`:
```env
# Change from localhost to server IP
REACT_APP_API_URL=http://192.168.1.100:8001
```

Rebuild frontend:
```bash
cd frontend
npm run build
```

### Step 4: Install Windows Firewall Rules

```powershell
# Run PowerShell as Administrator

# Allow Backend port 8001
New-NetFirewallRule -DisplayName "Petpooja Backend" -Direction Inbound -LocalPort 8001 -Protocol TCP -Action Allow

# Allow Frontend port 3000
New-NetFirewallRule -DisplayName "Petpooja Frontend" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
```

### Step 5: Start Services

**Backend:**
```bash
cd backend
python main.py
```

**Frontend:**
```bash
cd frontend
npm start
```

### Step 6: User Access

Users on same network open browser:
- **http://192.168.1.100:3000** (replace with your server IP)

### Making it Permanent (Windows Service)

Install as Windows Service using `nssm`:

**Download NSSM:**
```bash
# Download from: https://nssm.cc/download
# Extract to C:\nssm
```

**Install Backend Service:**
```cmd
cd C:\nssm\win64
nssm install PetpoojaBackend

# In NSSM GUI:
Path: C:\Python\python.exe
Startup directory: C:\Users\Petpooja-607\Desktop\pkt\backend
Arguments: main.py
```

**Install Frontend Service:**
```cmd
nssm install PetpoojaFrontend

# In NSSM GUI:
Path: C:\Program Files\nodejs\npm.cmd
Startup directory: C:\Users\Petpooja-607\Desktop\pkt\frontend
Arguments: start
```

---

## Cloud Deployment (Internet Access)

Perfect for: Remote teams, widespread access

### Option 1: Heroku (Easiest - FREE tier available)

#### Prepare for Heroku

**Backend Heroku Setup:**

Create `backend/Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Create `backend/runtime.txt`:
```
python-3.10.13
```

**Frontend Heroku Setup:**

Create `frontend/static.json`:
```json
{
  "root": "build/",
  "routes": {
    "/**": "index.html"
  }
}
```

#### Deploy Backend
```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create backend app
cd backend
heroku create petpooja-exam-backend

# Set environment variables
heroku config:set META_API_KEY=nvapi-YOUR_KEY_HERE

# Deploy
git init
git add .
git commit -m "Deploy backend"
git push heroku master

# Note the URL: https://petpooja-exam-backend.herokuapp.com
```

#### Deploy Frontend
```bash
cd frontend

# Update .env with backend URL
# REACT_APP_API_URL=https://petpooja-exam-backend.herokuapp.com

# Create frontend app
heroku create petpooja-exam-frontend
heroku buildpacks:add heroku/nodejs

# Build
npm run build

# Deploy
git init
git add .
git commit -m "Deploy frontend"
git push heroku master

# Access: https://petpooja-exam-frontend.herokuapp.com
```

### Option 2: Vercel + Railway (Modern Stack)

#### Deploy Backend to Railway

1. Go to: https://railway.app/
2. Sign up / Login
3. Click "New Project" → "Deploy from GitHub"
4. Connect your repo or upload backend folder
5. Set environment variables:
   - `META_API_KEY=nvapi-YOUR_KEY`
   - `PORT=8001`
6. Railway auto-detects Python and deploys
7. Note the URL: https://petpooja-backend.railway.app

#### Deploy Frontend to Vercel

1. Go to: https://vercel.com/
2. Sign up / Login
3. Click "Import Project"
4. Upload frontend folder
5. Set environment variable:
   - `REACT_APP_API_URL=https://petpooja-backend.railway.app`
6. Vercel auto-builds and deploys
7. Access: https://petpooja-exam.vercel.app

### Option 3: AWS EC2 (Advanced - Full Control)

**Launch EC2 Instance:**
1. AWS Console → EC2 → Launch Instance
2. Choose: Ubuntu Server 22.04 LTS
3. Instance type: t2.medium (for 20+ users)
4. Security Group:
   - Port 22 (SSH)
   - Port 8001 (Backend)
   - Port 3000 (Frontend)
5. Launch and download key pair

**Connect to EC2:**
```bash
ssh -i "key.pem" ubuntu@ec2-XX-XX-XX-XX.compute.amazonaws.com
```

**Install Dependencies:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install PM2 (process manager)
sudo npm install -g pm2
```

**Upload Project:**
```bash
# From local machine
scp -i "key.pem" -r C:\Users\Petpooja-607\Desktop\pkt ubuntu@ec2-XX-XX:~/
```

**Setup Backend:**
```bash
cd ~/pkt/backend
pip3 install -r requirements.txt

# Create .env
nano .env
# Add: META_API_KEY=nvapi-YOUR_KEY

# Start with PM2
pm2 start main.py --name petpooja-backend --interpreter python3
pm2 save
pm2 startup
```

**Setup Frontend:**
```bash
cd ~/pkt/frontend
npm install
npm run build

# Serve with PM2
pm2 serve build 3000 --name petpooja-frontend --spa
pm2 save
```

**Configure Nginx (Optional - for production):**
```bash
sudo apt install nginx -y

# Create config
sudo nano /etc/nginx/sites-available/petpooja

# Add:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8001;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/petpooja /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Access:**
- Direct: http://EC2_PUBLIC_IP:3000
- With domain: http://your-domain.com

---

## User Guide

### For End Users

#### 1. Access the Dashboard
- Open browser (Chrome, Edge, Firefox)
- Navigate to provided URL
- Example: http://192.168.1.100:3000

#### 2. First Time Setup (Admin Only)

**Upload Study Materials:**
1. Click **"📚 Manage Documents"**
2. Click **"Upload PDF"**
3. Select Petpooja documentation PDFs:
   - POS user manual
   - Dashboard guide
   - Payroll (Attendo) documentation
   - Finance module guide
4. Wait for processing (5-10 seconds per file)
5. Verify "Uploaded Documents" list

#### 3. Ask Questions

**Method 1: Screenshot (Recommended for MCQ)**
1. Take screenshot of MCQ question (Windows: Win+Shift+S)
2. Click in search box
3. Press **Ctrl+V** to paste screenshot
4. Optionally add text context
5. Click **"Get Answer"**
6. Wait 3-5 seconds
7. Review answer (bold option is correct)

**Method 2: Text Only**
1. Type question in search box
2. Click **"Get Answer"**
3. Review answer with reasoning

#### 4. Interpret Results

**Answer Format:**
```
Answer: B) Split Bill

Reasoning: The "Split Bill" feature in Petpooja POS 
is specifically designed for dividing bills...

Keywords: POS, split, billing, feature
Confidence: 95%
Sources: pos_manual.pdf, billing_guide.pdf
```

**Understanding Scores:**
- **90-100%**: Very confident, highly relevant materials found
- **70-89%**: Good confidence, supporting materials available
- **50-69%**: Moderate confidence, limited materials
- **<50%**: Low confidence, upload more study materials

#### 5. Tips for Best Results

✅ **DO:**
- Use clear, high-resolution screenshots
- Include complete question and all options
- Upload comprehensive study materials
- Review reasoning, not just answer
- Cross-verify with your knowledge

❌ **DON'T:**
- Crop important parts of question
- Use blurry screenshots
- Rely solely on AI without understanding
- Skip uploading study materials

---

## Maintenance & Updates

### Updating Study Materials
1. Access "Manage Documents"
2. Remove outdated PDFs
3. Upload new versions
4. System automatically re-indexes

### Monitoring System Health

**Check Backend Status:**
- Open: http://SERVER_IP:8001/docs
- Should show FastAPI documentation

**Check Logs:**
```bash
# Backend logs
cd backend
# Look at terminal output

# Frontend logs
cd frontend
# Look at terminal output
```

### Troubleshooting

**Problem: "Connection refused"**
- Check if backend is running
- Verify firewall settings
- Confirm correct IP/port

**Problem: "AI service not configured"**
- Check .env file has META_API_KEY
- Verify API key is valid
- Restart backend

**Problem: "No relevant information found"**
- Upload more study materials
- Check PDF quality and text extraction
- Verify PDFs are about Petpooja products

**Problem: Slow responses**
- Check internet connection
- Verify API key has rate limits
- Consider upgrading server resources

### Backup Strategy

**Regular Backups:**
```bash
# Backup knowledge base
xcopy knowledgebase knowledgebase_backup /E /I /H /Y

# Backup configuration
copy backend\.env backend\.env.backup

# Backup uploaded documents
xcopy uploaded_documents uploaded_documents_backup /E /I /Y
```

---

## Cost Breakdown

### Local/Network Deployment
- **Cost**: FREE
- **Requirements**: Existing computer
- **Users**: 1-20 (depending on computer specs)

### Heroku Deployment
- **Free Tier**: 
  - 550-1000 dyno hours/month
  - Good for: 5-10 concurrent users
- **Paid**: $7-$25/month for 24/7 uptime

### Vercel + Railway
- **Free Tier**:
  - Vercel: Generous free tier
  - Railway: $5 credit/month
  - Good for: 10-20 users
- **Paid**: ~$10-20/month

### AWS EC2
- **Free Tier**: t2.micro (1 year)
  - Good for: 5-10 users
- **Paid**: $15-50/month (t2.medium)
  - Good for: 50+ concurrent users

### API Costs
- **Meta Muse via NVIDIA**: **FREE** (unlimited!)
- No hidden costs for AI usage

---

## Security Considerations

### For Production Deployment:

1. **Enable HTTPS:**
   - Use Let's Encrypt (free SSL certificates)
   - Configure nginx with SSL

2. **Add Authentication:**
   - Implement user login system
   - Restrict document upload to admins

3. **Rate Limiting:**
   - Prevent API abuse
   - Limit requests per user

4. **Environment Variables:**
   - Never commit .env to git
   - Use secret management systems

5. **Regular Updates:**
   - Keep dependencies updated
   - Monitor security advisories

---

## Support & Documentation

### Additional Files Created:
- `SETUP_META_MUSE.md` - Meta Muse API setup
- `PETPOOJA_MCQ_GUIDE.md` - MCQ user guide
- `LOGICAL_REASONING_FEATURES.md` - AI reasoning details

### Quick Links:
- Meta Muse API: https://build.nvidia.com/meta/muse-glimmer-30b
- FastAPI Docs: http://localhost:8001/docs
- GitHub Issues: (create repository for bug tracking)

### Getting Help:
1. Check troubleshooting section
2. Review logs for error messages
3. Verify all prerequisites installed
4. Test with simple question first
5. Contact system administrator

---

## Next Steps

1. ✅ Choose deployment method (Local/Network/Cloud)
2. ✅ Follow step-by-step instructions
3. ✅ Upload Petpooja documentation PDFs
4. ✅ Test with sample MCQ questions
5. ✅ Share access with users
6. ✅ Monitor and maintain system

Good luck with your Petpooja exam preparation! 🎓
