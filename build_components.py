def get_translation_code():
    return """import { motion } from 'motion/react';
import { FileText, Download, CheckCircle, UploadCloud, RefreshCw } from 'lucide-react';
import { cn } from './lib/utils';

export default function Tarjima({
  sourceLang,
  setSourceLang,
  targetLang,
  setTargetLang,
  handleFileChange,
  translateFile,
  isTranslating,
  translationResult,
  downloadPDF
}: any) {
  return (
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
              <select value={sourceLang} onChange={e => setSourceLang(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white">
                <option>O'zbek tili</option>
                <option>Rus tili</option>
                <option>Ingliz tili</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Qaysi tilga</label>
              <select value={targetLang} onChange={e => setTargetLang(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white">
                <option>Ingliz tili</option>
                <option>Nemis tili</option>
                <option>Koreys tili</option>
                <option>Rus tili</option>
              </select>
            </div>
          </div>
          
          <div className="border-2 border-dashed border-cyan-500/40 bg-cyan-950/10 rounded-3xl p-8 flex flex-col items-center justify-center text-center space-y-3 cursor-pointer hover:border-cyan-400 transition relative">
            <input type="file" onChange={handleFileChange} accept=".pdf,.doc,.docx,.jpg,.png" className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
            <div className="w-14 h-14 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-2xl">
              <i className="fa-solid fa-cloud-arrow-up"></i>
            </div>
            <div>
              <h4 className="text-base font-bold text-white">Faylni yuklang</h4>
              <p className="text-xs text-slate-400 font-mono mt-0.5">PDF, DOCX yoki JPG (Max 10MB)</p>
            </div>
          </div>
          
          {translationResult && (
            <div className="mt-6 p-6 rounded-2xl bg-emerald-900/20 border border-emerald-500/30 text-white">
              <h4 className="font-bold text-emerald-400 mb-2">Tarjima muvaffaqiyatli yakunlandi!</h4>
              <p className="text-sm text-slate-300 max-h-40 overflow-y-auto">{translationResult}</p>
              <button onClick={downloadPDF} className="mt-4 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-bold flex items-center gap-2 transition">
                <Download className="w-4 h-4" /> Yuklab olish
              </button>
            </div>
          )}
          
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
            <button onClick={translateFile} disabled={isTranslating} className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-cyan-500/25 transition flex items-center justify-center gap-2">
              {isTranslating ? <RefreshCw className="w-4 h-4 animate-spin" /> : <i className="fa-solid fa-paper-plane"></i>}
              <span>{isTranslating ? 'Tarjima qilinmoqda...' : 'Tarjimaga yuborish'}</span>
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
"""

def get_moliya_code():
    return """import { motion } from 'motion/react';

export default function Moliya() {
  return (
    <motion.div key="funding" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="page-content space-y-6">
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
  );
}
"""

with open('scholarmap-frontend/src/Tarjima.tsx', 'w', encoding='utf-8') as f:
    f.write(get_translation_code())

with open('scholarmap-frontend/src/Moliya.tsx', 'w', encoding='utf-8') as f:
    f.write(get_moliya_code())

print("Created components")
