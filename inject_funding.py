import re
import os

with open('scholarmap-frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_ts = f.read()

funding_jsx = """
          <motion.div
            key="funding"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="page-content space-y-6"
          >
            <div className="p-6 rounded-3xl bg-gradient-to-r from-purple-900/40 via-indigo-900/30 to-blue-900/20 border border-purple-500/20">
              <span className="text-[10px] font-bold uppercase tracking-wider bg-purple-500/20 text-purple-300 px-2.5 py-0.5 rounded-full border border-purple-500/30">MOLIYALASHTIRISH</span>
              <h3 className="text-xl font-bold text-white mt-2">Moliyalashtirishga Tayyorlash</h3>
              <p className="text-xs text-slate-300 mt-1">EYUF, Yoshlar Ittifoqi va xalqaro tashkilotlar orqali ta'lim xarajatlarini to'liq qoplash yo'riqnomasi.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="glass-panel glass-card-hover p-6 rounded-3xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-xl">
                    <i className="fa-solid fa-wallet"></i>
                  </div>
                  <i className="fa-solid fa-circle-info text-slate-500 cursor-pointer"></i>
                </div>
                <div>
                  <h4 className="text-base font-bold text-white">EYUF ("El-yurt umidi" jamg'armasi)</h4>
                  <ul className="text-xs text-slate-400 mt-2 space-y-1 list-disc list-inside">
                    <li>Arizalar qabuli: May — Iyun</li>
                    <li>Tanlov bosqichlari: 3 ta (Hujjat, Test, Suhbat)</li>
                  </ul>
                </div>
                <button className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs border border-slate-700 transition">
                  Yo'riqnomani ko'rish →
                </button>
              </div>

              <div className="glass-panel glass-card-hover p-6 rounded-3xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-xl">
                    <i className="fa-solid fa-hand-holding-dollar"></i>
                  </div>
                  <i className="fa-solid fa-circle-info text-slate-500 cursor-pointer"></i>
                </div>
                <div>
                  <h4 className="text-base font-bold text-white">Yoshlar Ittifoqi Grantlari</h4>
                  <ul className="text-xs text-slate-400 mt-2 space-y-1 list-disc list-inside">
                    <li>Ijtimoiy faol yoshlar uchun qisman kompensatsiya</li>
                    <li>Xalqaro sertifikat (IELTS) to'lovini qaytarish</li>
                  </ul>
                </div>
                <button className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs border border-slate-700 transition">
                  Yo'riqnomani ko'rish →
                </button>
              </div>
            </div>
          </motion.div>
"""

# Replace the funding case content
start_tag = "case 'funding':"
end_tag = "case 'premium':"
start_idx = app_ts.find(start_tag)
end_idx = app_ts.find(end_tag, start_idx)

if start_idx != -1 and end_idx != -1:
    app_ts = app_ts[:start_idx] + "case 'funding':\n        return (\n" + funding_jsx + "        );\n\n      " + app_ts[end_idx:]
    with open('scholarmap-frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_ts)
    print("Injected funding case!")
else:
    print("Could not find funding tags")
