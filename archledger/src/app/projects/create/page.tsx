import { redirect } from 'next/navigation'
import Link from 'next/link'
import { createClient } from '../../../lib/supabase/server'

export default async function CreateProjectPage() {
  // The secure server action that catches the form data and saves it to the vault
  const createProject = async (formData: FormData) => {
    'use server'
    const supabase = await createClient()

    const projectName = formData.get('project_name') as string
    const location = formData.get('location') as string
    const category = formData.get('category') as string

    // Insert the data into our 'projects' table
    const { error } = await supabase.from('projects').insert({
      project_name: projectName,
      project_location: location,
      project_category: category,
      status: 'Draft'
    })

    if (!error) {
      // If successful, instantly route the user back to the dashboard
      redirect('/')
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 p-8 flex items-center justify-center">
      <div className="w-full max-w-2xl bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Register New Project</h1>
            <p className="text-sm text-slate-500 mt-1">Open a new site ledger in the system</p>
          </div>
          <Link href="/" className="px-4 py-2 text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition">
            Cancel
          </Link>
        </div>
        
        <form action={createProject} className="flex flex-col gap-6">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Official Project Name</label>
            <input 
              type="text" 
              name="project_name" 
              required 
              className="w-full p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-800" 
              placeholder="e.g., Asokoro Villa Renovation" 
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">Site Location</label>
              <input 
                type="text" 
                name="location" 
                required 
                className="w-full p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-800" 
                placeholder="e.g., Abuja, FCT" 
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">Project Category</label>
              <select 
                name="category" 
                required 
                className="w-full p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-800 bg-white"
              >
                <option value="Residential">Residential Construction</option>
                <option value="Commercial">Commercial Development</option>
                <option value="Infrastructure">Civil Infrastructure</option>
                <option value="Consulting">Consulting / Advisory</option>
              </select>
            </div>
          </div>

          <button 
            type="submit" 
            className="w-full bg-slate-900 text-white font-bold py-3.5 rounded-lg hover:bg-slate-700 transition shadow-sm mt-4"
          >
            Save Project to Vault
          </button>
        </form>
      </div>
    </main>
  )
}