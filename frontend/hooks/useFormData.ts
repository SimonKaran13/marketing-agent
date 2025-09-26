import { useState } from 'react'
import { InputPromptData } from '../types'

const initialFormData: InputPromptData = {
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
}

export function useFormData() {
  const [formData, setFormData] = useState<InputPromptData>(initialFormData)
  const [uploadedImages, setUploadedImages] = useState<File[]>([])
  const [imagePreviewUrls, setImagePreviewUrls] = useState<string[]>([])

  const handleInputChange = (field: keyof InputPromptData, value: string | string[]) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleImagesChange = (files: File[], urls: string[]) => {
    setUploadedImages(files)
    setImagePreviewUrls(urls)
    
    setFormData(prev => ({
      ...prev,
      product_images: files.map(file => file.name)
    }))
  }

  const resetForm = () => {
    setFormData(initialFormData)
    setUploadedImages([])
    setImagePreviewUrls([])
  }

  return {
    formData,
    uploadedImages,
    imagePreviewUrls,
    handleInputChange,
    handleImagesChange,
    resetForm
  }
}
