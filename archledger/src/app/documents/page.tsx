import { createClient } from '../../lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'
import UploadForm from './UploadForm'

export default async function DocumentsVaultPage() {
  const supabase = await createClient()

  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) redirect('/login')

  const { data: projectsData } = await supabase
    .from('projects')
    .select('id, project_name')
    .order('created_at', { ascending: false })
  
  const projects = projectsData || []

  // Secure Server Action
  const uploadDocument = async (formData: FormData) => {
    'use server'
    const supabase = await createClient()

    const projectId = formData.get('project_id') as string
    const description = formData.get('description') as string
    const file = formData.get('document') as File

    if (!file || file.size === 0) return

    const fileExt = file.name.split('.').pop()
    const uniqueFileName = `${Date.now()}-${Math.random().toString(36).substring(2)}.${fileExt}`
    const filePath = `${projectId}/${uniqueFileName}`

    const { error: uploadError } = await supabase.storage.from('documents').upload(filePath, file)
    if (uploadError) {
      console.error("Storage Error:", uploadError.message)
      return
    }

    const { data: { publicUrl } } = supabase.storage.from('documents').getPublicUrl(filePath)

    const { error: dbError } = await supabase.from('project_documents').insert({
      project_id: projectId,
      file_name: description,
      file_url: publicUrl,
      file_type: file.type
    })

    if (!dbError) redirect(`/projects/${projectId}`)
  }

  return (
    <main className="min-h-screen bg-slate-50 p-8 flex items-center justify-center">
      <div className="w-full max-w-2xl bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">Document & Receipt Vault</h1>
            <p className="text-sm text-slate-500 mt-1">Upload invoices, receipts, and compliance certificates.</p>
          </div>
          <Link href="/" className="px-4 py-2 text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition">
            Cancel
          </Link>
        </div>
        
        {/* Injecting our interactive Client Interface here */}
        <UploadForm projects={projects} uploadAction={uploadDocument} />
        
      </div>
    </main>
  )
}