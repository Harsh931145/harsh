# Petpooja MCQ Exam Assistant - User Guide

## Overview
Your exam dashboard is specifically optimized for **Petpooja product MCQ questions** with screenshot analysis.

## Petpooja Products Coverage

### 1. **Petpooja POS (Point of Sale)**
- Restaurant management system
- Order processing
- Billing and payments
- Menu management
- Kitchen operations

### 2. **Petpooja Dashboard**
- Analytics and reporting
- Business insights
- Performance metrics
- Data visualization
- Management tools

### 3. **Petpooja Payroll (Attendo)**
- Employee attendance tracking
- Payroll processing
- Leave management
- Shift scheduling
- HR operations

### 4. **Petpooja Finance**
- Financial accounting
- Expense tracking
- Revenue management
- Tax calculations
- Financial reports

## How to Use

### Step 1: Take Screenshot
1. Navigate to your MCQ question
2. Ensure the screenshot shows:
   - ✅ Complete question text
   - ✅ All available options (A, B, C, D or numbered)
   - ✅ Clear, readable text

### Step 2: Upload to Dashboard
1. Open dashboard at http://localhost:3000
2. Click in the search box
3. **Paste screenshot**: Press `Ctrl+V`
   - OR click the image icon and browse files
   - OR drag-drop the image file

### Step 3: Add Context (Optional)
- Type additional context if needed
- Example: "This is about POS billing"
- Example: "Attendo attendance feature"

### Step 4: Get Answer
1. Click **"Get Answer"** button
2. Wait 3-5 seconds
3. View the answer with:
   - ✅ Selected option (A, B, C, or D)
   - ✅ Reasoning with keywords
   - ✅ Confidence score
   - ✅ Source references

## AI Analysis Process

The system uses **Meta Muse Glimmer 30B** (multimodal AI) to:

### 1. **Image Analysis**
- Read question text from screenshot
- Extract all MCQ options
- Identify Petpooja product mentioned

### 2. **Keyword Extraction**
- Identify key terms: "billing", "attendance", "report", etc.
- Recognize product names: POS, Dashboard, Attendo, Finance
- Extract feature names and functionality keywords

### 3. **Knowledge Base Search**
- Search uploaded PDFs for relevant information
- Find matching concepts and features
- Retrieve top 8 most relevant chunks

### 4. **Logical Reasoning**
- Eliminate obviously wrong options
- Match keywords with product knowledge
- Apply domain expertise about Petpooja products
- Consider common workflows and use cases

### 5. **Answer Selection**
- Choose the most logical option
- Provide clear reasoning
- Reference study materials
- Show confidence level

## Example Workflow

### Example Question (Screenshot):
```
Question: In Petpooja POS, which feature is used for splitting bills?
A) Table Transfer
B) Split Bill
C) Merge Orders
D) Quick Billing
```

### System Analysis:
1. **Keywords identified**: "POS", "splitting bills", "feature"
2. **Product context**: Petpooja POS
3. **Search PDFs**: Look for billing and split functionality
4. **Logical reasoning**: 
   - Table Transfer = moving tables, not splitting
   - Split Bill = directly related to splitting
   - Merge Orders = combining, opposite of splitting
   - Quick Billing = fast billing, not splitting

### System Answer:
```
Answer: B) Split Bill

Reasoning: The "Split Bill" feature in Petpooja POS is specifically designed 
for dividing a single bill into multiple parts. This matches the keyword 
"splitting bills" in the question. Other options like Table Transfer and 
Merge Orders serve different purposes.

Confidence: 95%
Sources: petpooja_pos_manual.pdf, billing_features.pdf
```

## Tips for Best Results

### 1. **Clear Screenshots**
- Use high resolution
- Ensure good contrast
- Capture complete question and options
- Avoid cropping options

### 2. **Upload Study Materials**
- Add Petpooja product PDFs to knowledge base
- Include user manuals, guides, training docs
- More documents = better accuracy

### 3. **Add Context**
- Mention the product if unclear in screenshot
- Add any special context about the question
- Examples: "This is from payroll module"

### 4. **Review Reasoning**
- Don't just look at the answer
- Read the reasoning to understand WHY
- Check confidence score
- Verify against your knowledge

## Uploading Study Materials

### What to Upload:
- ✅ Petpooja POS documentation
- ✅ Dashboard user guides
- ✅ Attendo/Payroll manuals
- ✅ Finance module documentation
- ✅ Training materials
- ✅ Feature descriptions
- ✅ FAQ documents

### How to Upload:
1. Click **"📚 Manage Documents"** in dashboard
2. Click **"Upload PDF"**
3. Select PDF files (can upload multiple)
4. Wait for processing (5-10 seconds per file)
5. Documents are automatically indexed

### Processing:
- PDFs are split into chunks
- Text is extracted and embedded
- Vector search enables semantic matching
- Takes ~5-10 seconds per file

## Troubleshooting

### Issue: "I couldn't find relevant information"
**Solution**: Upload more study materials about Petpooja products

### Issue: Low confidence score (<50%)
**Causes**:
- Screenshot is unclear
- Question about topic not in study materials
- Ambiguous question wording

**Solutions**:
- Retake clearer screenshot
- Add more PDFs about that topic
- Provide additional context in text box

### Issue: Wrong answer selected
**Causes**:
- Study materials have outdated information
- Question wording is tricky
- Missing context in screenshot

**Solutions**:
- Update study materials
- Add context: "This is about [specific feature]"
- Upload more comprehensive documentation

### Issue: Can't paste screenshot
**Solution**: Use alternative methods:
- Click image icon and browse file
- Drag-drop screenshot file
- Save screenshot and upload as file

## Performance Tips

### For Faster Answers:
1. Keep knowledge base updated (don't upload duplicates)
2. Use clear, high-quality screenshots
3. Pre-type product context before pasting image

### For Better Accuracy:
1. Upload comprehensive documentation
2. Include product-specific manuals
3. Add training materials and FAQs
4. Keep documents current and accurate

## System Features

### ✅ Multimodal AI
- Handles both text and images
- Powered by Meta Muse Glimmer 30B
- FREE via NVIDIA

### ✅ Smart Keyword Analysis
- Extracts key terms from questions
- Matches with product knowledge
- Expands synonyms and related terms

### ✅ Logical Reasoning
- Eliminates wrong options
- Applies domain knowledge
- Uses contextual understanding

### ✅ Vector Search
- Semantic similarity matching
- Finds relevant info even with different wording
- Scans 24 chunks, returns top 8

### ✅ Confidence Scoring
- Shows certainty level
- Based on relevance scores
- Helps you validate answers

## Support

### Getting Started:
1. Upload Petpooja documentation PDFs
2. Test with a few practice questions
3. Review answers and reasoning
4. Adjust by adding more materials

### Best Practices:
- Always review the reasoning, not just the answer
- Cross-verify with your own knowledge
- Use confidence score as a guide
- Report patterns of wrong answers to improve materials

### Backend Status:
- Backend: http://localhost:8001
- Frontend: http://localhost:3000
- AI Model: Meta Muse Glimmer 30B
- Status: ✅ Using Meta Muse Glimmer (FREE via NVIDIA!)

Good luck with your Petpooja product exam! 🎓
