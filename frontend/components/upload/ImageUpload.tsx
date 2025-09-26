interface ImageUploadProps {
  onImagesChange: (files: File[], urls: string[]) => void
  uploadedImages: File[]
  imagePreviewUrls: string[]
}

export default function ImageUpload({ onImagesChange, uploadedImages, imagePreviewUrls }: ImageUploadProps) {
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    if (files.length > 0) {
      // Take only the first file for single image upload
      const firstFile = files[0]
      const url = URL.createObjectURL(firstFile)
      onImagesChange([firstFile], [url])
    }
  }

  const removeImage = () => {
    onImagesChange([], [])
  }

  const hasImage = uploadedImages.length > 0

  return (
    <div className="form-group">
      <label htmlFor="product_image" className="label">
        Product Image
      </label>
      
      {!hasImage ? (
        <div className="single-image-upload">
          <input
            type="file"
            id="product_image"
            accept="image/*"
            onChange={handleImageUpload}
            className="file-input"
          />
          <label htmlFor="product_image" className="upload-area">
            <div className="upload-icon">📷</div>
            <div className="upload-text">
              <span className="upload-title">Upload Product Image</span>
              <span className="upload-subtitle">Click to browse or drag and drop</span>
            </div>
          </label>
        </div>
      ) : (
        <div className="image-preview-container">
          <div className="image-preview">
            <img src={imagePreviewUrls[0]} alt="Product preview" className="preview-image" />
            <button
              type="button"
              onClick={removeImage}
              className="remove-image-btn"
            >
              ✕
            </button>
          </div>
          <div className="image-info">
            <span className="image-name">{uploadedImages[0].name}</span>
            <span className="image-size">
              {(uploadedImages[0].size / 1024 / 1024).toFixed(2)} MB
            </span>
          </div>
        </div>
      )}
    </div>
  )
}
