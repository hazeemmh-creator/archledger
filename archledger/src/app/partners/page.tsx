import { createClient } from '../../lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default async function PartnersDirectoryPage() {
  const supabase = await createClient()

  // Verify User Session
  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) redirect('/login')

  // Fetch all registered partners
  const { data: partnersData } = await supabase
    .from('partners')
    .select('*')
    .order('created_at', { ascending: false })
  
  const partners = partnersData || []

  // Server action to register a new partner
  const registerPartner = async (formData: FormData) => {
    'use server'
    const supabase = await createClient()
    const fullName = formData.get('full_name') as string
    const role = formData.get('role') as string

    const { error } = await supabase.from('partners').insert({
      full_name: fullName,
      company_or_role: role
    })

    if (!error) {
      redirect('/partners')
    } else {
      console.error("Vault Error (Partner):", error.message)
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 pb-12">
      {/* Corporate Top Navigation */}
      <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link href="/" className="text-slate-400 hover:text-amber-600 transition font-medium text-sm flex items-center gap-1">
              <span>←</span> Back to Command Center
            </Link>
            <div className="h-4 w-px bg-slate-200"></div>
            <span className="font-bold text-slate-900">Partner Directory</span>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 mt-10 grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: The Directory List */}
        <div className="lg:col-span-2">
          <div className="mb-6 flex justify-between items-end">
            <div>
              <h1 className="text-3xl font-extrabold text-slate-900">Official Partners</h1>
              <p className="text-slate-500 font-medium mt-1">Manage investors and project stakeholders.</p>
            </div>
            <span className="text-xs font-bold text-slate-700 bg-slate-200 px-3 py-1.5 rounded-full border border-slate-300">
              {partners.length} REGISTERED
            </span>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
             {partners.length === 0 ? (
               <div className="p-12 text-center">
                 <p className="text-slate-500 font-medium">No partners registered yet. Add your first investor to the right.</p>
               </div>
             ) : (
               <div className="divide-y divide-slate-100">
                 {partners.map((partner) => (
                   <div key={partner.id} className="p-6 flex justify-between items-center hover:bg-slate-50 transition group">
                     <div className="flex items-center gap-4">
                       <div className="h-12 w-12 rounded-full bg-slate-100 border border-slate-300 flex items-center justify-center text-slate-700 font-bold text-lg">
                         {partner.full_name.charAt(0)}
                       </div>
                       <div>
                         <p className="font-bold text-slate-900 text-lg">{partner.full_name}</p>
                         <p className="text-sm text-slate-500 font-medium">{partner.company_or_role}</p>
                       </div>
                     </div>
                     <button className="text-sm font-bold text-amber-600 opacity-0 group-hover:opacity-100 transition">
                       View Ledger →
                     </button>
                   </div>
                 ))}
               </div>
             )}
          </div>
        </div>

        {/* Right Column: Registration Form */}
        <div>
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm sticky top-24">
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-6">Register New Partner</h2>
            
            <form action={registerPartner} className="flex flex-col gap-5">
              <div>
                <label className="block text-sm font-bold text-slate-700 mb-1">Full Name / Entity</label>
                <input 
                  type="text" 
                  name="full_name" 
                  required 
                  className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-medium bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 transition" 
                  placeholder="e.g., Oga Hamza" 
                />
              </div>
              
              <div>
                <label className="block text-sm font-bold text-slate-700 mb-1">Role / Affiliation</label>
                <input 
                  type="text" 
                  name="role" 
                  required 
                  className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 font-medium bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 transition" 
                  placeholder="e.g., Lead Investor" 
                />
              </div>

              {/* Build-Crafts Amber Action Button */}
              <button 
                type="submit" 
                className="w-full bg-amber-500 text-slate-900 font-extrabold py-3.5 rounded-lg hover:bg-amber-600 transition shadow-sm mt-2"
              >
                Add to Directory
              </button>
            </form>
          </div>
        </div>

      </div>
    </main>
  )
}