import FormField from './FormField'
import FormRow from './FormRow'
import ImageUpload from '../upload/ImageUpload'

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

interface ProductInfoFormProps {
  formData: InputPromptData
  onInputChange: (field: keyof InputPromptData, value: string | string[]) => void
  uploadedImages: File[]
  imagePreviewUrls: string[]
  onImagesChange: (files: File[], urls: string[]) => void
}

export default function ProductInfoForm({ 
  formData, 
  onInputChange, 
  uploadedImages, 
  imagePreviewUrls, 
  onImagesChange 
}: ProductInfoFormProps) {
  const pricingOptions = [
    { value: 'premium', label: 'Premium' },
    { value: 'mid-tier', label: 'Mid-tier' },
    { value: 'budget-friendly', label: 'Budget-friendly' }
  ]

  return (
    <>
      <div className="form-section-header">
        <h2>Product Information</h2>
      </div>

      <ImageUpload
        onImagesChange={onImagesChange}
        uploadedImages={uploadedImages}
        imagePreviewUrls={imagePreviewUrls}
      />
      
      <FormField
        id="product_name"
        label="Product Name"
        value={formData.product_name}
        onChange={(value) => onInputChange('product_name', value)}
        placeholder="Acme Hydration Bottle"
        required
      />

      <FormField
        id="product_description"
        label="Product Description"
        type="textarea"
        value={formData.product_description}
        onChange={(value) => onInputChange('product_description', value)}
        placeholder="vacuum-insulated stainless steel water bottle"
        rows={2}
        required
      />

      <FormRow>
        <FormField
          id="product_main_features"
          label="Key Features"
          type="textarea"
          value={formData.product_main_features}
          onChange={(value) => onInputChange('product_main_features', value)}
          placeholder="double-wall insulation, leakproof lid, 24oz capacity"
          rows={1}
        />

        <FormField
          id="product_benefits"
          label="Benefits"
          type="textarea"
          value={formData.product_benefits}
          onChange={(value) => onInputChange('product_benefits', value)}
          placeholder="keeps drinks cold for 24 hours, easy-carry loop"
          rows={1}
        />
      </FormRow>

      <FormRow>
        <FormField
          id="product_use_cases"
          label="Use Cases"
          value={formData.product_use_cases}
          onChange={(value) => onInputChange('product_use_cases', value)}
          placeholder="outdoor adventures, gym sessions, commute"
        />

        <FormField
          id="product_pricing"
          label="Pricing Tier"
          type="select"
          value={formData.product_pricing}
          onChange={(value) => onInputChange('product_pricing', value)}
          placeholder="Select pricing tier"
          options={pricingOptions}
        />
      </FormRow>

      <FormField
        id="product_target_audience"
        label="Target Audience"
        value={formData.product_target_audience}
        onChange={(value) => onInputChange('product_target_audience', value)}
        placeholder="designed for eco-conscious athletes"
      />
    </>
  )
}
