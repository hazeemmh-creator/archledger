import { createClient } from '../../../../../lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default async function RecordContributionPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()

  // 1. Fetch verified partners directly from the CRM Vault
  const { data: partnersData } = await supabase
    .from('partners')
    .select('full_name')
    .order('full_name')
  
  const partners = partnersData || []

  const logContribution = async (formData: FormData) => {
    'use server'
    const supabase = await createClient()

    const description = formData.get('description') as string
    const amount = parseFloat(formData.get('amount') as string)
    const contributorName = formData.get('contributor_name') as string

    // 2. Insert the contribution into the vault
    const { error } = await supabase.from('contributions').insert({
      project_id: id,
      description: description,
      amount: amount,
      contributor_name: contributorName
    })

    if (error) {
      console.error("Vault Error:", error.message)
    } else {
      redirect(`/projects/${id}`)
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 p-8 flex items-center justify-center">
      <div className="w-full max-w-2xl bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">Record Partner Contribution</h1>
            <p className="text-sm text-slate-500 mt-1">Log out-of-pocket expenses or partner equity</p>
          </div>
          <Link href={`/projects/${id}`} className="px-4 py-2 text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition">
            Cancel
          </Link>
        </div>
        
        <form action={logContribution} className="flex flex-col gap-6">
          <div>
            <label className="block text-sm font-bold text-slate-700 mb-1">Contribution Description</label>
            <input 
              type="text" 
              name="description" 
              required 
              className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-medium focus:outline-none focus:ring-2 focus:ring-amber-500" 
              placeholder="e.g., Paid for emergency site clearing" 
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1">Amount (₦)</label>
              <input 
                type="number" 
                name="amount" 
                required 
                min="0"
                step="0.01"
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-medium focus:outline-none focus:ring-2 focus:ring-amber-500" 
                placeholder="e.g., 150000" 
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1">Select Verified Partner</label>
              {partners.length === 0 ? (
                <div className="w-full p-3 border border-red-300 rounded-lg bg-red-50 text-red-700 text-sm font-medium">
                  No partners found. Register them in the CRM first.
                </div>
              ) : (
                <select 
                  name="contributor_name" 
                  required 
                  className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-medium bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                >
                  <option value="">-- Choose Partner --</option>
                  {partners.map((p, i) => (
                    <option key={i} value={p.full_name}>{p.full_name}</option>
                  ))}
                </select>
              )}
            </div>
          </div>
          
          <button type="submit" className="w-full bg-amber-500 text-slate-900 font-extrabold py-3.5 rounded-lg hover:bg-amber-600 transition shadow-sm mt-4">
            Log Contribution to Vault
          </button>
        </form>
      </div>
    </main>
  )
}