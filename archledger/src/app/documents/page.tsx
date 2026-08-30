import Link from 'next/link'

export default function DocumentsVaultPage() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 pb-12">
      <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link href="/" className="text-slate-400 hover:text-amber-600 transition font-medium text-sm flex items-center gap-1">
              <span>←</span> Back to Command Center
            </Link>
            <div className="h-4 w-px bg-slate-200"></div>
            <span className="font-bold text-slate-900">Document & Receipt Vault</span>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 mt-16 text-center">
        <div className="bg-white p-12 rounded-3xl border border-slate-200 shadow-sm">
          <div className="text-5xl mb-4">📁</div>
          <h1 className="text-3xl font-extrabold text-slate-900 mb-2">Enterprise Document Vault</h1>
          <p className="text-slate-500 font-medium max-w-lg mx-auto mb-8">
            Phase 3 integration: Upload physical receipt scans, contractor invoices, and compliance certificates directly into project ledgers.
          </p>
          <div className="inline-block bg-amber-50 text-amber-800 font-bold px-5 py-3 rounded-xl border border-amber-200 text-sm">
            🚧 Scheduled for deployment in the next architectural sprint.
          </div>
        </div>
      </div>
    </main>
  )
}