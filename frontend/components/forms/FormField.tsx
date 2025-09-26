interface FormFieldProps {
  id: string
  label: string
  type?: 'text' | 'textarea' | 'select'
  value: string
  onChange: (value: string) => void
  placeholder?: string
  required?: boolean
  options?: { value: string; label: string }[]
  rows?: number
}

export default function FormField({
  id,
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  required = false,
  options = [],
  rows = 1
}: FormFieldProps) {
  const renderInput = () => {
    switch (type) {
      case 'textarea':
        return (
          <textarea
            id={id}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
            className="textarea"
            rows={rows}
            required={required}
          />
        )
      case 'select':
        return (
          <select
            id={id}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="select"
            required={required}
          >
            <option value="">{placeholder}</option>
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        )
      default:
        return (
          <input
            type="text"
            id={id}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
            className="input"
            required={required}
          />
        )
    }
  }

  return (
    <div className="form-group">
      <label htmlFor={id} className="label">
        {label} {required && '*'}
      </label>
      {renderInput()}
    </div>
  )
}
