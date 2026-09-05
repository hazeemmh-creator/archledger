import { createClient } from '../lib/supabase/server'
import { redirect } from 'next/navigation'

export default function LogoutButton() {
  const handleLogout = async () => {
    'use server'
    const supabase = await createClient()
    await supabase.auth.signOut()
    redirect('/login')
  }

  return (
    <form action={handleLogout}>
      <button type="submit" className="text-xs font-bold text-slate-500 hover:text-red-600 transition bg-slate-100 hover:bg-red-50 px-4 py-1.5 rounded-full border border-slate-200 shadow-sm">
        Logout
      </button>
    </form>
  )
}