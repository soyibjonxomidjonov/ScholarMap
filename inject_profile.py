import re
import os

with open('scholarmap-frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_ts = f.read()

profile_jsx = """
          <motion.div
            key="profile"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="page-content space-y-6"
          >
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
              {/* User Identity Card */}
              <div className="md:col-span-4 space-y-6">
                <div className="p-8 rounded-[2.5rem] border bg-slate-900 border-slate-800 flex flex-col items-center text-center shadow-2xl relative overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-b from-blue-600/10 to-transparent"></div>
                  
                  <div className="relative mb-5 group cursor-pointer" onClick={() => setIsEditingProfile(!isEditingProfile)}>
                    <div className="w-28 h-28 rounded-3xl bg-slate-800 border-4 border-slate-900 shadow-xl overflow-hidden relative">
                      {userProfile?.photo ? (
                        <img src={userProfile.photo} className="w-full h-full object-cover" alt="Profile" />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-4xl text-slate-600 bg-slate-800">
                          <i className="fa-solid fa-user"></i>
                        </div>
                      )}
                      <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center transition">
                        <i className="fa-solid fa-camera text-white text-xl"></i>
                      </div>
                    </div>
                    {userProfile?.is_premium && (
                      <div className="absolute -bottom-2 -right-2 w-8 h-8 rounded-full bg-gradient-to-tr from-amber-400 to-yellow-500 border-2 border-slate-900 flex items-center justify-center text-white shadow-lg shadow-amber-500/40" title="Premium A'zo">
                        <i className="fa-solid fa-crown text-[10px]"></i>
                      </div>
                    )}
                  </div>
                  
                  <div className="relative z-10 w-full">
                    <h3 className="text-xl font-black text-white">{userProfile?.first_name} {userProfile?.last_name}</h3>
                    <p className="text-xs font-bold text-cyan-400 mt-1 uppercase tracking-wider">{userProfile?.is_premium ? "Premium A'zo" : "Oddiy A'zo"}</p>
                    
                    <div className="mt-6 flex flex-col gap-2 w-full text-left">
                      <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 text-xs text-slate-300">
                        <i className="fa-solid fa-envelope text-slate-500"></i>
                        <span className="truncate">{userProfile?.email}</span>
                      </div>
                      <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 text-xs text-slate-300">
                        <i className="fa-solid fa-phone text-slate-500"></i>
                        <span>{userProfile?.phone_number || "+998 90 123 45 67"}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {!userProfile?.is_premium && (
                  <div className="p-6 rounded-3xl bg-gradient-to-tr from-amber-500/20 to-yellow-500/10 border border-amber-500/30 text-center">
                    <div className="w-12 h-12 mx-auto rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center text-xl mb-3 shadow-lg shadow-amber-500/20">
                      <i className="fa-solid fa-crown"></i>
                    </div>
                    <h4 className="font-bold text-white mb-1">Premium Obuna</h4>
                    <p className="text-xs text-slate-400 mb-4">Barcha pullik grantlarga kirish va cheksiz AI xizmatlari</p>
                    <button onClick={() => { setActiveSection('premium'); }} className="w-full py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-900 font-bold text-xs shadow-lg shadow-amber-500/20 transition">
                      Obunani yangilash
                    </button>
                  </div>
                )}
              </div>

              {/* Editable Information */}
              <div className="md:col-span-8 space-y-6">
                <div className="p-8 rounded-[2.5rem] border bg-slate-900 border-slate-800 shadow-2xl relative">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-white">Shaxsiy ma'lumotlar</h3>
                    <button onClick={() => setIsEditingProfile(!isEditingProfile)} className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition flex items-center gap-2 border border-slate-700">
                      <i className="fa-solid fa-pen"></i> {isEditingProfile ? 'Bekor qilish' : 'Tahrirlash'}
                    </button>
                  </div>

                  <form className="space-y-4" onSubmit={handleProfileUpdate}>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Ism</label>
                        <div className="relative">
                          <i className="fa-regular fa-user absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
                          <input type="text" disabled={!isEditingProfile} value={userProfile?.first_name || ''} onChange={e => setUserProfile({...userProfile, first_name: e.target.value} as any)} className="w-full bg-slate-900/90 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 transition disabled:opacity-50 disabled:cursor-not-allowed" />
                        </div>
                      </div>
                      <div>
                        <label className="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Familiya</label>
                        <div className="relative">
                          <i className="fa-regular fa-user absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
                          <input type="text" disabled={!isEditingProfile} value={userProfile?.last_name || ''} onChange={e => setUserProfile({...userProfile, last_name: e.target.value} as any)} className="w-full bg-slate-900/90 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 transition disabled:opacity-50 disabled:cursor-not-allowed" />
                        </div>
                      </div>
                      <div>
                        <label className="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Telefon</label>
                        <div className="relative">
                          <i className="fa-solid fa-phone absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
                          <input type="text" disabled={!isEditingProfile} value={userProfile?.phone_number || ''} onChange={e => setUserProfile({...userProfile, phone_number: e.target.value} as any)} className="w-full bg-slate-900/90 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 transition disabled:opacity-50 disabled:cursor-not-allowed" />
                        </div>
                      </div>
                      <div>
                        <label className="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Davlat</label>
                        <div className="relative">
                          <i className="fa-solid fa-earth-americas absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
                          <select disabled={!isEditingProfile} className="w-full bg-slate-900/90 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 transition disabled:opacity-50 disabled:cursor-not-allowed appearance-none">
                            <option>O'zbekiston</option>
                            <option>Qozog'iston</option>
                          </select>
                        </div>
                      </div>
                    </div>

                    {isEditingProfile && (
                      <div className="flex justify-end pt-4">
                        <button type="submit" disabled={isSavingProfile} className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-cyan-500/30 transition flex items-center gap-2">
                          <i className="fa-solid fa-check"></i>
                          <span>{isSavingProfile ? 'Saqlanmoqda...' : 'Saqlash'}</span>
                        </button>
                      </div>
                    )}
                  </form>
                </div>

                <div className="p-8 rounded-[2.5rem] border bg-slate-900 border-slate-800 shadow-xl">
                  <h3 className="text-lg font-bold text-white mb-6">Xavfsizlik</h3>
                  <form className="space-y-4" onSubmit={handlePasswordChange}>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Eski parol</label>
                        <div className="relative">
                          <i className="fa-solid fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
                          <input type="password" value={passwords.old} onChange={e => setPasswords({...passwords, old: e.target.value})} className="w-full bg-slate-900/90 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 transition" />
                        </div>
                      </div>
                      <div>
                        <label className="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Yangi parol</label>
                        <div className="relative">
                          <i className="fa-solid fa-key absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
                          <input type="password" value={passwords.new} onChange={e => setPasswords({...passwords, new: e.target.value})} className="w-full bg-slate-900/90 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 transition" />
                        </div>
                      </div>
                    </div>
                    {passwordError && <p className="text-xs text-rose-500">{passwordError}</p>}
                    <div className="flex justify-end pt-2">
                      <button type="submit" className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs border border-slate-700 transition">
                        Parolni yangilash
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </motion.div>
"""

start_tag = "case 'profile':"
end_tag = "case 'database':"
start_idx = app_ts.find(start_tag)
end_idx = app_ts.find(end_tag, start_idx)

if start_idx != -1 and end_idx != -1:
    app_ts = app_ts[:start_idx] + "case 'profile':\n        return (\n" + profile_jsx + "        );\n\n      " + app_ts[end_idx:]
    with open('scholarmap-frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_ts)
    print("Injected profile case!")
else:
    print("Could not find profile tags")
