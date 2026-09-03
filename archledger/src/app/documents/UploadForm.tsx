'use client'

import { useState } from 'react'

type Project = { id: string; project_name: string }

export default function UploadForm({ projects, uploadAction }: { projects: Project[], uploadAction: (formData: FormData) => Promise<void> }) {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string | null>(null)
  const [isImage, setIsImage] = useState<boolean>(false)
  const [isUploading, setIsUploading] = useState<boolean>(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setFileName(file.name)
      if (file.type.startsWith('image/')) {
        setPreviewUrl(URL.createObjectURL(file))
        setIsImage(true)
      } else {
        setPreviewUrl(null)
        setIsImage(false)
      }
    }
  }

  return (
    <form 
      action={(formData) => {
        setIsUploading(true)
        uploadAction(formData)
      }} 
      className="flex flex-col gap-6"
    >
      <div className="bg-slate-50 p-5 rounded-2xl border border-slate-200">
        <label className="block text-sm font-bold text-slate-700 mb-2">Select Destination Project</label>
        {projects.length === 0 ? (
          <div className="w-full p-3 border border-red-300 rounded-lg bg-red-50 text-red-700 text-sm font-medium">
            No active projects found. Create a project first.
          </div>
        ) : (
          <select name="project_id" required className="w-full p-3.5 border border-slate-300 rounded-xl text-slate-900 font-bold bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm">
            <option value="">-- Route Document to Project --</option>
            {projects.map((p) => (
              <option key={p.id} value={p.id}>{p.project_name}</option>
            ))}
          </select>
        )}
      </div>

      <div>
        <label className="block text-sm font-bold text-slate-700 mb-1.5">Document Description</label>
        <input type="text" name="description" required className="w-full p-3.5 border border-slate-300 rounded-xl text-slate-900 font-medium bg-white focus:outline-none focus:ring-2 focus:ring-amber-500" placeholder="e.g., Dangote Cement Invoice #4092" />
      </div>
      
      {/* Premium Live Preview Zone */}
      <div className="border-2 border-dashed border-slate-300 rounded-2xl p-8 text-center bg-slate-50 hover:bg-slate-100 transition relative overflow-hidden">
        
        {/* Invisible Overlay Input to trigger file selection */}
        <input 
          type="file" 
          name="document" 
          required 
          accept=".pdf, image/jpeg, image/png, image/webp"
          onChange={handleFileChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
        />

        {!fileName ? (
          <div>
            <div className="text-4xl mb-3">📄</div>
            <label className="block text-sm font-bold text-slate-900 mb-1">Click to select a file</label>
            <p className="text-xs text-slate-500 font-medium mt-2">PDF, JPG, or PNG (Max: 5MB)</p>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center">
            {isImage && previewUrl ? (
              <img src={previewUrl} className="max-h-48 rounded-xl shadow-sm mb-3 object-contain" alt="Preview" />
            ) : (
              <div className="text-5xl mb-3">📑</div>
            )}
            <p className="text-sm font-bold text-emerald-700 truncate w-full px-4">{fileName}</p>
            <p className="text-xs text-slate-500 font-medium mt-1">Click anywhere in this box to change file</p>
          </div>
        )}
      </div>

      <button 
        type="submit" 
        disabled={isUploading}
        className={`w-full text-white font-extrabold py-4 rounded-xl transition shadow-md mt-4 text-lg flex items-center justify-center gap-2 ${isUploading ? 'bg-slate-400 cursor-not-allowed' : 'bg-slate-900 hover:bg-slate-800'}`}
      >
        <span>{isUploading ? '⏳' : '📎'}</span> 
        {isUploading ? 'Uploading & Securing...' : 'Upload & Secure in Vault'}
      </button>
    </form>
  )
}