export interface InputPromptData {
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

export interface WorkflowResponse {
  success: boolean
  message: string
  caption?: string
  image?: string
}
