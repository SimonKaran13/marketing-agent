interface ContentPreviewProps {
  generatedContent: any
  parsedCaption: string
  onBackToForm: () => void
}

export default function ContentPreview({ generatedContent, parsedCaption, onBackToForm }: ContentPreviewProps) {
  const handleCopyCaption = () => {
    navigator.clipboard.writeText(parsedCaption)
    alert('Caption copied to clipboard!')
  }

  const handleDownloadImage = () => {
    const link = document.createElement('a')
    const imageUrl = generatedContent?.image ? `http://localhost:8000${generatedContent.image}` : ""
    link.href = imageUrl
    link.download = 'social-media-post.jpg'
    link.click()
  }

  return (
    <div className="content-preview">
      <div className="preview-header">
        <button 
          className="back-button"
          onClick={onBackToForm}
        >
          ← Back to Form
        </button>
        <h2>Your Generated Content</h2>
      </div>
      
      <div className="preview-content">
        <div className="preview-image">
          <img 
            src={generatedContent?.image ? `http://localhost:8000${generatedContent.image}` : "https://via.placeholder.com/400x400/000000/FFFFFF?text=Product+Image"} 
            alt="Product"
            className="image-content"
          />
        </div>
        
        <div className="preview-caption">
          <div className="caption-header">
            <h3>Generated Caption</h3>
            <button 
              className="copy-caption-btn"
              onClick={handleCopyCaption}
            >
              📋 Copy Caption
            </button>
          </div>
          <div className="caption-text">
            {parsedCaption}
          </div>
        </div>
      </div>
      
      <div className="preview-actions">
        <button 
          className="download-image-btn"
          onClick={handleDownloadImage}
        >
          📥 Download Image
        </button>
        <button 
          className="retry-button"
          onClick={onBackToForm}
        >
          🔄 Generate New Content
        </button>
      </div>
    </div>
  )
}
