import { redirect } from 'next/navigation'
import Link from 'next/link'
import { createClient } from '../lib/supabase/server'

export default async function DashboardPage() {
  const supabase = await createClient()

  // 1. Verify User Session
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    redirect('/login')
  }

  // 2. Fetch live projects directly from the vault
  const { data: projects } = await supabase
    .from('projects')
    .select('*')
    .order('created_at', { ascending: false })

  const totalProjects = projects?.length || 0

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 p-8">
      {/* Navigation Header */}
      <header className="max-w-7xl mx-auto flex justify-between items-center mb-10 pb-6 border-b border-slate-200">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">ArchLedger</h1>
          <p className="text-sm text-slate-500 mt-1">Hawea Heritage Financial Control Engine</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">Logged In As</p>
            <p className="text-sm font-semibold text-slate-700">{user.email}</p>
          </div>
          <form action={async () => {
            'use server'
            const sb = await createClient()
            await sb.auth.signOut()
            redirect('/login')
          }}>
            <button 
              type="submit"
              className="px-4 py-2 text-xs font-semibold text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition border border-red-200"
            >
              Sign Out
            </button>
          </form>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto">
        
        {/* Dashboard Controls */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-slate-800">Active Projects ({totalProjects})</h2>
          <Link href="/projects/create" className="bg-slate-900 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-700 transition shadow-sm">
            + Register New Project
          </Link>
        </div>

        {/* Projects Grid */}
        {totalProjects === 0 ? (
          <div className="bg-white p-12 rounded-2xl border border-dashed border-slate-300 text-center">
            <h3 className="text-lg font-semibold text-slate-800 mb-2">No Projects Registered Yet</h3>
            <p className="text-sm text-slate-500 max-w-md mx-auto mb-6">
              Your vault and tax ledgers are ready. Click the button above to register your first site.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <div key={project.id} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col">
                <div className="flex justify-between items-start mb-4">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    {project.project_category}
                  </span>
                  <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                    {project.status}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-1">{project.project_name}</h3>
                <p className="text-sm text-slate-500 mb-6 flex-grow">{project.project_location}</p>
                <Link 
                  href={`/projects/${project.id}`} 
                  className="w-full block text-center bg-slate-900 text-white font-semibold py-2.5 rounded-lg hover:bg-slate-700 transition text-sm shadow-sm"
                >
                  Open Project Ledger
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  )
}