import os

with open('scholarmap-frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_ts = f.read()

sidebar_jsx = """
          {/* --- Desktop Sidebar --- */}
          <aside className="hidden md:flex w-72 bg-[#090E1A]/95 border-r border-slate-800/80 flex-col justify-between p-4 z-30 shrink-0 sticky top-0 h-screen">
            <div>
              {/* Brand Logo with Futuristic Compass & Academy */}
              <div className="flex items-center gap-3.5 px-3 py-3 mb-6 cursor-pointer" onClick={() => setActiveSection('database')}>
                <div className="relative w-11 h-11 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 p-[1.5px] shadow-lg shadow-cyan-500/20">
                  <div className="w-full h-full bg-[#0E1629] rounded-[14px] flex items-center justify-center relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-cyan-400/10"></div>
                    <i className="fa-solid fa-graduation-cap text-cyan-400 text-lg z-10 drop-shadow-[0_0_8px_rgba(34,211,238,0.5)]"></i>
                  </div>
                </div>
                <div>
                  <h1 className="text-xl font-black text-white tracking-tight leading-tight flex items-center">
                    Scholar<span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">Map</span>
                  </h1>
                  <p className="text-[9px] font-bold text-slate-400 tracking-[0.2em] uppercase">AI Navigator</p>
                </div>
              </div>

              {/* Navigation Menu */}
              <nav className="space-y-1.5 mt-2">
                <button 
                  onClick={() => setActiveSection('database')} 
                  className={`nav-item w-full flex items-center gap-3.5 px-4 py-3.5 rounded-2xl font-semibold text-[13px] transition-all group ${activeSection === 'database' ? 'bg-blue-600/15 text-cyan-300 border border-cyan-500/30 shadow-lg shadow-cyan-900/20' : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'}`}
                >
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center transition-all ${activeSection === 'database' ? 'bg-cyan-500/20 text-cyan-400 shadow-inner' : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'}`}>
                    <i className="fa-solid fa-layer-group"></i>
                  </div>
                  Grantlar Bazasi
                </button>
                <button 
                  onClick={() => setActiveSection('search')} 
                  className={`nav-item w-full flex items-center gap-3.5 px-4 py-3.5 rounded-2xl font-semibold text-[13px] transition-all group ${activeSection === 'search' ? 'bg-blue-600/15 text-cyan-300 border border-cyan-500/30 shadow-lg shadow-cyan-900/20' : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'}`}
                >
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center transition-all ${activeSection === 'search' ? 'bg-cyan-500/20 text-cyan-400 shadow-inner' : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'}`}>
                    <i className="fa-solid fa-compass"></i>
                  </div>
                  Mos Grantlar Qidirish
                </button>
                <button 
                  onClick={() => setActiveSection('eligibility')} 
                  className={`nav-item w-full flex items-center gap-3.5 px-4 py-3.5 rounded-2xl font-semibold text-[13px] transition-all group ${activeSection === 'eligibility' ? 'bg-blue-600/15 text-cyan-300 border border-cyan-500/30 shadow-lg shadow-cyan-900/20' : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'}`}
                >
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center transition-all ${activeSection === 'eligibility' ? 'bg-cyan-500/20 text-cyan-400 shadow-inner' : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'}`}>
                    <i className="fa-solid fa-chart-simple"></i>
                  </div>
                  Imkoniyatni Baholash
                </button>
                
                <div className="pt-6 pb-2 px-4">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Premium Xizmatlar</p>
                </div>

                <button 
                  onClick={() => setActiveSection('translation')} 
                  className={`nav-item w-full flex items-center gap-3.5 px-4 py-3.5 rounded-2xl font-semibold text-[13px] transition-all group ${activeSection === 'translation' ? 'bg-blue-600/15 text-cyan-300 border border-cyan-500/30 shadow-lg shadow-cyan-900/20' : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'}`}
                >
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center transition-all relative ${activeSection === 'translation' ? 'bg-emerald-500/20 text-emerald-400 shadow-inner' : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'}`}>
                    <i className="fa-solid fa-language"></i>
                    <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-500 rounded-full border-2 border-[#090E1A]"></span>
                  </div>
                  AI Hujjat Tarjimasi
                </button>
                <button 
                  onClick={() => setActiveSection('funding')} 
                  className={`nav-item w-full flex items-center gap-3.5 px-4 py-3.5 rounded-2xl font-semibold text-[13px] transition-all group ${activeSection === 'funding' ? 'bg-blue-600/15 text-cyan-300 border border-cyan-500/30 shadow-lg shadow-cyan-900/20' : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'}`}
                >
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center transition-all ${activeSection === 'funding' ? 'bg-purple-500/20 text-purple-400 shadow-inner' : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'}`}>
                    <i className="fa-solid fa-sack-dollar"></i>
                  </div>
                  Moliyalashtirish
                </button>
                <button 
                  onClick={() => setActiveSection('profile')} 
                  className={`nav-item w-full flex items-center gap-3.5 px-4 py-3.5 rounded-2xl font-semibold text-[13px] transition-all group ${activeSection === 'profile' ? 'bg-blue-600/15 text-cyan-300 border border-cyan-500/30 shadow-lg shadow-cyan-900/20' : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'}`}
                >
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center transition-all ${activeSection === 'profile' ? 'bg-cyan-500/20 text-cyan-400 shadow-inner' : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'}`}>
                    <i className="fa-regular fa-user"></i>
                  </div>
                  Shaxsiy Kabinet
                </button>
              </nav>
            </div>

            {/* Bottom: Pro Upgrade & User Mini Profile */}
            <div className="space-y-4">
              {!userProfile?.is_premium && (
                <div className="relative p-4 rounded-2xl bg-gradient-to-tr from-cyan-900/40 to-blue-900/20 border border-cyan-500/30 overflow-hidden group">
                  <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/20 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2 group-hover:bg-cyan-400/30 transition"></div>
                  <div className="relative z-10">
                    <div className="flex items-center gap-2 mb-2">
                      <i className="fa-solid fa-bolt text-amber-400 text-lg"></i>
                      <h4 className="text-sm font-black text-white">Premium Obuna</h4>
                    </div>
                    <p className="text-[10px] text-slate-300 mb-3 leading-relaxed">Barcha VIP imkoniyatlarni oching va cheksiz AI xizmatlaridan foydalaning.</p>
                    <button onClick={() => setActiveSection('premium')} className="w-full py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold text-xs shadow-lg shadow-cyan-500/30 transition">
                      Yangilash
                    </button>
                  </div>
                </div>
              )}
              
              <div className="p-3 rounded-2xl bg-slate-800/40 border border-slate-700/50 flex items-center justify-between cursor-pointer hover:bg-slate-800 transition">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-slate-700 border border-slate-600 overflow-hidden relative shadow-inner">
                    {userProfile?.photo ? (
                      <img src={userProfile.photo} className="w-full h-full object-cover" alt="Profile" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-slate-400">
                        <i className="fa-solid fa-user"></i>
                      </div>
                    )}
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-white">{userProfile?.first_name || 'Foydalanuvchi'}</h4>
                    <p className="text-[10px] font-medium text-cyan-400">ID: #{userProfile?.id || '0000'}</p>
                  </div>
                </div>
                <button onClick={handleLogout} className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition">
                  <i className="fa-solid fa-right-from-bracket text-sm"></i>
                </button>
              </div>
            </div>
          </aside>
"""

header_jsx = """
          <header className="sticky top-0 z-20 bg-[#0E1629]/80 backdrop-blur-xl border-b border-slate-800/80 p-4 md:p-6 flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-black text-white tracking-tight" id="current-page-title">
                {activeSection === 'database' ? 'Grantlar Bazasi' :
                 activeSection === 'search' ? 'Mos Grantlar Qidirish' :
                 activeSection === 'eligibility' ? 'Grant Imkoniyatlarini Baholash' :
                 activeSection === 'translation' ? 'Hujjatlarni Tarjima Qilish' :
                 activeSection === 'funding' ? 'Moliyalashtirish' :
                 activeSection === 'profile' ? 'Shaxsiy Kabinet' : 'ScholarMap'}
              </h2>
              <p className="text-xs text-slate-400 mt-1 hidden md:block">Barcha xalqaro ta'lim imkoniyatlari bitta platformada</p>
            </div>
            <div className="flex items-center gap-3 md:gap-5">
              <div className="relative group hidden sm:block">
                <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-slate-400 cursor-pointer border border-slate-700 group-hover:border-cyan-500 transition">
                  <i className="fa-regular fa-bell"></i>
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-rose-500 rounded-full border-2 border-[#0E1629]"></span>
                </div>
              </div>
              <div className="hidden sm:block w-px h-8 bg-slate-800"></div>
              <button onClick={() => window.open('https://t.me/scholarmap', '_blank')} className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition flex items-center gap-2 border border-slate-700">
                <i className="fa-solid fa-headset text-cyan-400"></i>
                <span className="hidden sm:inline">Qo'llab-quvvatlash</span>
              </button>
            </div>
          </header>
"""

# Now replace the <aside ...> up to </aside> in App.tsx
start_tag_aside = "{/* --- Desktop Sidebar --- */}"
end_tag_aside = "</aside>"

start_idx = app_ts.find(start_tag_aside)
end_idx = app_ts.find(end_tag_aside, start_idx) + len(end_tag_aside)

if start_idx != -1 and end_idx != -1:
    app_ts = app_ts[:start_idx] + sidebar_jsx + app_ts[end_idx:]

# Now replace the <header ...> up to </header>
start_tag_header = "<header"
end_tag_header = "</header>"

# The header is after the aside
header_start = app_ts.find(start_tag_header, start_idx)
header_end = app_ts.find(end_tag_header, header_start) + len(end_tag_header)

if header_start != -1 and header_end != -1:
    app_ts = app_ts[:header_start] + header_jsx + app_ts[header_end:]

# Set global app background to the new dark theme
app_ts = app_ts.replace("bg-slate-900 transition-colors duration-500", "bg-[#0E1629] transition-colors duration-500 font-sans")
app_ts = app_ts.replace("style={{ background: isDarkMode ? '#0f172a' : '#f8fafc' }}", "style={{ background: '#0E1629' }}")

with open('scholarmap-frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app_ts)

print("Injected Sidebar, Header, and Global Layout!")
