import re
import os

with open('scholarmap-frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_ts = f.read()

translation_jsx = """
          <motion.div
            key="translation"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="page-content space-y-6"
          >
            <div className="p-8 rounded-[2.5rem] border bg-slate-900 border-slate-800 shadow-2xl relative overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
              <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white shadow-lg">
                      <i className="fa-solid fa-language"></i>
                    </div>
                    <h3 className="text-xl font-black text-white tracking-tight">AI Hujjat Tarjimoni</h3>
                  </div>
                  <p className="text-sm text-slate-400">PDF, DOCX yoki rasmlarni yuklang, sun'iy intellekt xalqaro standartlarda tarjima qiladi.</p>
                </div>
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  Online
                </div>
              </div>
              
              <div className="mt-8 space-y-6 relative z-10">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Qaysi tildan</label>
                    <select value={sourceLang} onChange={e => setSourceLang(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 transition">
                      <option>O'zbek tili</option>
                      <option>Rus tili</option>
                      <option>Ingliz tili</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Qaysi tilga</label>
                    <select value={targetLang} onChange={e => setTargetLang(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 transition">
                      <option>Ingliz tili</option>
                      <option>Nemis tili</option>
                      <option>Koreys tili</option>
                      <option>Rus tili</option>
                    </select>
                  </div>
                </div>
                
                <div className="border-2 border-dashed border-cyan-500/40 bg-cyan-950/10 rounded-3xl p-8 flex flex-col items-center justify-center text-center space-y-3 hover:border-cyan-400 transition relative cursor-pointer">
                  <input type="file" onChange={handleFileChange} accept=".pdf,.doc,.docx,.jpg,.png" className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                  <div className="w-14 h-14 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-2xl">
                    <i className="fa-solid fa-cloud-arrow-up"></i>
                  </div>
                  <div>
                    <h4 className="text-base font-bold text-white">{selectedFile ? selectedFile.name : "Faylni yuklang"}</h4>
                    <p className="text-xs text-slate-400 font-mono mt-0.5">PDF, DOCX yoki JPG (Max 10MB)</p>
                  </div>
                </div>
                
                {translationResult && (
                  <div className="mt-6 p-6 rounded-2xl bg-emerald-900/20 border border-emerald-500/30 text-white">
                    <h4 className="font-bold text-emerald-400 mb-2">Tarjima muvaffaqiyatli yakunlandi!</h4>
                    <p className="text-sm text-slate-300 max-h-40 overflow-y-auto whitespace-pre-wrap">{translationResult}</p>
                    <button onClick={downloadPDF} className="mt-4 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-bold flex items-center gap-2 transition">
                      Yuklab olish
                    </button>
                  </div>
                )}
                
                <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
                  <div className="flex items-center gap-3 w-full sm:w-auto">
                    <div className="w-10 h-10 rounded-xl bg-slate-800 text-slate-300 flex items-center justify-center">
                      <i className="fa-solid fa-globe"></i>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-white">Notarial tasdiqlash</p>
                      <p className="text-[11px] text-slate-400">Rasmiy hujjatlar uchun muhr va apostil</p>
                    </div>
                  </div>
                  <button onClick={translateFile} disabled={isTranslating} className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-cyan-500/25 transition flex items-center justify-center gap-2">
                    {isTranslating ? <div className="w-4 h-4 rounded-full border-2 border-white border-t-transparent animate-spin"></div> : <i className="fa-solid fa-paper-plane"></i>}
                    <span>{isTranslating ? 'Tarjima qilinmoqda...' : 'Tarjimaga yuborish'}</span>
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
"""

# Replace the translation case content
start_tag = "case 'translation':"
end_tag = "case 'funding':"
start_idx = app_ts.find(start_tag)
end_idx = app_ts.find(end_tag, start_idx)

if start_idx != -1 and end_idx != -1:
    app_ts = app_ts[:start_idx] + "case 'translation':\n        return (\n" + translation_jsx + "        );\n\n      " + app_ts[end_idx:]
    with open('scholarmap-frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_ts)
    print("Injected translation case!")
else:
    print("Could not find translation tags")
