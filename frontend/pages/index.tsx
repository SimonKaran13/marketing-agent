import { useState } from 'react'
import Head from 'next/head'

interface InputPromptData {
  product_images: string[]
  product_name: string
  product_description: string
  product_main_features: string
  product_benefits: string
  product_use_cases: string
  product_pricing: string
  product_target_audience: string
  background_scene: string
  composition_style: string
  lighting_preferences: string
  mood: string
  camera_setup: string
  color_palette: string
  additional_modifiers: string
  style_presets: string[]
  format_presets: string[]
  shot_presets: string[]
  lighting_presets: string[]
  camera_angle_presets: string[]
  lens_presets: string[]
  environment_presets: string[]
  color_grade_presets: string[]
  post_processing_presets: string[]
}

export default function Home() {
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState<any>(null)
  const [parsedCaption, setParsedCaption] = useState<string>('')
  const [showPreview, setShowPreview] = useState(false)
  const [formData, setFormData] = useState<InputPromptData>({
    product_images: [],
    product_name: '',
    product_description: '',
    product_main_features: '',
    product_benefits: '',
    product_use_cases: '',
    product_pricing: '',
    product_target_audience: '',
    background_scene: '',
    composition_style: '',
    lighting_preferences: '',
    mood: '',
    camera_setup: '',
    color_palette: '',
    additional_modifiers: '',
    style_presets: [],
    format_presets: [],
    shot_presets: [],
    lighting_presets: [],
    camera_angle_presets: [],
    lens_presets: [],
    environment_presets: [],
    color_grade_presets: [],
    post_processing_presets: []
  })

  const handleInputChange = (field: keyof InputPromptData, value: string | string[]) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsGenerating(true)
    
    try {
      const response = await fetch('http://localhost:8000/start_workflow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      
      const result = await response.json()
      
      if (result.success) {
        // Parse the caption to extract the actual text
        try {
          let captionText = result.caption
          
          // Handle different caption formats
          if (typeof result.caption === 'string') {
            // Try to parse as JSON first
            try {
              const parsedCaption = JSON.parse(result.caption)
              
              // Extract text from content[0].text structure
              if (parsedCaption.content && parsedCaption.content[0] && parsedCaption.content[0].text) {
                captionText = parsedCaption.content[0].text
              }
            } catch (jsonError) {
              // Handle Python dictionary string format
              try {
                // Use eval to parse Python dict (only for trusted content)
                const parsedCaption = eval('(' + result.caption + ')')
                
                if (parsedCaption.content && parsedCaption.content[0] && parsedCaption.content[0].text) {
                  captionText = parsedCaption.content[0].text
                }
              } catch (evalError) {
                captionText = result.caption
              }
            }
          } else if (typeof result.caption === 'object' && result.caption !== null) {
            // Handle object format directly
            if (result.caption.content && result.caption.content[0] && result.caption.content[0].text) {
              captionText = result.caption.content[0].text
            }
          }
          
          setParsedCaption(captionText)
          setGeneratedContent(result)
          setShowPreview(true)
        } catch (parseError) {
          setParsedCaption(result.caption)
          setGeneratedContent(result)
          setShowPreview(true)
        }
      } else {
        alert(`Error: ${result.message}`)
      }
    } catch (error) {
      alert('Failed to generate content. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  // Loading component
  const LoadingSpinner = () => (
    <div className="loading-container">
      <div className="loading-spinner">
        <div className="spinner"></div>
        <p>Generating your content...</p>
        <p className="loading-subtitle">AI is crafting the perfect post for you</p>
      </div>
    </div>
  )

  // Content preview component
  const ContentPreview = () => (
    <div className="content-preview">
      <div className="preview-header">
        <button 
          className="back-button"
          onClick={() => setShowPreview(false)}
        >
          ← Back to Form
        </button>
        <h2>Your Generated Content</h2>
      </div>
      
      <div className="preview-content">
        <div className="preview-image">
          <img 
            src={generatedContent?.image || "https://via.placeholder.com/400x400/000000/FFFFFF?text=Product+Image"} 
            alt="Product"
            className="image-content"
          />
        </div>
        
        <div className="preview-caption">
          <div className="caption-header">
            <h3>Generated Caption</h3>
            <button 
              className="copy-caption-btn"
              onClick={() => {
                navigator.clipboard.writeText(parsedCaption)
                alert('Caption copied to clipboard!')
              }}
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
          onClick={() => {
            const link = document.createElement('a')
            link.href = generatedContent?.image || ""
            link.download = 'social-media-post.jpg'
            link.click()
          }}
        >
          📥 Download Image
        </button>
        <button 
          className="retry-button"
          onClick={() => setShowPreview(false)}
        >
          🔄 Generate New Content
        </button>
      </div>
    </div>
  )

  return (
    <>
      <Head>
        <title>AgenticMarketers</title>
        <meta name="description" content="AI-powered marketing content generation" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

          {isGenerating && <LoadingSpinner />}
          {showPreview && <ContentPreview />}
      
      {!isGenerating && !showPreview && (
      <main className="container">
        <header className="header">
          <h1 className="title">AgenticMarketers</h1>
          <p className="subtitle">AI-powered marketing content generation</p>
        </header>

        <section className="form-section">
          <form onSubmit={handleSubmit} className="form">
            {/* Essential Product Information */}
            <div className="form-section-header">
              <h2>Product Information</h2>
            </div>
            
            <div className="form-group">
              <label htmlFor="product_name" className="label">
                Product Name *
              </label>
              <input
                type="text"
                id="product_name"
                value={formData.product_name}
                onChange={(e) => handleInputChange('product_name', e.target.value)}
                placeholder="Acme Hydration Bottle"
                className="input"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="product_description" className="label">
                Product Description *
              </label>
              <textarea
                id="product_description"
                value={formData.product_description}
                onChange={(e) => handleInputChange('product_description', e.target.value)}
                placeholder="vacuum-insulated stainless steel water bottle"
                className="textarea"
                rows={2}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="product_main_features" className="label">
                  Key Features
                </label>
                <textarea
                  id="product_main_features"
                  value={formData.product_main_features}
                  onChange={(e) => handleInputChange('product_main_features', e.target.value)}
                  placeholder="double-wall insulation, leakproof lid, 24oz capacity"
                  className="textarea"
                  rows={1}
                />
              </div>

              <div className="form-group">
                <label htmlFor="product_benefits" className="label">
                  Benefits
                </label>
                <textarea
                  id="product_benefits"
                  value={formData.product_benefits}
                  onChange={(e) => handleInputChange('product_benefits', e.target.value)}
                  placeholder="keeps drinks cold for 24 hours, easy-carry loop"
                  className="textarea"
                  rows={1}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="product_use_cases" className="label">
                  Use Cases
                </label>
                <input
                  type="text"
                  id="product_use_cases"
                  value={formData.product_use_cases}
                  onChange={(e) => handleInputChange('product_use_cases', e.target.value)}
                  placeholder="outdoor adventures, gym sessions, commute"
                  className="input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="product_pricing" className="label">
                  Pricing Tier
                </label>
                <select
                  id="product_pricing"
                  value={formData.product_pricing}
                  onChange={(e) => handleInputChange('product_pricing', e.target.value)}
                  className="select"
                >
                  <option value="">Select pricing tier</option>
                  <option value="premium">Premium</option>
                  <option value="mid-tier">Mid-tier</option>
                  <option value="budget-friendly">Budget-friendly</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="product_target_audience" className="label">
                Target Audience
              </label>
              <input
                type="text"
                id="product_target_audience"
                value={formData.product_target_audience}
                onChange={(e) => handleInputChange('product_target_audience', e.target.value)}
                placeholder="designed for eco-conscious athletes"
                className="input"
              />
            </div>

            {/* Advanced Options Toggle */}
            <div className="advanced-toggle">
              <button
                type="button"
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="toggle-button"
              >
                {showAdvanced ? '▼' : '▶'} Advanced Photography & Styling Options
              </button>
            </div>

            {/* Advanced Options */}
            {showAdvanced && (
              <div className="advanced-section">
                <div className="form-section-header">
                  <h3>Photography & Styling</h3>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="background_scene" className="label">
                      Background Scene
                    </label>
                    <input
                      type="text"
                      id="background_scene"
                      value={formData.background_scene}
                      onChange={(e) => handleInputChange('background_scene', e.target.value)}
                      placeholder="sunlit alpine meadow, modern kitchen countertop"
                      className="input"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="composition_style" className="label">
                      Composition Style
                    </label>
                    <input
                      type="text"
                      id="composition_style"
                      value={formData.composition_style}
                      onChange={(e) => handleInputChange('composition_style', e.target.value)}
                      placeholder="rule of thirds composition, flat lay"
                      className="input"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="lighting_preferences" className="label">
                      Lighting Preferences
                    </label>
                    <input
                      type="text"
                      id="lighting_preferences"
                      value={formData.lighting_preferences}
                      onChange={(e) => handleInputChange('lighting_preferences', e.target.value)}
                      placeholder="dramatic rim lighting, soft daylight"
                      className="input"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="mood" className="label">
                      Mood
                    </label>
                    <input
                      type="text"
                      id="mood"
                      value={formData.mood}
                      onChange={(e) => handleInputChange('mood', e.target.value)}
                      placeholder="energetic, calm and minimalist"
                      className="input"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="camera_setup" className="label">
                      Camera Setup
                    </label>
                    <input
                      type="text"
                      id="camera_setup"
                      value={formData.camera_setup}
                      onChange={(e) => handleInputChange('camera_setup', e.target.value)}
                      placeholder="macro product shot, tripod-mounted studio setup"
                      className="input"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="color_palette" className="label">
                      Color Palette
                    </label>
                    <input
                      type="text"
                      id="color_palette"
                      value={formData.color_palette}
                      onChange={(e) => handleInputChange('color_palette', e.target.value)}
                      placeholder="teal and orange accents"
                      className="input"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="additional_modifiers" className="label">
                    Additional Modifiers
                  </label>
                  <textarea
                    id="additional_modifiers"
                    value={formData.additional_modifiers}
                    onChange={(e) => handleInputChange('additional_modifiers', e.target.value)}
                    placeholder="splashing water droplets, premium props"
                    className="textarea"
                    rows={1}
                  />
                </div>
              </div>
            )}
            
            <div className="form-actions">
              <button 
                type="submit" 
                className="button"
                disabled={isGenerating}
              >
                {isGenerating ? 'Generating...' : 'Generate Content'}
              </button>
            </div>
          </form>
        </section>

      </main>
      )}
    </>
  )
}
