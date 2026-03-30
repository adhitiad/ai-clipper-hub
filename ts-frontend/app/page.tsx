"use client";
import { useState, useEffect } from "react";

export default function Dashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("Idle");
  const [platform, setPlatform] = useState("tiktok");
  const [caption, setCaption] = useState("This clip is insane! #viral");

  useEffect(() => {
    if (!taskId || status === "Ready" || status.startsWith("Error")) return;

    const checkStatus = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/status/${taskId}`);
        if (!res.ok) throw new Error("Network response was not ok");
        const data = await res.json();
        setStatus(data.status);
      } catch (error) {
        console.error("Error fetching status:", error);
      }
    };

    const intervalId = setInterval(checkStatus, 2000);
    return () => clearInterval(intervalId);
  }, [taskId, status]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleStartProcessing = async () => {
    if (!file) {
      alert("Please select an MP4 file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading...");
    try {
      const res = await fetch("http://localhost:8000/api/process", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setTaskId(data.task_id);
      setStatus("Queued");
    } catch (error: any) {
      console.error("Failed to start processing:", error);
      setStatus(`Error: ${error.message}`);
    }
  };

  const handleDownload = () => {
    if (taskId) {
      window.location.href = `http://localhost:8000/api/videos/${taskId}/download`;
    }
  };

  const handlePublish = async (platformName: string) => {
    if (!taskId) return;
    try {
      const res = await fetch(`http://localhost:8000/api/videos/${taskId}/publish`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ platform: platformName, caption }),
      });
      if (!res.ok) throw new Error(await res.text());
      alert(`Successfully initiated publish to ${platformName}!`);
    } catch (error: any) {
      console.error("Publish failed:", error);
      alert(`Publish failed: ${error.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      <h1 className="text-3xl font-bold text-emerald-400 mb-6 flex items-center gap-3">
        <span className="relative flex h-4 w-4">
          {status !== "Idle" && status !== "Ready" && !status.startsWith("Error") && (
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          )}
          <span className="relative inline-flex rounded-full h-4 w-4 bg-emerald-500"></span>
        </span>
        AI Content Director Hub
      </h1>

      <div className="max-w-2xl bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg mb-8">
        <h2 className="text-xl font-semibold mb-4 text-white">1. Upload Video</h2>
        <div className="flex flex-col gap-4">
          <input
            type="file"
            accept="video/mp4"
            onChange={handleFileChange}
            className="block w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100 cursor-pointer"
          />
          <button
            onClick={handleStartProcessing}
            disabled={!file || (status !== "Idle" && status !== "Ready" && !status.startsWith("Error"))}
            className="bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition-colors"
          >
            Start Processing
          </button>
        </div>
      </div>

      <div className="max-w-2xl bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg mb-8">
        <h2 className="text-xl font-semibold mb-4 text-white">2. Status: {status}</h2>
        {taskId && (
          <p className="text-sm text-slate-400 mb-2">Task ID: <span className="font-mono">{taskId}</span></p>
        )}
      </div>

      {status === "Ready" && (
        <div className="max-w-2xl bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <h2 className="text-xl font-semibold mb-4 text-white">3. Actions</h2>
          <div className="flex flex-col gap-6">
            <button
              onClick={handleDownload}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition-colors w-full sm:w-auto"
            >
              Download Video
            </button>

            <div className="border-t border-slate-700 pt-4">
              <h3 className="text-lg font-medium text-slate-300 mb-2">Publish to Socials</h3>
              <input
                type="text"
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
                placeholder="Enter caption..."
                className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white mb-4 focus:outline-none focus:border-emerald-500"
              />
              <div className="flex gap-4 flex-wrap">
                <button
                  onClick={() => handlePublish("tiktok")}
                  className="bg-black hover:bg-gray-900 text-white border border-slate-600 font-bold py-2 px-4 rounded transition-colors flex-1 min-w-[120px]"
                >
                  Upload to TikTok
                </button>
                <button
                  onClick={() => handlePublish("youtube")}
                  className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition-colors flex-1 min-w-[120px]"
                >
                  Upload to YouTube
                </button>
                <button
                  onClick={() => handlePublish("instagram")}
                  className="bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 hover:opacity-90 text-white font-bold py-2 px-4 rounded transition-colors flex-1 min-w-[120px]"
                >
                  Upload to Instagram
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
