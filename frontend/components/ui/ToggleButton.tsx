interface ToggleButtonProps {
  isOpen: boolean
  onToggle: () => void
  label: string
}

export default function ToggleButton({ isOpen, onToggle, label }: ToggleButtonProps) {
  return (
    <div className="advanced-toggle">
      <button
        type="button"
        onClick={onToggle}
        className="toggle-button"
      >
        {isOpen ? '▼' : '▶'} {label}
      </button>
    </div>
  )
}
