import { createClient } from '../../../lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'

const formatNaira = (amount: number) => {
  return new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' }).format(amount)
}

export default async function ProjectLedgerPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()
  
  const { data: project, error } = await supabase.from('projects').select('*').eq('id', id).single()
  if (error || !project) redirect('/')

  // Fetch all itemized financial records for this specific project
  const { data: expensesData } = await supabase.from('expenses').select('*').eq('project_id', id).order('created_at', { ascending: false })
  const { data: fundingData } = await supabase.from('funding_transactions').select('*').eq('project_id', id).order('created_at', { ascending: false })
  const { data: contributionsData } = await supabase.from('contributions').select('*').eq('project_id', id).order('created_at', { ascending: false })
  
  const expenses = expensesData || []
  const funding = fundingData || []
  const contributions = contributionsData || []

  const totalExpensed = expenses.reduce((sum, item) => sum + Number(item.amount), 0)
  const totalFunded = funding.reduce((sum, item) => sum + Number(item.amount), 0)
  const totalContributions = contributions.reduce((sum, item) => sum + Number(item.amount), 0)
  
  const availablePosition = (totalFunded + totalContributions) - totalExpensed

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 pb-12">
      <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link href="/" className="text-slate-400 hover:text-amber-600 transition font-medium text-sm flex items-center gap-1">
              <span>←</span> Back to Portfolio
            </Link>
            <div className="h-4 w-px bg-slate-200"></div>
            <span className="font-bold text-slate-900 truncate max-w-[200px] md:max-w-md">{project.project_name}</span>
          </div>
          <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-200">
            🟢 {(project.status || 'DRAFT').toUpperCase()}
          </span>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 mt-8">
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold text-slate-900 mb-1">{project.project_name} Ledger</h1>
          <p className="text-slate-500 font-medium">{project.project_location} • {project.project_category}</p>
        </div>
        
        {/* Financial Snapshot Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8">
           <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm group">
             <p className="text-sm font-semibold text-slate-500 mb-1">Total Funded</p>
             <h3 className="text-2xl font-bold text-slate-900 truncate" title={formatNaira(totalFunded)}>{formatNaira(totalFunded)}</h3>
           </div>
           <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm group">
             <p className="text-sm font-semibold text-slate-500 mb-1">Partner Contributions</p>
             <h3 className="text-2xl font-bold text-amber-600 truncate" title={formatNaira(totalContributions)}>{formatNaira(totalContributions)}</h3>
           </div>
           <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm group">
             <p className="text-sm font-semibold text-slate-500 mb-1">Total Expensed</p>
             <h3 className="text-2xl font-bold text-red-600 truncate" title={formatNaira(totalExpensed)}>{formatNaira(totalExpensed)}</h3>
           </div>
           <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-lg text-white">
             <p className="text-sm font-medium text-slate-300 mb-1">Available Position</p>
             <h3 className="text-2xl font-extrabold text-white truncate" title={formatNaira(availablePosition)}>{formatNaira(availablePosition)}</h3>
           </div>
        </div>

        {/* Ledger Actions */}
        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Ledger Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-10">
           <Link href={`/projects/${project.id}/funding/create`} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-300 transition flex items-center justify-between group">
             <div>
               <span className="text-emerald-700 font-bold block mb-1">Record Money In</span>
               <span className="text-xs text-slate-500 font-medium">Client capital</span>
             </div>
             <div className="h-10 w-10 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 group-hover:scale-110 transition">➕</div>
           </Link>
           <Link href={`/projects/${project.id}/contributions/create`} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:border-amber-300 transition flex items-center justify-between group">
             <div>
               <span className="text-amber-700 font-bold block mb-1">Log Contribution</span>
               <span className="text-xs text-slate-500 font-medium">Partner equity</span>
             </div>
             <div className="h-10 w-10 rounded-full bg-amber-50 flex items-center justify-center text-amber-600 group-hover:scale-110 transition">🤝</div>
           </Link>
           <Link href={`/projects/${project.id}/expenses/create`} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:border-red-300 transition flex items-center justify-between group">
             <div>
               <span className="text-red-700 font-bold block mb-1">Log Money Out</span>
               <span className="text-xs text-slate-500 font-medium">Site expenses</span>
             </div>
             <div className="h-10 w-10 rounded-full bg-red-50 flex items-center justify-center text-red-600 group-hover:scale-110 transition">➖</div>
           </Link>
        </div>

        {/* Itemized Audit Feeds */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* 1. Itemized Expenses (Dangote Cement, Security, Wages) */}
            <div>
              <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Itemized Expenses (Money Out)</h2>
              <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                 {expenses.length === 0 ? (
                   <div className="p-8 text-center text-slate-500 text-sm">No expenses recorded yet.</div>
                 ) : (
                   <div className="divide-y divide-slate-100">
                     {expenses.map((item) => (
                       <div key={item.id} className="p-4 flex justify-between items-center hover:bg-slate-50 transition">
                         <div>
                           <p className="font-bold text-slate-900 text-sm">{item.description}</p>
                           <p className="text-xs text-slate-500 font-medium">{item.category} • {new Date(item.created_at).toLocaleDateString()}</p>
                         </div>
                         <p className="font-extrabold text-red-600 text-sm">-{formatNaira(Number(item.amount))}</p>
                       </div>
                     ))}
                   </div>
                 )}
              </div>
            </div>

            {/* 2. Itemized Client Funding (Money In) */}
            <div>
              <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Client Funding Inflows</h2>
              <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                 {funding.length === 0 ? (
                   <div className="p-8 text-center text-slate-500 text-sm">No funding inflows recorded yet.</div>
                 ) : (
                   <div className="divide-y divide-slate-100">
                     {funding.map((item) => (
                       <div key={item.id} className="p-4 flex justify-between items-center hover:bg-slate-50 transition">
                         <div>
                           <p className="font-bold text-slate-900 text-sm">{item.description}</p>
                           <p className="text-xs text-emerald-700 font-medium">{item.funding_type} • {new Date(item.created_at).toLocaleDateString()}</p>
                         </div>
                         <p className="font-extrabold text-emerald-600 text-sm">+{formatNaira(Number(item.amount))}</p>
                       </div>
                     ))}
                   </div>
                 )}
              </div>
            </div>

            {/* 3. Itemized Partner Contributions (Equity) */}
            <div>
              <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Partner Contributions</h2>
              <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                 {contributions.length === 0 ? (
                   <div className="p-8 text-center text-slate-500 text-sm">No partner contributions recorded yet.</div>
                 ) : (
                   <div className="divide-y divide-slate-100">
                     {contributions.map((item) => (
                       <div key={item.id} className="p-4 flex justify-between items-center hover:bg-slate-50 transition">
                         <div>
                           <p className="font-bold text-slate-900 text-sm">{item.description}</p>
                           <p className="text-xs text-amber-600 font-medium">{item.contributor_name} • {new Date(item.created_at).toLocaleDateString()}</p>
                         </div>
                         <p className="font-extrabold text-amber-600 text-sm">+{formatNaira(Number(item.amount))}</p>
                       </div>
                     ))}
                   </div>
                 )}
              </div>
            </div>

        </div>

      </div>
    </main>
  )
}