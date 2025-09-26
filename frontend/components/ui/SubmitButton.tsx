interface SubmitButtonProps {
  isGenerating: boolean
  onSubmit: (e: React.FormEvent) => void
}

export default function SubmitButton({ isGenerating, onSubmit }: SubmitButtonProps) {
  return (
    <div className="form-actions">
      <button 
        type="submit" 
        className="button"
        disabled={isGenerating}
        onClick={onSubmit}
      >
        {isGenerating ? 'Generating...' : 'Generate Content'}
      </button>
    </div>
  )
}
