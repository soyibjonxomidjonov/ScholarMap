import re
import os

with open('scholarmap-frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_ts = f.read()

# I will replace the main render method in App.tsx
# The main return is at the end of the file. Let's find it.

bazasi_jsx = """
          <motion.div
            key="database"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="page-content space-y-6"
          >
            <div className="flex flex-col md:flex-row gap-4 items-stretch justify-between">
              <div className="relative flex-1">
                <i className="fa-solid fa-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                <input 
                  className="w-full bg-slate-900/90 border border-slate-700/80 rounded-2xl pl-11 pr-4 py-3.5 text-sm text-white focus:outline-none focus:border-cyan-500 transition" 
                  placeholder="Grant yoki universitet nomini kiriting..." 
                  type="text"
                  value={uniSearchQuery}
                  onChange={(e) => setUniSearchQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      setIsLoadingUnis(true);
                      const params = new URLSearchParams();
                      if (uniSearchQuery.trim()) params.append('search', uniSearchQuery.trim());
                      if (searchLevel) params.append('level', searchLevel);
                      apiFetch(`/universiteties/?${params.toString()}`)
                        .then(r => r.json())
                        .then(data => {
                          if (data.results) {
                            const mapped = data.results.map((u: any) => ({
                              id: String(u.id), name: u.university_name, country: u.state,
                              grantType: u.grant_name, amount: u.grand_amount,
                              deadline: u.reception_end, openingDate: u.reception_start,
                              link: u.link || '', photo: u.photo || '',
                            }));
                            const sq = uniSearchQuery.trim().toLowerCase();
                            const sfilt = sq ? mapped.filter((u: University) =>
                              u.name?.toLowerCase().includes(sq) ||
                              u.country?.toLowerCase().includes(sq) ||
                              u.grantType?.toLowerCase().includes(sq)
                            ) : mapped;
                            setApiUniversities(sfilt.length > 0 ? sfilt : mapped);
                          }
                        })
                        .catch(() => { })
                        .finally(() => setIsLoadingUnis(false));
                    }
                  }}
                />
              </div>
              <div className="flex items-center gap-3">
                <select 
                  className="bg-slate-900/90 border border-slate-700/80 rounded-2xl px-4 py-3 text-sm text-slate-200 font-medium focus:outline-none focus:border-cyan-500" 
                  value={searchLevel}
                  onChange={(e) => setSearchLevel(e.target.value)}
                >
                  <option value="">Barcha Darajalar</option>
                  <option value="Bakalavr">Bakalavr</option>
                  <option value="Magistratura">Magistratura</option>
                  <option value="Doktorantura">Doktorantura (PhD)</option>
                </select>
                <button className="px-5 py-3 rounded-2xl bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-bold flex items-center gap-2 shadow-lg shadow-cyan-600/30 transition">
                  <i className="fa-solid fa-filter"></i>
                  <span>Filtr</span>
                </button>
              </div>
            </div>

            <div className="space-y-4">
              {activeUniversities.map(uni => (
                <div key={uni.id} className="grant-row glass-panel glass-card-hover rounded-2xl p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border border-slate-800">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center text-white font-black text-xl shadow-lg shrink-0">
                      {uni.name.substring(0,2).toUpperCase()}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="text-base font-bold text-white">{uni.name}</h4>
                        <span className="text-[10px] bg-blue-500/20 text-blue-400 border border-blue-500/30 px-2 py-0.5 rounded-full font-bold">{uni.grantType || 'Bakalavr'}</span>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5 flex items-center gap-2">
                        <span><i className="fa-solid fa-location-dot text-cyan-400 mr-1"></i> {uni.country}</span>
                        <span>•</span>
                        <span>{uni.grantType}</span>
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-6 self-end md:self-auto w-full md:w-auto justify-between md:justify-end">
                    <div className="text-left md:text-right">
                      <p className="text-[10px] uppercase font-bold text-slate-500">Grant Summasi</p>
                      <p className="text-sm font-bold text-emerald-400">{uni.amount}</p>
                    </div>
                    <div className="text-left md:text-right">
                      <p className="text-[10px] uppercase font-bold text-slate-500">Deadline</p>
                      <p className="text-sm font-mono font-bold text-rose-400">{uni.deadline}</p>
                    </div>
                    <a 
                      href={uni.link || '#'} 
                      target="_blank" 
                      rel="noreferrer"
                      className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-cyan-600 text-white text-xs font-bold transition flex items-center gap-1.5 border border-slate-700 hover:border-cyan-500"
                    >
                      <span>Rasmiy sayt</span>
                      <i className="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                  </div>
                </div>
              ))}
              {activeUniversities.length === 0 && (
                <div className="text-center py-10 text-slate-400">
                  Kiritilgan parametrlar bo'yicha grantlar topilmadi.
                </div>
              )}
            </div>
          </motion.div>
"""

# Replace the database case content
db_start = app_ts.find("case 'database':")
db_end = app_ts.find("case 'eligibility':", db_start)
app_ts = app_ts[:db_start] + "case 'database':\n        return (\n" + bazasi_jsx + "        );\n\n      " + app_ts[db_end:]

with open('scholarmap-frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app_ts)

print("Injected database case!")
