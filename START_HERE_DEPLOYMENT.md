# 🚀 START HERE - Deployment Quick Guide

**Welcome! This is your complete guide to deploying the Petpooja Exam Dashboard.**

---

## 📖 Choose Your Path:

### 👤 For End Users (Just want to use it)
**→ Read: `USER_GUIDE_SIMPLE.md`**
- How to ask questions
- How to paste screenshots
- How to understand answers

### 🔧 For System Admins (Setting it up)
**→ Follow this guide below**

### 💻 For Developers (Want technical details)
**→ Read: `README.md` and `DEPLOYMENT_GUIDE.md`**

---

## ⚡ Quick 3-Step Deployment

### Step 1: Install (5 minutes)
```bash
# Double-click this file:
INSTALL_DEPENDENCIES.bat

# Wait for installation to complete
# You'll see: "Installation Complete!"
```

### Step 2: Configure (2 minutes)
1. Get FREE API key from: https://build.nvidia.com/meta/muse-glimmer-30b
2. Open: `backend/.env`
3. Replace this line:
   ```
   META_API_KEY=your_meta_api_key_here
   ```
   With your actual key:
   ```
   META_API_KEY=nvapi-YOUR_ACTUAL_KEY_HERE
   ```
4. Save file

### Step 3: Start (1 minute)
```bash
# Double-click this file:
START_ALL.bat

# Wait 15 seconds
# Two windows will open (Backend & Frontend)
```

### Step 4: Use! ✅
1. Open browser: **http://localhost:3000**
2. Upload Petpooja PDFs in "Manage Documents"
3. Paste MCQ screenshots and get answers!

---

## 📋 Deployment Scenarios

### Scenario A: Local (Just Me)
**Time**: 10 minutes  
**Cost**: FREE  
**Users**: 1  

**What you need:**
- Your computer
- Python & Node.js installed
- Internet for API calls

**Follow:**
1. Run `INSTALL_DEPENDENCIES.bat`
2. Add API key to `backend/.env`
3. Run `START_ALL.bat`
4. Open http://localhost:3000

**Files to read:**
- ✅ README.md (overview)
- ✅ USER_GUIDE_SIMPLE.md (how to use)

---

### Scenario B: Network (5-20 Users in Office)
**Time**: 30 minutes  
**Cost**: FREE (uses your server)  
**Users**: 5-20  

**What you need:**
- Windows server/computer
- Same network as users
- Python & Node.js installed
- Admin access for firewall

**Follow:**
1. Complete Scenario A first
2. Find server IP: Run `ipconfig` → Note IPv4 Address
3. Open `frontend/.env`, change to:
   ```
   REACT_APP_API_URL=http://YOUR_SERVER_IP:8001
   ```
4. Rebuild frontend:
   ```bash
   cd frontend
   npm run build
   ```
5. Open firewall ports:
   ```powershell
   # Run PowerShell as Admin:
   New-NetFirewallRule -DisplayName "Petpooja Backend" -Direction Inbound -LocalPort 8001 -Protocol TCP -Action Allow
   New-NetFirewallRule -DisplayName "Petpooja Frontend" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
   ```
6. Start services with `START_ALL.bat`
7. Share URL with users: `http://YOUR_SERVER_IP:3000`

**Files to read:**
- ✅ DEPLOYMENT_GUIDE.md (Network Deployment section)
- ✅ DEPLOYMENT_CHECKLIST.md (verify everything)

---

### Scenario C: Cloud (Unlimited Users via Internet)
**Time**: 1-2 hours  
**Cost**: $0-$50/month  
**Users**: Unlimited  

**Options:**

#### Option 1: Heroku (Easiest)
1. Sign up: https://heroku.com
2. Install Heroku CLI
3. Deploy backend, then frontend
4. Share Heroku URL with users

#### Option 2: Vercel + Railway (Modern)
1. Backend → Railway: https://railway.app
2. Frontend → Vercel: https://vercel.com
3. Share Vercel URL with users

#### Option 3: AWS EC2 (Advanced)
1. Launch EC2 instance
2. Install dependencies
3. Upload project
4. Configure and start

**Files to read:**
- ✅ DEPLOYMENT_GUIDE.md (Cloud Deployment section)
- ✅ Full step-by-step instructions included

---

## 📁 Important Files Reference

### Must-Read Documents:
| File | When to Read | Who Should Read |
|------|-------------|----------------|
| **START_HERE_DEPLOYMENT.md** | First! | Admins |
| **USER_GUIDE_SIMPLE.md** | Before using | End Users |
| **README.md** | For overview | Everyone |
| **DEPLOYMENT_GUIDE.md** | When deploying | Admins/Devs |
| **DEPLOYMENT_CHECKLIST.md** | During deployment | Admins |

### Configuration Files:
| File | Purpose |
|------|---------|
| `backend/.env` | API keys and config |
| `frontend/.env` | Backend URL config |
| `backend/requirements.txt` | Python dependencies |
| `frontend/package.json` | Node dependencies |

### Batch Scripts:
| File | Purpose |
|------|---------|
| `INSTALL_DEPENDENCIES.bat` | Install everything |
| `START_ALL.bat` | Start both services |
| `STOP_ALL.bat` | Stop all services |

---

## 🎯 Checklist Before Starting

### Prerequisites Check:
- [ ] Python 3.8+ installed
  ```bash
  python --version
  ```
- [ ] Node.js 14+ installed
  ```bash
  node --version
  ```
- [ ] NVIDIA API account created
- [ ] FREE API key obtained
- [ ] Internet connection available
- [ ] 4GB RAM available
- [ ] 5GB disk space available

### Decision Made:
- [ ] Decided: Local / Network / Cloud deployment
- [ ] Read appropriate section in DEPLOYMENT_GUIDE.md
- [ ] Have necessary access (admin rights if network/server)
- [ ] Understand time and cost requirements

---

## ⚠️ Common First-Time Issues

### Issue 1: Python not found
```bash
Error: 'python' is not recognized...
```
**Fix:** Install Python from https://www.python.org/downloads/  
Make sure to check "Add Python to PATH" during installation.

### Issue 2: Node not found
```bash
Error: 'node' is not recognized...
```
**Fix:** Install Node.js from https://nodejs.org/

### Issue 3: Port already in use
```bash
Error: Address already in use (8001 or 3000)
```
**Fix:** 
```bash
# Run STOP_ALL.bat first
STOP_ALL.bat

# Then start again
START_ALL.bat
```

### Issue 4: Module not found
```bash
Error: No module named 'fastapi'
```
**Fix:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue 5: API key error
```bash
Error: Authorization failed (403)
```
**Fix:**
1. Check API key is correct in `backend/.env`
2. Get new key from https://build.nvidia.com/meta/muse-glimmer-30b
3. Restart backend

---

## 🔧 After Successful Start

### You Should See:

**Backend Window:**
```
✅ Using Meta Muse Glimmer (FREE via NVIDIA! - Multimodal Text+Image)
🤖 Meta Muse Glimmer initialized with model: meta/muse-glimmer-30b
INFO: Uvicorn running on http://0.0.0.0:8001
```

**Frontend Window:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.X.X:3000
```

**Browser:**
- Dashboard loads at http://localhost:3000
- You see "Exam Preparation Assistant"
- Search box is visible
- "Manage Documents" button works

### First Actions:

1. **Upload Study Materials:**
   - Click "📚 Manage Documents"
   - Upload Petpooja PDFs
   - Wait for processing
   - Verify in document list

2. **Test with Question:**
   - Type: "What is Petpooja POS?"
   - Click "Get Answer"
   - Wait 3-5 seconds
   - See answer with confidence score

3. **Test Screenshot:**
   - Take screenshot of any text
   - Click in search box
   - Press Ctrl+V
   - Ask a question
   - Get answer

---

## 📚 Study Materials to Upload

### Recommended PDFs to add:

**Petpooja POS:**
- [ ] User manual
- [ ] Feature guide
- [ ] Billing documentation
- [ ] Menu management guide

**Petpooja Dashboard:**
- [ ] Analytics guide
- [ ] Reports documentation
- [ ] User manual

**Petpooja Payroll (Attendo):**
- [ ] Attendance guide
- [ ] Payroll processing manual
- [ ] Leave management docs

**Petpooja Finance:**
- [ ] Accounting guide
- [ ] Expense management
- [ ] Financial reports docs

**General:**
- [ ] Training materials
- [ ] FAQ documents
- [ ] Quick reference guides

---

## 🎓 Training Your Users

### What Users Need to Know:

1. **Access URL**: http://localhost:3000 (or your URL)
2. **How to paste screenshots**: Ctrl+V
3. **Bold answer is correct**: Look for bold option in screenshot
4. **Read reasoning**: Understand why, don't just memorize
5. **Check confidence**: 90%+ is very reliable

### Quick User Training (5 minutes):

1. Show how to access dashboard
2. Demo pasting a screenshot
3. Show where answer appears
4. Explain confidence score
5. Share USER_GUIDE_SIMPLE.md

---

## 📞 Getting Help

### Self-Service:
1. Check **TROUBLESHOOTING** section in DEPLOYMENT_GUIDE.md
2. Review **DEPLOYMENT_CHECKLIST.md** for missed steps
3. Read **README.md** for technical details
4. Check terminal windows for error messages

### Documentation:
- Technical issues → DEPLOYMENT_GUIDE.md
- User questions → USER_GUIDE_SIMPLE.md
- Feature details → PETPOOJA_MCQ_GUIDE.md
- API setup → SETUP_META_MUSE.md

### Logs:
- Backend logs: Check backend terminal window
- Frontend logs: Check frontend terminal window
- Browser console: Press F12 → Console tab

---

## ✅ Success Checklist

Your deployment is successful when you can:

- [ ] Open dashboard at http://localhost:3000
- [ ] Upload a PDF successfully
- [ ] Ask a text question and get answer
- [ ] Paste a screenshot (Ctrl+V)
- [ ] See answer with confidence score
- [ ] Answer identifies bold option correctly
- [ ] Reasoning is provided
- [ ] Sources are listed
- [ ] System is stable (no crashes)

---

## 🚀 Next Steps After Deployment

### Immediate (Today):
1. Upload all available Petpooja documentation
2. Test with 5-10 sample questions
3. Verify accuracy is good
4. Share URL with initial users
5. Collect feedback

### This Week:
1. Monitor system stability
2. Add more study materials
3. Train more users
4. Document any issues
5. Optimize based on usage

### Ongoing:
1. Update study materials regularly
2. Keep dependencies updated
3. Monitor performance
4. Collect user feedback
5. Plan enhancements

---

## 🎉 You're Ready!

### Quick Start Command:
```bash
# Run these in order:
1. INSTALL_DEPENDENCIES.bat (once)
2. Edit backend/.env with API key (once)
3. START_ALL.bat (every time you use it)
```

### Access:
**Dashboard:** http://localhost:3000  
**API Docs:** http://localhost:8001/docs

### What to Do Now:
1. ✅ Follow Quick 3-Step Deployment above
2. ✅ Upload Petpooja PDFs
3. ✅ Test with questions
4. ✅ Share with users
5. ✅ Enjoy automated exam prep! 🎓

---

**Need help? Check:**
- DEPLOYMENT_GUIDE.md (full details)
- DEPLOYMENT_CHECKLIST.md (step-by-step)
- USER_GUIDE_SIMPLE.md (for users)

**Good luck with your deployment!** 🚀

---

*Last updated: September 2026*  
*Version: 1.0*
