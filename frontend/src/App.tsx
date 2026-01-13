import { useState } from 'react';
import axios from 'axios';
import { BookOpen, Send, FileText, CheckCircle, AlertTriangle, Loader2 } from 'lucide-react';

// Types matching our Backend
interface GenerateResponse {
  final_document: string;
  revisions: number;
  final_critique: string;
  used_context: number;
}

function App() {
  const [topic, setTopic] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (msg: string) => setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);

  const handleGenerate = async () => {
    if (!topic) return;
    setStatus('loading');
    setLogs([]);
    setResult(null);

    addLog(`🚀 Starting workflow for: "${topic}"`);
    addLog("🔍 Searching Knowledge Base...");

    try {
      const response = await axios.post('/api/v1/generate', {
        topic: topic,
        tone: "technical"
      });

      setResult(response.data);
      addLog(`✅ Generation Complete! Revisions: ${response.data.revisions}`);
      setStatus('success');
    } catch (err) {
      console.error(err);
      addLog("❌ Error: Failed to contact agents.");
      setStatus('error');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 font-sans">
      {/* Header */}
      <header className="bg-slate-900 text-white p-6 shadow-md">
        <div className="max-w-6xl mx-auto flex items-center gap-3">
          <BookOpen className="text-sky-400" size={32} />
          <div>
            <h1 className="text-2xl font-bold tracking-tight">DocuForge</h1>
            <p className="text-slate-400 text-sm">Autonomous Technical Documentation Engine</p>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* Left Col: Controls */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <FileText size={20} className="text-sky-600" /> Request
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Topic / Query</label>
                <textarea
                  className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-sky-500 focus:outline-none h-32 resize-none"
                  placeholder="e.g. How do I install the HMP155 sensor?"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                />
              </div>
              <button
                onClick={handleGenerate}
                disabled={status === 'loading' || !topic}
                className="w-full bg-sky-600 hover:bg-sky-700 text-white py-3 rounded-lg font-medium flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
              >
                {status === 'loading' ? <Loader2 className="animate-spin" /> : <Send size={18} />}
                Generate Draft
              </button>
            </div>
          </div>

          {/* System Logs */}
          <div className="bg-slate-900 p-4 rounded-xl shadow-sm text-sm font-mono h-64 overflow-y-auto">
            <h3 className="text-slate-400 text-xs uppercase tracking-wider mb-2">System Logs</h3>
            {logs.length === 0 && <span className="text-slate-600 italic">Ready...</span>}
            {logs.map((log, i) => (
              <div key={i} className="text-green-400 mb-1">{log}</div>
            ))}
          </div>
        </div>

        {/* Right Col: Output */}
        <div className="lg:col-span-2 space-y-6">
          {status === 'success' && result && (
            <>
              {/* Stats Cards */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 flex items-center gap-3">
                  <div className="p-2 bg-green-100 text-green-700 rounded-full">
                    <CheckCircle size={20} />
                  </div>
                  <div>
                    <div className="text-2xl font-bold">{result.revisions}</div>
                    <div className="text-xs text-slate-500">Revisions Made</div>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 flex items-center gap-3">
                  <div className="p-2 bg-amber-100 text-amber-700 rounded-full">
                    <AlertTriangle size={20} />
                  </div>
                  <div>
                    <div className="text-2xl font-bold">{result.used_context}</div>
                    <div className="text-xs text-slate-500">Sources Cited</div>
                  </div>
                </div>
              </div>

              {/* Final Document */}
              <div className="bg-white p-8 rounded-xl shadow-lg border border-slate-200">
                <h2 className="text-xl font-bold mb-6 text-slate-900 border-b pb-4">Draft Output</h2>
                <div className="prose prose-slate max-w-none text-slate-700 whitespace-pre-wrap">
                  {result.final_document}
                </div>
              </div>

              {/* Critique Report */}
              <div className="bg-slate-50 p-6 rounded-lg border border-slate-200">
                <h3 className="text-sm font-bold text-slate-500 uppercase mb-2">Final Editor's Note</h3>
                <p className="text-sm text-slate-600 italic">"{result.final_critique}"</p>
              </div>
            </>
          )}

          {status === 'idle' && (
            <div className="h-full flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-xl p-12">
              <BookOpen size={48} className="mb-4 opacity-20" />
              <p>Enter a topic to start the multi-agent workflow.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;