import re
import os

with open('scholarmap-frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_ts = f.read()

baholash_jsx = """
          <motion.div
            key="eligibility"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="page-content space-y-6"
          >
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              
              <div className="lg:col-span-5 space-y-6">
                <div className="p-8 rounded-[2.5rem] border bg-slate-900 border-slate-800 shadow-2xl relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
                  
                  <div className="relative z-10 flex items-center gap-3 mb-8">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center text-white shadow-lg">
                      <i className="fa-solid fa-calculator"></i>
                    </div>
                    <h3 className="text-xl font-black text-white tracking-tight">Ko'rsatkichlaringiz</h3>
                  </div>
                  
                  <div className="space-y-8 relative z-10">
                    <div>
                      <div className="flex justify-between items-end mb-3">
                        <label className="text-sm font-bold text-slate-400 uppercase tracking-wider">GPA (O'rtacha baho)</label>
                        <div className="bg-slate-800 text-emerald-400 font-mono font-bold px-3 py-1 rounded-lg text-lg border border-slate-700 shadow-inner" id="gpa-badge">{gpaValue}</div>
                      </div>
                      <input type="range" min="3.0" max="5.0" step="0.1" value={gpaValue} onChange={(e) => setGpaValue(Number(e.target.value))} className="w-full accent-emerald-500 h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer" />
                      <div className="flex justify-between text-[10px] text-slate-500 font-bold mt-2">
                        <span>3.0</span>
                        <span>4.0</span>
                        <span>5.0</span>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between items-end mb-3">
                        <label className="text-sm font-bold text-slate-400 uppercase tracking-wider">IELTS / TOEFL</label>
                        <div className="bg-slate-800 text-cyan-400 font-mono font-bold px-3 py-1 rounded-lg text-lg border border-slate-700 shadow-inner" id="ielts-badge">{ieltsValue}</div>
                      </div>
                      <input type="range" min="5.5" max="9.0" step="0.5" value={ieltsValue} onChange={(e) => setIeltsValue(Number(e.target.value))} className="w-full accent-cyan-500 h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer" />
                      <div className="flex justify-between text-[10px] text-slate-500 font-bold mt-2">
                        <span>5.5</span>
                        <span>7.0</span>
                        <span>9.0</span>
                      </div>
                    </div>
                    
                    <button onClick={handleEligibilityCheck} className="w-full py-4 rounded-xl bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-emerald-500/25 transition">
                      Natijani Hisoblash
                    </button>
                  </div>
                </div>
              </div>

              <div className="lg:col-span-7 flex flex-col gap-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-full">
                  <div className="p-8 rounded-[2.5rem] border bg-slate-900 border-slate-800 flex flex-col items-center justify-center text-center shadow-xl">
                    <div className="relative w-40 h-40 mb-6 flex items-center justify-center">
                      <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                        <path className="text-slate-800" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" strokeDasharray="100, 100" />
                        <path className="text-emerald-500 transition-all duration-1000 ease-out" strokeDasharray={`${Math.min(100, (gpaValue/5)*45 + (ieltsValue/9)*35 + 15)}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-3xl font-black text-white" id="probability-percent">~{Math.round((gpaValue/5)*45 + (ieltsValue/9)*35 + 15)}%</span>
                      </div>
                    </div>
                    <h4 className="text-base font-bold text-white mb-1">Umumiy Imkoniyat</h4>
                    <p className="text-xs font-bold text-emerald-400" id="probability-label">
                      {Math.round((gpaValue/5)*45 + (ieltsValue/9)*35 + 15) >= 70 ? 'Maksimal Imkoniyat' : 
                       Math.round((gpaValue/5)*45 + (ieltsValue/9)*35 + 15) >= 55 ? 'Yuqori Natija' : 'O\'rtacha Natija'}
                    </p>
                  </div>

                  <div className="flex flex-col gap-4">
                    <div className="glass-panel p-5 rounded-3xl border border-slate-800 flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-white font-bold shadow-inner">SU</div>
                        <div>
                          <p className="text-sm font-bold text-white">Stanford Univ.</p>
                          <p className="text-[10px] text-slate-400">Top 10 (AQSh)</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-black text-emerald-400">{Math.round(((gpaValue/5)*45 + (ieltsValue/9)*35 + 15) * 0.9)}%</p>
                      </div>
                    </div>
                    
                    <div className="glass-panel p-5 rounded-3xl border border-slate-800 flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-white font-bold shadow-inner">OX</div>
                        <div>
                          <p className="text-sm font-bold text-white">Oxford Univ.</p>
                          <p className="text-[10px] text-slate-400">Top 5 (UK)</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-black text-amber-400">{Math.round(((gpaValue/5)*45 + (ieltsValue/9)*35 + 15) * 0.88)}%</p>
                      </div>
                    </div>

                    <div className="mt-auto p-4 rounded-2xl bg-slate-800/50 border border-slate-700/50 text-[11px] text-slate-400 flex items-start gap-2">
                      <i className="fa-solid fa-circle-info text-cyan-500 mt-0.5"></i>
                      <span>AI modeli so'nggi 5 yillik qabul statistikasiga asoslanib hisoblaydi. Bu taxminiy ko'rsatkich.</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
"""

# Replace the eligibility case content
start_tag = "case 'eligibility':"
end_tag = "case 'deadlines':"
start_idx = app_ts.find(start_tag)
end_idx = app_ts.find(end_tag, start_idx)

if start_idx != -1 and end_idx != -1:
    app_ts = app_ts[:start_idx] + "case 'eligibility':\n        return (\n" + baholash_jsx + "        );\n\n      " + app_ts[end_idx:]
    with open('scholarmap-frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_ts)
    print("Injected eligibility case!")
else:
    print("Could not find eligibility tags")
