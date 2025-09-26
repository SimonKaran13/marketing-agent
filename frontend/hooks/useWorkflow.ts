import { useState } from 'react'
import { InputPromptData, WorkflowResponse } from '../types'

export function useWorkflow() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState<WorkflowResponse | null>(null)
  const [parsedCaption, setParsedCaption] = useState<string>('')
  const [showPreview, setShowPreview] = useState(false)

  const parseCaption = (caption: any): string => {
    try {
      let captionText = caption
      
      if (typeof caption === 'string') {
        try {
          const parsedCaption = JSON.parse(caption)
          if (parsedCaption.content && parsedCaption.content[0] && parsedCaption.content[0].text) {
            captionText = parsedCaption.content[0].text
          }
        } catch (jsonError) {
          try {
            const parsedCaption = eval('(' + caption + ')')
            if (parsedCaption.content && parsedCaption.content[0] && parsedCaption.content[0].text) {
              captionText = parsedCaption.content[0].text
            }
          } catch (evalError) {
            captionText = caption
          }
        }
      } else if (typeof caption === 'object' && caption !== null) {
        if (caption.content && caption.content[0] && caption.content[0].text) {
          captionText = caption.content[0].text
        }
      }
      
      return captionText
    } catch (parseError) {
      return String(caption)
    }
  }

  const submitWorkflow = async (formData: InputPromptData, uploadedImages: File[]) => {
    setIsGenerating(true)
    
    try {
      const formDataToSend = new FormData()
      
      // Add form fields
      Object.entries(formData).forEach(([key, value]) => {
        if (key !== 'product_images') {
          if (Array.isArray(value)) {
            formDataToSend.append(key, JSON.stringify(value))
          } else {
            formDataToSend.append(key, value)
          }
        }
      })
      
      // Add uploaded images
      uploadedImages.forEach((file) => {
        formDataToSend.append('product_images', file)
      })
      
      const response = await fetch('http://localhost:8000/start_workflow', {
        method: 'POST',
        body: formDataToSend
      })
      
      const result = await response.json()
      
      if (result.success) {
        const caption = parseCaption(result.caption)
        setParsedCaption(caption)
        setGeneratedContent(result)
        setShowPreview(true)
      } else {
        alert(`Error: ${result.message}`)
      }
    } catch (error) {
      alert('Failed to generate content. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const backToForm = () => {
    setShowPreview(false)
  }

  return {
    isGenerating,
    generatedContent,
    parsedCaption,
    showPreview,
    submitWorkflow,
    backToForm
  }
}
