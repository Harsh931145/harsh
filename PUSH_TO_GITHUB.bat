@echo off
echo ========================================
echo Pushing to GitHub Repository
echo ========================================
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Step 1: Checking Git status...
git status
echo.

echo Step 2: Adding all files...
git add .
echo.

echo Step 3: Committing changes...
git commit -m "Initial commit: Petpooja Exam Dashboard with AI MCQ analysis"
echo.

echo Step 4: Setting remote URL...
git remote set-url origin https://github.com/milanbpatel90-a11y/knowledgebase.git
echo.

echo Step 5: Renaming branch to main...
git branch -M main
echo.

echo Step 6: Pushing to GitHub...
echo This may take a minute...
git push -u origin main
echo.

if %errorlevel%==0 (
    echo ========================================
    echo SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo Repository: https://github.com/milanbpatel90-a11y/knowledgebase
    echo.
    echo Next steps:
    echo 1. Go to https://railway.app/
    echo 2. Deploy backend from your GitHub repo
    echo 3. Go to https://vercel.com/
    echo 4. Deploy frontend from your GitHub repo
    echo.
) else (
    echo ========================================
    echo ERROR: Push failed!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Not authenticated with GitHub
    echo 2. Repository doesn't exist
    echo 3. No internet connection
    echo.
    echo Please run: git push -u origin main
    echo And follow authentication prompts
    echo.
)

pause
