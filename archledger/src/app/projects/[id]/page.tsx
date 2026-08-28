import { createClient } from '../../../lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default async function ProjectLedgerPage({ params }: { params: Promise<{ id: string }> }) {
  // Await the dynamic URL parameters (Next.js 15+ standard)
  const { id } = await params
  const supabase = await createClient()
  
  // Fetch only the specific project clicked
  const { data: project, error } = await supabase
    .from('projects')
    .select('*')
    .eq('id', id)
    .single()

  // If someone types a fake ID, bounce them back to the dashboard
  if (error || !project) {
    redirect('/')
  }

  return (
    <main className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        
        {/* Ledger Header */}
        <div className="flex justify-between items-end mb-8 border-b border-slate-200 pb-6">
          <div>
            <Link href="/" className="text-sm font-semibold text-slate-500 hover:text-slate-800 mb-3 inline-block transition">
              ← Back to Command Center
            </Link>
            <h1 className="text-3xl font-bold text-slate-900">{project.project_name}</h1>
            <p className="text-sm text-slate-500 mt-1">{project.project_location} • {project.project_category}</p>
          </div>
          <span className="text-sm font-bold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-200">
            {project.status}
          </span>
        </div>
        
        {/* Temporary Placeholder for Phase 4 Analytics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
           <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm flex flex-col items-center justify-center min-h-[200px]">
             <span className="text-slate-400 font-semibold mb-2">Money Out</span>
             <span className="text-sm text-slate-500">Expense Logging UI (Coming Next)</span>
           </div>
           <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm flex flex-col items-center justify-center min-h-[200px]">
             <span className="text-slate-400 font-semibold mb-2">Money In</span>
             <span className="text-sm text-slate-500">Funding Intake UI (Coming Next)</span>
           </div>
        </div>

      </div>
    </main>
  )
}