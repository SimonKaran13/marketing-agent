export default function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="loading-spinner">
        <div className="spinner"></div>
        <p>Generating your content...</p>
        <p className="loading-subtitle">AI is crafting the perfect post for you</p>
      </div>
    </div>
  )
}
