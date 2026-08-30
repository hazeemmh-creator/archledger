import { createClient } from '../../../../../lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default async function RecordExpensePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()

  const isGlobal = id === 'global'

  // If accessed globally, fetch all projects for the dropdown
  let projects: { id: string; project_name: string }[] = []
  if (isGlobal) {
    const { data } = await supabase.from('projects').select('id, project_name').order('created_at', { ascending: false })
    projects = data || []
  } else {
    // Fetch specific project name for the header context
    const { data } = await supabase.from('projects').select('project_name').eq('id', id).single()
    if (data) projects = [{ id, project_name: data.project_name }]
  }

  const logExpense = async (formData: FormData) => {
    'use server'
    const supabase = await createClient()

    const targetProjectId = isGlobal ? (formData.get('project_id') as string) : id
    const description = formData.get('description') as string
    const amount = parseFloat(formData.get('amount') as string)
    const category = formData.get('category') as string

    const { error } = await supabase.from('expenses').insert({
      project_id: targetProjectId,
      description: description,
      amount: amount,
      category: category
    })

    if (!error) {
      redirect(`/projects/${targetProjectId}`)
    } else {
      console.error("Vault Error (Expense):", error.message)
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 p-8 flex items-center justify-center">
      <div className="w-full max-w-2xl bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">
              {isGlobal ? 'Global Expense Dispatch' : `Record Expense: ${projects[0]?.project_name || 'Project'}`}
            </h1>
            <p className="text-sm text-slate-500 mt-1">Log materials, labor, or site operational costs</p>
          </div>
          <Link href={isGlobal ? '/' : `/projects/${id}`} className="px-4 py-2 text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition">
            Cancel
          </Link>
        </div>
        
        <form action={logExpense} className="flex flex-col gap-6">
          
          {/* If global, show the destination picker */}
          {isGlobal && (
            <div className="bg-slate-50 p-5 rounded-2xl border border-slate-200">
              <label className="block text-sm font-bold text-slate-700 mb-2">Select Destination Project</label>
              <select 
                name="project_id" 
                required 
                className="w-full p-3.5 border border-slate-300 rounded-xl text-slate-900 font-bold bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm"
              >
                <option value="">-- Route to Project --</option>
                {projects.map((p) => (
                  <option key={p.id} value={p.id}>{p.project_name}</option>
                ))}
              </select>
            </div>
          )}

          <div>
            <label className="block text-sm font-bold text-slate-700 mb-1.5">Expense Description</label>
            <input 
              type="text" 
              name="description" 
              required 
              className="w-full p-3.5 border border-slate-300 rounded-xl text-slate-900 font-medium bg-white focus:outline-none focus:ring-2 focus:ring-amber-500" 
              placeholder="e.g., 50 bags of Dangote Cement" 
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1.5">Amount (₦)</label>
              <input 
                type="number" 
                name="amount" 
                required 
                min="0"
                step="0.01"
                className="w-full p-3.5 border border-slate-300 rounded-xl text-slate-900 font-medium bg-white focus:outline-none focus:ring-2 focus:ring-amber-500" 
                placeholder="e.g., 250000" 
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1.5">Category</label>
              <select 
                name="category" 
                required 
                className="w-full p-3.5 border border-slate-300 rounded-xl text-slate-900 font-medium bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              >
                <option value="Materials">Materials & Supplies</option>
                <option value="Labor">Labor & Wages</option>
                <option value="Logistics">Logistics & Transport</option>
                <option value="Security">Security</option>
                <option value="Administrative">Administrative</option>
                <option value="Taxes">Taxes & Levies</option>
              </select>
            </div>
          </div>

          <button 
            type="submit" 
            className="w-full bg-slate-900 text-white font-extrabold py-4 rounded-xl hover:bg-slate-800 transition shadow-md mt-4 text-lg flex items-center justify-center gap-2"
          >
            <span>💸</span> Log Expense to Vault
          </button>
        </form>
      </div>
    </main>
  )
}