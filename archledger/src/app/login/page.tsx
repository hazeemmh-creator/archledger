import Image from 'next/image'
import { createClient } from '../../lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function LoginPage() {
  const supabase = await createClient()
  
  // If the chief is already logged in, skip this page
  const { data: { user } } = await supabase.auth.getUser()
  if (user) redirect('/')

  const signIn = async (formData: FormData) => {
    'use server'
    const email = formData.get('email') as string
    const password = formData.get('password') as string
    const supabase = await createClient()
    
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (!error) redirect('/')
  }

  return (
    <main className="min-h-screen bg-slate-50 flex flex-col justify-center items-center p-6">
      <div className="w-full max-w-md bg-white p-10 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-200">
        
        {/* Massive Centered Logo */}
        <div className="flex justify-center mb-10">
          <Image 
            src="/logo.png" 
            alt="Build-Crafts Innovations" 
            width={400} 
            height={150}
            style={{ width: '260px', height: 'auto' }}
            className="object-contain"
            priority
          />
        </div>
        
        <h1 className="text-2xl font-extrabold text-slate-900 text-center mb-2">Command Center</h1>
        <p className="text-slate-500 text-center mb-8 font-medium">Sign in to access your financial intelligence.</p>
        
        <form action={signIn} className="flex flex-col gap-6">
          <div>
            <label className="block text-sm font-bold text-slate-700 mb-1.5">Email Address</label>
            <input 
              type="email" 
              name="email" 
              required 
              className="w-full p-3.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 font-medium focus:bg-white focus:ring-2 focus:ring-amber-500 focus:outline-none transition" 
              placeholder="chief@buildcrafts.com"
            />
          </div>
          <div>
            <label className="block text-sm font-bold text-slate-700 mb-1.5">Password</label>
            <input 
              type="password" 
              name="password" 
              required 
              className="w-full p-3.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 font-medium focus:bg-white focus:ring-2 focus:ring-amber-500 focus:outline-none transition" 
              placeholder="••••••••"
            />
          </div>
          <button 
            type="submit" 
            className="w-full bg-amber-500 text-slate-900 font-extrabold py-4 rounded-xl hover:bg-amber-600 transition shadow-sm mt-2 text-lg"
          >
            Access System
          </button>
        </form>
        
      </div>
      
      {/* Corporate Footer */}
      <p className="text-slate-400 text-sm font-medium mt-8">
        &copy; {new Date().getFullYear()} Build-Crafts Innovations Ltd. All rights reserved.
      </p>
    </main>
  )
}