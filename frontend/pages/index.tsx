import Head from 'next/head'
import { Header, LoadingSpinner, ContentPreview, MainForm } from '../components'
import { useFormData } from '../hooks/useFormData'
import { useWorkflow } from '../hooks/useWorkflow'

export default function Home() {
  const {
    formData,
    uploadedImages,
    imagePreviewUrls,
    handleInputChange,
    handleImagesChange
  } = useFormData()

  const {
    isGenerating,
    generatedContent,
    parsedCaption,
    showPreview,
    submitWorkflow,
    backToForm
  } = useWorkflow()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await submitWorkflow(formData, uploadedImages)
  }

  return (
    <>
      <Head>
        <title>AgenticMarketers</title>
        <meta name="description" content="AI-powered marketing content generation" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {isGenerating && <LoadingSpinner />}
      {showPreview && (
        <ContentPreview
          generatedContent={generatedContent}
          parsedCaption={parsedCaption}
          onBackToForm={backToForm}
        />
      )}
      
      {!isGenerating && !showPreview && (
        <main className="container">
          <Header />
          <MainForm
            formData={formData}
            onInputChange={handleInputChange}
            uploadedImages={uploadedImages}
            imagePreviewUrls={imagePreviewUrls}
            onImagesChange={handleImagesChange}
            isGenerating={isGenerating}
            onSubmit={handleSubmit}
          />
        </main>
      )}
    </>
  )
}
