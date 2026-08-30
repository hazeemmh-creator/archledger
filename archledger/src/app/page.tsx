import { redirect } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { createClient } from '../lib/supabase/server'

const formatNaira = (amount: number) => {
  return new Intl.NumberFormat('en-NG', {
    style: 'currency',
    currency: 'NGN'
  }).format(amount)
}

export default async function DashboardPage() {
  const supabase = await createClient()

  const { data: { user }, error } = await supabase.auth.getUser()
  if (error || !user) redirect('/login')

  const { data: projectsData } = await supabase.from('projects').select('*').order('created_at', { ascending: false })
  const projects = projectsData || []
  const totalProjects = projects.length

  const { data: fundingData } = await supabase.from('funding_transactions').select('*')
  const { data: expensesData } = await supabase.from('expenses').select('*')
  const { data: contributionsData } = await supabase.from('contributions').select('*')
  
  const allFunding = fundingData || []
  const allExpenses = expensesData || []
  const allContributions = contributionsData || []

  const globalFunded = allFunding.reduce((sum, item) => sum + Number(item.amount), 0)
  const globalExpensed = allExpenses.reduce((sum, item) => sum + Number(item.amount), 0)
  const globalContributions = allContributions.reduce((sum, item) => sum + Number(item.amount), 0)
  
  const globalCashPosition = (globalFunded + globalContributions) - globalExpensed

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 pb-12">
      
      <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <div className="flex items-center">
            <Image 
              src="/logo.png" 
              alt="Build-Crafts Innovations" 
              width={300} 
              height={100} 
              className="w-[220px] md:w-[280px] h-auto object-contain"
              priority
            />
          </div>
          <div className="flex items-center gap-6">
            <span className="text-sm font-medium text-slate-400 hover:text-amber-600 cursor-pointer transition">🔔 Notifications</span>
            <div className="h-10 w-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-700 font-bold border border-slate-300 shadow-sm">
              HM
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 mt-10">
        
        <div className="flex flex-col md:flex-row md:justify-between md:items-end mb-8 gap-4">
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900">Good Afternoon, Chief 👋</h1>
            <p className="text-slate-500 mt-1 font-medium">Here is your financial position across all projects.</p>
          </div>
          <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-4 py-2.5 rounded-full shadow-sm">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span className="text-sm font-bold text-emerald-800 tracking-wide">PORTFOLIO HEALTH: HEALTHY</span>
          </div>
        </div>

        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Portfolio Financial Snapshot</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-5 mb-10">
          
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition relative overflow-hidden group">
            <div className="absolute -top-2 -right-2 text-5xl opacity-5 group-hover:opacity-10 transition group-hover:scale-110">💰</div>
            <p className="text-sm font-semibold text-slate-500 mb-1">Funds Received</p>
            <h3 className="text-xl md:text-2xl font-bold text-slate-900 truncate" title={formatNaira(globalFunded)}>{formatNaira(globalFunded)}</h3>
          </div>
          
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition relative overflow-hidden group">
            <div className="absolute -top-2 -right-2 text-5xl opacity-5 group-hover:opacity-10 transition group-hover:scale-110">🤝</div>
            <p className="text-sm font-semibold text-slate-500 mb-1">Partner Contributions</p>
            <h3 className="text-xl md:text-2xl font-bold text-amber-600 truncate" title={formatNaira(globalContributions)}>{formatNaira(globalContributions)}</h3>
          </div>
          
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition relative overflow-hidden group">
            <div className="absolute -top-2 -right-2 text-5xl opacity-5 group-hover:opacity-10 transition group-hover:scale-110">💸</div>
            <p className="text-sm font-semibold text-slate-500 mb-1">Total Expenses</p>
            <h3 className="text-xl md:text-2xl font-bold text-red-600 truncate" title={formatNaira(globalExpensed)}>{formatNaira(globalExpensed)}</h3>
          </div>
          
          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-lg relative overflow-hidden text-white group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-white opacity-5 rounded-full -mr-10 -mt-10 group-hover:scale-110 transition duration-500"></div>
            <p className="text-sm font-medium text-slate-300 mb-1">Cash Position</p>
            <h3 className="text-xl md:text-2xl font-extrabold text-white truncate" title={formatNaira(globalCashPosition)}>{formatNaira(globalCashPosition)}</h3>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          <div className="lg:col-span-2">
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Active Projects</h2>
            
            {totalProjects === 0 ? (
              <div className="bg-white p-12 rounded-2xl border border-dashed border-slate-300 text-center">
                <p className="text-slate-500 font-medium">No active projects. Start by registering a new site.</p>
              </div>
            ) : (
              <div className="flex flex-col gap-4">
                {projects.map((project) => {
                  const projectBudget = project.project_budget || 0
                  const projectExpensed = allExpenses.filter(e => e.project_id === project.id).reduce((sum, item) => sum + Number(item.amount), 0)
                  const budgetRemaining = projectBudget - projectExpensed
                  const progressPercent = projectBudget > 0 ? Math.min((projectExpensed / projectBudget) * 100, 100) : 0

                  return (
                    <Link href={`/projects/${project.id}`} key={project.id} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:border-slate-400 hover:shadow-md transition group block">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-xl font-bold text-slate-900 group-hover:text-amber-600 transition">{project.project_name}</h3>
                        <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                          🟢 {(project.status || 'DRAFT').toUpperCase()}
                        </span>
                      </div>
                      <p className="text-sm text-slate-500 mb-5 font-medium">{project.project_location} • {project.project_category}</p>
                      
                      <div className="w-full bg-slate-100 rounded-full h-2 mb-4 overflow-hidden">
                        <div className="bg-amber-500 h-2 rounded-full transition-all duration-1000" style={{ width: `${progressPercent}%` }}></div>
                      </div>

                      <div className="grid grid-cols-3 gap-4 border-t border-slate-100 pt-4">
                         <div>
                           <p className="text-xs text-slate-400 font-bold uppercase">Budget</p>
                           <p className="text-sm font-extrabold text-slate-700 truncate" title={formatNaira(projectBudget)}>{formatNaira(projectBudget)}</p>
                         </div>
                         <div>
                           <p className="text-xs text-slate-400 font-bold uppercase">Spent</p>
                           <p className="text-sm font-extrabold text-slate-700 truncate" title={formatNaira(projectExpensed)}>{formatNaira(projectExpensed)}</p>
                         </div>
                         <div>
                           <p className="text-xs text-slate-400 font-bold uppercase">Remaining</p>
                           <p className="text-sm font-extrabold text-slate-700 truncate" title={formatNaira(budgetRemaining)}>{formatNaira(budgetRemaining)}</p>
                         </div>
                      </div>
                    </Link>
                  )
                })}
              </div>
            )}
          </div>

          <div className="flex flex-col gap-6">
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
               <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Quick Actions</h2>
               <Link href="/projects/create" className="w-full flex items-center justify-center gap-2 bg-amber-500 text-slate-900 font-extrabold py-3.5 rounded-xl hover:bg-amber-600 transition shadow-md mb-4">
                 ➕ New Project
               </Link>
               {/* Fixed Routes */}
               <div className="grid grid-cols-2 gap-3">
                 <Link href="/partners" className="bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-sm font-bold py-3 text-center rounded-xl transition shadow-sm block">
                   🤝 Partner CRM
                 </Link>
                 <Link href="/projects/global/funding/create" className="bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-sm font-bold py-3 text-center rounded-xl transition shadow-sm block">
                   💰 Funding
                 </Link>
                 <Link href="/projects/global/expenses/create" className="bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-sm font-bold py-3 text-center rounded-xl transition shadow-sm block">
                   💸 Expense
                 </Link>
                 <Link href="/documents" className="bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-sm font-bold py-3 text-center rounded-xl transition shadow-sm block">
                   📎 Document
                 </Link>
               </div>
            </div>

            <div className="bg-emerald-50 p-6 rounded-2xl border border-emerald-200 shadow-sm">
               <h2 className="text-xs font-bold text-emerald-800 uppercase tracking-wider mb-4 flex items-center gap-2">
                 🟢 System Status
               </h2>
               <div className="space-y-3">
                 <div className="bg-white p-4 rounded-xl border border-emerald-200 shadow-sm text-sm flex items-start gap-3">
                    <span className="mt-0.5">✓</span>
                    <p className="text-slate-700 font-medium">Global Command Center modules active. Ready for multi-project dispatch.</p>
                 </div>
               </div>
            </div>
            
          </div>
        </div>
      </div>
    </main>
  )
}