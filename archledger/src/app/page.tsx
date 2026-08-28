export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6">
      <div className="bg-white p-10 rounded-2xl shadow-sm border border-slate-200 text-center max-w-2xl w-full">
        <h1 className="text-4xl font-bold text-slate-800 mb-4">
          Welcome to ArchLedger
        </h1>
        <p className="text-slate-600 text-lg mb-8">
          The financial control engine for Hawea Heritage is officially online, Chief!
        </p>
        <div className="grid grid-cols-2 gap-4 text-left">
          <div className="p-4 border border-slate-100 rounded-xl bg-slate-50">
            <h3 className="font-semibold text-slate-700">Database Vault</h3>
            <p className="text-sm text-emerald-600 font-medium">● Connected & Live</p>
          </div>
          <div className="p-4 border border-slate-100 rounded-xl bg-slate-50">
            <h3 className="font-semibold text-slate-700">Financial Analytics</h3>
            <p className="text-sm text-emerald-600 font-medium">● Connected & Live</p>
          </div>
        </div>
      </div>
    </main>
  );
}