import React, { useState } from 'react';
import clsx from 'clsx';
import { Bot, Send, CheckCircle2 } from 'lucide-react';
import { chatCopilot } from '../services/api';

export default function ActionCenter({ dossier, actions }) {
  const [activeTab, setActiveTab] = useState('technical');
  const [copilotInput, setCopilotInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);

  const threatScore = dossier?.threat_score || 0;
  const severity = dossier?.severity || 'NONE';
  const mitreTactics = dossier?.mitre_tactics || [];
  
  const handleChat = async (q) => {
    if (!q.trim()) return;
    
    setChatHistory(prev => [...prev, { role: 'user', content: q }]);
    setCopilotInput('');
    setChatLoading(true);
    
    try {
      const incidentId = dossier?.incident_id || "INC-TEST-API";
      const res = await chatCopilot({ incident_id: incidentId, query: q });
      setChatHistory(prev => [...prev, { role: 'copilot', content: res.reply, cited: res.cited_events }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: 'copilot', content: "Error communicating with AI Copilot." }]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="h-full flex flex-col bg-white rounded-none border border-zinc-200 overflow-hidden text-zinc-900">
      {/* Header Info */}
      <div className="p-4 border-b border-zinc-200 flex justify-between items-center bg-zinc-50">
        <div className="flex items-center space-x-4">
          <div className="relative w-16 h-16 flex items-center justify-center rounded-full border-4 border-zinc-200">
            <svg className="absolute inset-0 w-full h-full transform -rotate-90">
              <circle cx="28" cy="28" r="26" fill="transparent" strokeWidth="4" 
                className={clsx(
                  "transition-all duration-1000",
                  threatScore > 80 ? "stroke-red-600" : threatScore > 50 ? "stroke-yellow-400" : "stroke-zinc-300"
                )}
                strokeDasharray="163" 
                strokeDashoffset={163 - (163 * threatScore) / 100}
              />
            </svg>
            <span className="text-xl font-bold text-zinc-900">{threatScore}</span>
          </div>
          <div>
            <div className="text-xs text-zinc-500 font-bold uppercase tracking-wider">Severity</div>
            <div className={clsx("text-lg font-bold", 
              severity === 'CRITICAL' ? 'text-red-600' : severity === 'HIGH' ? 'text-yellow-500' : 'text-zinc-900'
            )}>{severity}</div>
          </div>
        </div>
      </div>

      {/* MITRE Badges */}
      <div className="p-4 border-b border-zinc-200">
        <div className="text-xs text-zinc-500 font-bold mb-2">MITRE ATT&CK TTPs</div>
        <div className="flex flex-wrap gap-2">
          {mitreTactics.map((ttp, i) => (
            <span key={i} className="px-2 py-1 bg-white border border-zinc-300 rounded-none text-xs text-zinc-800 font-mono shadow-sm">
              {ttp}
            </span>
          ))}
          {mitreTactics.length === 0 && <span className="text-xs text-zinc-500">No active threats detected.</span>}
        </div>
      </div>

      {/* Dual Lens Tabs */}
      <div className="flex border-b border-zinc-200 bg-zinc-50">
        <button 
          onClick={() => setActiveTab('technical')}
          className={clsx("flex-1 py-2 text-xs font-bold uppercase tracking-wider transition-colors", 
            activeTab === 'technical' ? "border-b-2 border-yellow-400 text-black" : "text-zinc-500 hover:text-zinc-800")}
        >
          Technical Forensics
        </button>
        <button 
          onClick={() => setActiveTab('executive')}
          className={clsx("flex-1 py-2 text-xs font-bold uppercase tracking-wider transition-colors", 
            activeTab === 'executive' ? "border-b-2 border-yellow-400 text-black" : "text-zinc-500 hover:text-zinc-800")}
        >
          Executive Brief
        </button>
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-y-auto p-4 terminal-scroll text-sm bg-white">
        {activeTab === 'technical' ? (
          <div className="space-y-4">
            <div>
              <h3 className="font-bold text-zinc-900 mb-1">Attack Reconstruction</h3>
              <p className="text-zinc-700 leading-relaxed">{dossier?.attack_story || "Awaiting telemetry analysis..."}</p>
            </div>
            {actions?.length > 0 && (
              <div className="mt-4 p-3 bg-zinc-50 rounded-none border border-zinc-200 font-mono text-xs">
                <div className="text-zinc-900 font-bold mb-2 border-b border-zinc-200 pb-1">CONTAINMENT EXECUTION LOG</div>
                {actions.map((act, i) => (
                  <div key={i} className="flex items-center text-zinc-800 mt-1">
                    <CheckCircle2 className="w-3 h-3 text-zinc-900 mr-2" />
                    <span className="opacity-70">[{new Date(act.timestamp).toLocaleTimeString()}]</span> 
                    <span className="ml-2 font-bold">[EXECUTED] {act.action.replace('_', ' ')}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            <h3 className="font-bold text-zinc-900 mb-1">Business Impact Summary</h3>
            <div className="p-3 bg-white rounded-none border border-zinc-200 shadow-sm">
              <div className="text-yellow-600 font-bold mb-1">Estimated Liability Prevented</div>
              <div className="text-2xl font-bold text-black mb-3">$1.4M</div>
              <ul className="space-y-2 text-zinc-700 list-disc list-inside">
                <li>Zero Production Data Exfiltrated</li>
                <li>Immediate Regulatory Compliance Maintained</li>
                <li>Business Continuity Preserved</li>
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Copilot Drawer */}
      <div className="border-t border-zinc-200 bg-zinc-50 p-4 flex flex-col h-1/3 min-h-[200px]">
        <div className="flex items-center text-xs text-zinc-900 font-bold mb-2 tracking-widest">
          <Bot className="w-4 h-4 mr-1 text-black" /> ATHEUS COPILOT
        </div>
        
        <div className="flex-1 overflow-y-auto terminal-scroll mb-2 space-y-2 text-xs">
          {chatHistory.map((msg, i) => (
            <div key={i} className={clsx("p-2", msg.role === 'user' ? "bg-zinc-100 border border-zinc-200 ml-4 text-zinc-900" : "bg-white border-l-2 border-yellow-400 pl-3 mr-4 text-zinc-900 shadow-sm")}>
              <div className="font-bold mb-1 opacity-70">{msg.role === 'user' ? 'Analyst' : 'Copilot'}</div>
              <div>{msg.content}</div>
              {msg.cited && msg.cited.length > 0 && (
                <div className="mt-1 pt-1 border-t border-zinc-200 text-[10px] text-zinc-500">Cited: {msg.cited.join(', ')}</div>
              )}
            </div>
          ))}
          {chatLoading && <div className="text-zinc-500 animate-pulse font-mono">Analyzing...</div>}
        </div>

        <div className="flex space-x-2 overflow-x-auto terminal-scroll pb-2 mb-2">
          {["Why was host 10.0.1.10 isolated?", "What is the evidence for lateral movement?", "Explain the active honey-trap deployment."].map((q, i) => (
            <button key={i} onClick={() => handleChat(q)} className="shrink-0 px-2 py-1 bg-white border border-zinc-300 hover:border-zinc-400 shadow-sm text-[10px] text-zinc-700 font-medium whitespace-nowrap transition-colors">
              {q}
            </button>
          ))}
        </div>

        <div className="flex shadow-sm">
          <input 
            type="text" 
            value={copilotInput}
            onChange={e => setCopilotInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleChat(copilotInput)}
            placeholder="Ask Copilot about the incident..."
            className="flex-1 bg-white border border-zinc-300 rounded-l-none border-r-0 px-3 py-1.5 text-sm focus:outline-none focus:border-yellow-400 focus:ring-1 focus:ring-yellow-400 text-zinc-900"
            disabled={chatLoading}
          />
          <button 
            onClick={() => handleChat(copilotInput)}
            disabled={chatLoading}
            className="bg-yellow-400 text-black px-3 rounded-r-none border border-yellow-400 hover:bg-yellow-500 disabled:opacity-50 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
