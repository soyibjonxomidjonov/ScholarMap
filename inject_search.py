import os

with open('scholarmap-frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_ts = f.read()

search_jsx = """
          <motion.div
            key="search"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="page-content space-y-6"
          >
            <div className="glass-panel rounded-3xl p-6 lg:p-8 space-y-6 border border-cyan-500/20">
              <h3 className="text-xl font-bold text-white flex items-center gap-2.5">
                <i className="fa-solid fa-magnifying-glass-location text-cyan-400"></i>
                <span>Mos Grantlarni Qidirish</span>
              </h3>
              <p className="text-sm text-slate-400">Kriteriyalar bo'yicha kerakli mamlakat, universitet va yo'nalishni belgilang.</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Davlatni tanlang</label>
                  <select value={searchCountry} onChange={e => setSearchCountry(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3.5 text-sm text-white focus:outline-none focus:border-cyan-500 transition">
                    <option value="">Barcha davlatlar (Global)</option>
                    <option value="AQSH">Amerika Qo'shma Shtatlari (AQSh)</option>
                    <option value="Buyuk Britaniya">Buyuk Britaniya (UK)</option>
                    <option value="Germaniya">Germaniya (DAAD)</option>
                    <option value="Janubiy Koreya">Janubiy Koreya (GKS)</option>
                    <option value="Yaponiya">Yaponiya (MEXT)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Universitet</label>
                  <select value={searchUniName} onChange={e => setSearchUniName(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3.5 text-sm text-white focus:outline-none focus:border-cyan-500 transition">
                    <option value="">Istalgan Universitet</option>
                    <option value="Harvard">Harvard University</option>
                    <option value="Stanford">Stanford University</option>
                    <option value="Oxford">University of Oxford</option>
                    <option value="Cambridge">University of Cambridge</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Ta'lim Darajasi</label>
                  <select value={searchLevel} onChange={e => setSearchLevel(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3.5 text-sm text-white focus:outline-none focus:border-cyan-500 transition">
                    <option value="">Barcha darajalar</option>
                    <option value="Bakalavr">Bakalavr</option>
                    <option value="Magistratura">Magistratura</option>
                    <option value="Doktorantura">Doktorantura (PhD)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Yo'nalish (Major)</label>
                  <select value={searchMajor} onChange={e => setSearchMajor(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3.5 text-sm text-white focus:outline-none focus:border-cyan-500 transition">
                    <option value="">Barcha yo'nalishlar</option>
                    <option value="IT">Axborot Texnologiyalari (IT)</option>
                    <option value="Business">Biznes va Menejment</option>
                    <option value="Medicine">Tibbiyot</option>
                    <option value="Engineering">Muhandislik</option>
                  </select>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800">
                <button 
                  onClick={() => {
                    setIsLoadingSearch(true);
                    const params = new URLSearchParams();
                    if (searchCountry) params.append('state', searchCountry);
                    if (searchLevel) params.append('level', searchLevel);
                    if (searchMajor) params.append('major', searchMajor);
                    if (searchUniName) params.append('university_name', searchUniName);
                    
                    apiFetch(`/universiteties/?${params.toString()}&page_size=200`)
                      .then(r => r.json())
                      .then(data => {
                        if (data.results) {
                          setSearchPageResults(data.results);
                        }
                      })
                      .catch(() => {})
                      .finally(() => setIsLoadingSearch(false));
                  }}
                  className="w-full py-4 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-black text-sm shadow-xl shadow-cyan-500/25 transition flex items-center justify-center gap-2"
                >
                  <i className="fa-solid fa-magnifying-glass"></i>
                  <span>Qidirishni Boshlash</span>
                </button>
              </div>
            </div>

            {searchPageResults.length > 0 && (
              <div className="grid grid-cols-1 gap-4">
                <h4 className="text-white font-bold mb-2">Topilgan Natijalar ({searchPageResults.length})</h4>
                {searchPageResults.map(uni => (
                  <div key={uni.id} className="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center text-white font-bold">{uni.university_name?.substring(0,2) || 'UN'}</div>
                      <div>
                        <p className="text-sm font-bold text-white">{uni.university_name}</p>
                        <p className="text-[10px] text-slate-400">{uni.state} • {uni.grant_name}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-black text-emerald-400">{uni.grand_amount}</p>
                      <a href={uni.link || '#'} target="_blank" rel="noreferrer" className="text-[10px] text-cyan-400 hover:underline">Batafsil →</a>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
"""

start_tag = "case 'search':"
end_tag = "case 'eligibility':"
start_idx = app_ts.find(start_tag)
end_idx = app_ts.find(end_tag, start_idx)

if start_idx != -1 and end_idx != -1:
    app_ts = app_ts[:start_idx] + "case 'search':\n        return (\n" + search_jsx + "        );\n\n      " + app_ts[end_idx:]
    with open('scholarmap-frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_ts)
    print("Injected search case!")
else:
    print("Could not find search tags")
