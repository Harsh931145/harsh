# Knowledge Base Directory

This directory stores your exam preparation materials (PDF files).

## Usage

1. **Upload via Dashboard**: Use the "Manage Documents" interface to upload PDFs
2. **Manual Upload**: Copy PDF files directly into this folder, then click "Refresh Index"

## Supported Formats

- ✅ PDF files (.pdf)
- ❌ Other formats (DOCX, images, etc.) are not yet supported

## Important Notes

- **File Names**: Use descriptive names for easier source identification
- **File Size**: Large PDFs (>100MB) may take longer to process
- **Index Files**: Don't delete `.index.faiss` or `.documents.pkl` (auto-generated)
- **Backup**: Keep original PDFs backed up elsewhere

## Example Structure

```
knowledgebase/
├── biology-chapter-1.pdf
├── chemistry-formulas.pdf
├── physics-mechanics.pdf
├── .index.faiss          # Auto-generated search index
└── .documents.pkl        # Auto-generated metadata
```

## Processing

When you upload a PDF:
1. Text is extracted from all pages
2. Content is split into searchable chunks
3. Semantic embeddings are created
4. Index is updated for fast retrieval

## Tips for Best Results

- **Quality**: Use PDFs with clear, OCR-processed text
- **Organization**: Group related topics in single PDFs
- **Updates**: Refresh the index after manual file additions
- **Cleanup**: Remove outdated materials to improve relevance

## Troubleshooting

**Problem**: PDF uploaded but not searchable
- **Solution**: Click "Refresh Index" in Document Manager

**Problem**: Scanned PDF not working
- **Solution**: Use an OCR tool to make the PDF text-searchable first

**Problem**: Out of memory error
- **Solution**: Reduce number of PDFs or split large files
