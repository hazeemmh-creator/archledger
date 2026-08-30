import { createClient } from '../../../../../lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default async function RecordFundingPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()

  const isGlobal = id === 'global'

  let projects: { id: string; project_name: string }[] = []
  if (isGlobal) {
    const { data } = await supabase.from('projects').select('id, project_name').order('created_at', { ascending: false })
    projects = data || []
  } else {
    const { data } = await supabase.from('projects').select('project_name').eq('id', id).single()
    if (data) projects = [{ id, project_name: data.project_name }]
  }

  const logFunding = async (formData: FormData) => {
    'use server'
    const supabase = await createClient()

    const targetProjectId = isGlobal ? (formData.get('project_id') as string) : id
    const description = formData.get('description') as string
    const amount = parseFloat(formData.get('amount') as string)
    const fundingType = formData.get('funding_type') as string

    const { error } = await supabase.from('funding_transactions').insert({
      project_id: targetProjectId,
      description: description,
      amount: amount,
      funding_type: fundingType
    })

    if (error) {
      console.error("Vault Insertion Error (Funding):", error.message)
    } else {
      redirect(`/projects/${targetProjectId}`)
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 p-8 flex items-center justify-center">
      <div className="w-full max-w-2xl bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">
              {isGlobal ? 'Global Funding Dispatch' : `Record Project Funding`}
            </h1>
            <p className="text-sm text-slate-500 mt-1">Log incoming capital, client advances, or partner equity</p>
          </div>
          <Link href={isGlobal ? '/' : `/projects/${id}`} className="px-4 py-2 text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition">
            Cancel
          </Link>
        </div>
        
        <form action={logFunding} className="flex flex-col gap-6">
          {isGlobal && (
            <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
              <label className="block text-sm font-bold text-slate-700 mb-2">Select Destination Project</label>
              <select 
                name="project_id" 
                required 
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-bold bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm"
              >
                <option value="">-- Route to Project --</option>
                {projects.map((p) => (
                  <option key={p.id} value={p.id}>{p.project_name}</option>
                ))}
              </select>
            </div>
          )}

          <div>
            <label className="block text-sm font-bold text-slate-700 mb-1">Funding Description / Reference</label>
            <input 
              type="text" 
              name="description" 
              required 
              className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-medium bg-white focus:outline-none focus:ring-2 focus:ring-amber-500" 
              placeholder="e.g., Initial Client Mobilization Advance (50%)" 
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1">Amount Received (₦)</label>
              <input 
                type="number" 
                name="amount" 
                required 
                min="0"
                step="0.01"
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-medium bg-white focus:outline-none focus:ring-2 focus:ring-amber-500" 
                placeholder="e.g., 5000000" 
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1">Funding Source Type</label>
              <select 
                name="funding_type" 
                required 
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-medium bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              >
                <option value="Client Advance">Client Advance / Milestone</option>
                <option value="Director Equity">Chief / Director Equity</option>
                <option value="Partner Contribution">Partner Contribution</option>
                <option value="Loan Facility">Loan / Credit Facility</option>
              </select>
            </div>
          </div>

          <button 
            type="submit" 
            className="w-full bg-amber-500 text-slate-900 font-extrabold py-3.5 rounded-lg hover:bg-amber-600 transition shadow-sm mt-4"
          >
            Inject Capital to Vault
          </button>
        </form>
      </div>
    </main>
  )
}