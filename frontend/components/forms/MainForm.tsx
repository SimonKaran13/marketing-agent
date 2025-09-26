import { useState } from 'react'
import ProductInfoForm from './ProductInfoForm'
import AdvancedOptionsForm from './AdvancedOptionsForm'
import ToggleButton from '../ui/ToggleButton'
import SubmitButton from '../ui/SubmitButton'

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

interface MainFormProps {
  formData: InputPromptData
  onInputChange: (field: keyof InputPromptData, value: string | string[]) => void
  uploadedImages: File[]
  imagePreviewUrls: string[]
  onImagesChange: (files: File[], urls: string[]) => void
  isGenerating: boolean
  onSubmit: (e: React.FormEvent) => void
}

export default function MainForm({
  formData,
  onInputChange,
  uploadedImages,
  imagePreviewUrls,
  onImagesChange,
  isGenerating,
  onSubmit
}: MainFormProps) {
  const [showAdvanced, setShowAdvanced] = useState(false)

  return (
    <section className="form-section">
      <form onSubmit={onSubmit} className="form">
        <ProductInfoForm
          formData={formData}
          onInputChange={onInputChange}
          uploadedImages={uploadedImages}
          imagePreviewUrls={imagePreviewUrls}
          onImagesChange={onImagesChange}
        />

        <ToggleButton
          isOpen={showAdvanced}
          onToggle={() => setShowAdvanced(!showAdvanced)}
          label="Advanced Photography & Styling Options"
        />

        {showAdvanced && (
          <AdvancedOptionsForm
            formData={formData}
            onInputChange={onInputChange}
          />
        )}
        
        <SubmitButton
          isGenerating={isGenerating}
          onSubmit={onSubmit}
        />
      </form>
    </section>
  )
}
