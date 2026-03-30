"use client";
import { useEffect, useState } from "react";

interface ClipProject { project_id: string; niche: string; title: string; status: string; timestamp: string; }
interface DashboardData { agent_status: string; total_projects: number; recent_clips: ClipProject[]; }

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    const fetchData = () => {
      fetch("http://localhost:8000/api/dashboard")
        .then((res) => res.json()).then((data) => setData(data)).catch((err) => console.error(err));
    };
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!data) return <div className="p-10 text-white bg-slate-900 min-h-screen">Memuat Sistem...</div>;

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      <h1 className="text-3xl font-bold text-emerald-400 mb-6 flex items-center gap-3">
        <span className="relative flex h-4 w-4">
          {data.agent_status !== "Idle" && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>}
          <span className="relative inline-flex rounded-full h-4 w-4 bg-emerald-500"></span>
        </span>
        AI Content Director Hub
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <h2 className="text-slate-400 text-sm font-semibold uppercase">Status AI Agent</h2>
          <p className="text-2xl font-bold text-white mt-2">{data.agent_status}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <h2 className="text-slate-400 text-sm font-semibold uppercase">Total Video Dirender</h2>
          <p className="text-4xl font-bold text-indigo-400 mt-2">{data.total_projects}</p>
        </div>
      </div>

      <div className="overflow-x-auto bg-slate-800 rounded-xl border border-slate-700">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-700 text-slate-300">
            <tr><th className="p-4">Waktu</th><th className="p-4">Niche</th><th className="p-4">Hook Final</th><th className="p-4">ID Vizard</th><th className="p-4">Status</th></tr>
          </thead>
          <tbody>
            {data.recent_clips.map((clip, idx) => (
              <tr key={idx} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                <td className="p-4 text-slate-300">{new Date(clip.timestamp).toLocaleString('id-ID')}</td>
                <td className="p-4 font-medium text-emerald-300">{clip.niche}</td>
                <td className="p-4">{clip.title}</td>
                <td className="p-4 font-mono text-xs text-slate-400">{clip.project_id}</td>
                <td className="p-4"><span className="bg-blue-500/10 text-blue-400 px-3 py-1 rounded-full">{clip.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
