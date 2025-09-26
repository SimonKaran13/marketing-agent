import { ReactNode } from 'react'

interface FormRowProps {
  children: ReactNode
}

export default function FormRow({ children }: FormRowProps) {
  return (
    <div className="form-row">
      {children}
    </div>
  )
}
