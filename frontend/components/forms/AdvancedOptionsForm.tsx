import FormField from './FormField'
import FormRow from './FormRow'

interface InputPromptData {
  background_scene: string
  composition_style: string
  lighting_preferences: string
  mood: string
  camera_setup: string
  color_palette: string
  additional_modifiers: string
}

interface AdvancedOptionsFormProps {
  formData: InputPromptData
  onInputChange: (field: keyof InputPromptData, value: string | string[]) => void
}

export default function AdvancedOptionsForm({ formData, onInputChange }: AdvancedOptionsFormProps) {
  return (
    <div className="advanced-section">
      <div className="form-section-header">
        <h3>Photography & Styling</h3>
      </div>

      <FormRow>
        <FormField
          id="background_scene"
          label="Background Scene"
          value={formData.background_scene}
          onChange={(value) => onInputChange('background_scene', value)}
          placeholder="sunlit alpine meadow, modern kitchen countertop"
        />

        <FormField
          id="composition_style"
          label="Composition Style"
          value={formData.composition_style}
          onChange={(value) => onInputChange('composition_style', value)}
          placeholder="rule of thirds composition, flat lay"
        />
      </FormRow>

      <FormRow>
        <FormField
          id="lighting_preferences"
          label="Lighting Preferences"
          value={formData.lighting_preferences}
          onChange={(value) => onInputChange('lighting_preferences', value)}
          placeholder="dramatic rim lighting, soft daylight"
        />

        <FormField
          id="mood"
          label="Mood"
          value={formData.mood}
          onChange={(value) => onInputChange('mood', value)}
          placeholder="energetic, calm and minimalist"
        />
      </FormRow>

      <FormRow>
        <FormField
          id="camera_setup"
          label="Camera Setup"
          value={formData.camera_setup}
          onChange={(value) => onInputChange('camera_setup', value)}
          placeholder="macro product shot, tripod-mounted studio setup"
        />

        <FormField
          id="color_palette"
          label="Color Palette"
          value={formData.color_palette}
          onChange={(value) => onInputChange('color_palette', value)}
          placeholder="teal and orange accents"
        />
      </FormRow>

      <FormField
        id="additional_modifiers"
        label="Additional Modifiers"
        type="textarea"
        value={formData.additional_modifiers}
        onChange={(value) => onInputChange('additional_modifiers', value)}
        placeholder="splashing water droplets, premium props"
        rows={1}
      />
    </div>
  )
}
