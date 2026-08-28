import { redirect } from 'next/navigation'
import { createClient } from '../../lib/supabase/server'

export default function LoginPage() {
  // This is a Next.js Server Action that securely handles the login request
  const signIn = async (formData: FormData) => {
    'use server'
    const email = formData.get('email') as string
    const password = formData.get('password') as string
    const supabase = await createClient()

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (error) {
      // If login fails, it safely reloads the login page
      return redirect('/login?error=true')
    }
    
    // If successful, it sends you to the secure dashboard
    return redirect('/')
  }

  return (
    <main className="min-h-screen bg-slate-100 flex items-center justify-center p-6">
      <div className="bg-white p-8 rounded-2xl shadow-md border border-slate-200 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-slate-800">ArchLedger Gateway</h1>
          <p className="text-sm text-slate-500 mt-2">Authorized personnel only</p>
        </div>
        
        <form action={signIn} className="flex flex-col gap-5">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Email Address</label>
            <input 
              type="email" 
              name="email" 
              required 
              className="w-full p-2.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-800"
              placeholder="chief@haweaheritage.com"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Password</label>
            <input 
              type="password" 
              name="password" 
              required 
              className="w-full p-2.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-800"
              placeholder="••••••••"
            />
          </div>
          <button 
            type="submit" 
            className="w-full bg-slate-900 text-white font-bold py-3 rounded-lg hover:bg-slate-700 transition shadow-sm mt-2"
          >
            Access Vault
          </button>
        </form>
      </div>
    </main>
  )
}