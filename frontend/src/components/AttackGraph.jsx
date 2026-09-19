import React from 'react';
import clsx from 'clsx';
import { ShieldCheck, ShieldAlert, Target, Crosshair } from 'lucide-react';

export default function AttackGraph({ dossier, actions }) {
  const hasIncident = dossier != null;
  const isTrapActive = dossier?.deception_status === "TRAP_ACTIVE";
  const isolatedHosts = actions?.filter(a => a.action === "HOST_ISOLATION").map(a => a.target) || [];
  
  // Predict target
  const predicted = dossier?.predicted_target?.target || "";
  const isDbPredicted = predicted.includes("Active Directory") || predicted.includes("DB") || predicted.includes("Production");

  return (
    <div className="h-full bg-white bg-dot-grid rounded-none border border-zinc-200 p-6 flex flex-col items-center justify-center relative overflow-hidden">
      <h2 className="absolute top-4 left-4 text-xs font-bold tracking-widest text-zinc-500">NETWORK CANVAS</h2>
      
      {/* Node 1: Adversary */}
      <div className="mb-12 w-48 text-center p-3 rounded-none border border-red-600 bg-white relative z-10">
        <div className="text-xs text-red-600 font-bold mb-1 flex items-center justify-center"><Crosshair className="w-3 h-3 mr-1"/> Adversary</div>
        <div className="font-mono text-sm text-zinc-800">198.51.100.23</div>
      </div>

      {/* SVG Connectors */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none z-0" viewBox="0 0 100 100" preserveAspectRatio="none">
        <defs>
          <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#ef4444" />
          </marker>
          <marker id="arrow-amber" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#f59e0b" />
          </marker>
          <marker id="arrow-slate" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#d4d4d8" />
          </marker>
        </defs>

        {/* Adv to Bastion */}
        <line x1="50" y1="20" x2="50" y2="40" stroke={hasIncident ? "#dc2626" : "#d4d4d8"} strokeWidth="1" markerEnd={`url(#arrow-${hasIncident ? 'red' : 'slate'})`} />
        
        {/* Bastion to HoneyDB */}
        <path d="M 50 55 C 50 65, 25 65, 25 75" fill="none" stroke={isTrapActive ? "#facc15" : "#d4d4d8"} strokeWidth="1" strokeDasharray={isTrapActive ? "2,2" : "0"} markerEnd={`url(#arrow-${isTrapActive ? 'amber' : 'slate'})`} className={clsx(isTrapActive && "animate-pulse")} />
        
        {/* Bastion to Prod DB */}
        <path d="M 50 55 C 50 65, 75 65, 75 75" fill="none" stroke={hasIncident && !isTrapActive ? "#dc2626" : "#d4d4d8"} strokeWidth="1" markerEnd={`url(#arrow-${hasIncident && !isTrapActive ? 'red' : 'slate'})`} />
      </svg>

      {/* Node 2: Bastion */}
      <div className={clsx(
        "mb-16 w-48 text-center p-3 rounded-none border z-10 transition-colors duration-500",
        isolatedHosts.includes("10.0.1.10") ? "border-zinc-800 bg-zinc-100" : (hasIncident ? "border-red-600 animate-pulse bg-red-50" : "border-zinc-300 bg-white")
      )}>
        <div className="flex justify-between items-center mb-1">
          <div className={clsx("text-xs font-bold", isolatedHosts.includes("10.0.1.10") ? "text-zinc-900" : (hasIncident ? "text-red-700" : "text-zinc-800"))}>Bastion Host</div>
          {isolatedHosts.includes("10.0.1.10") ? <ShieldCheck className="w-4 h-4 text-zinc-900" /> : (hasIncident && <ShieldAlert className="w-4 h-4 text-red-600" />)}
        </div>
        <div className={clsx("font-mono text-sm", isolatedHosts.includes("10.0.1.10") ? "text-zinc-700" : (hasIncident ? "text-red-600" : "text-zinc-600"))}>10.0.1.10</div>
        {isolatedHosts.includes("10.0.1.10") && <div className="mt-2 text-[10px] text-zinc-100 bg-zinc-900 px-2 py-1 font-bold">ISOLATED & SECURED</div>}
      </div>

      <div className="flex w-full justify-around z-10">
        {/* Node 3: HoneyDB */}
        <div className={clsx(
          "w-48 text-center p-3 rounded-none border transition-all duration-500",
          isTrapActive ? "border-yellow-400 bg-yellow-400" : "border-zinc-300 border-dashed bg-white opacity-50"
        )}>
          <div className={clsx("text-xs font-bold mb-1", isTrapActive ? "text-black" : "text-yellow-600")}>HoneyDB Decoy</div>
          <div className={clsx("font-mono text-sm", isTrapActive ? "text-zinc-900" : "text-zinc-500")}>10.0.2.99</div>
          {isTrapActive && <div className="mt-2 text-[10px] text-black bg-white px-2 py-1 font-bold">TRAP ACTIVE</div>}
        </div>

        {/* Node 4: Prod DB */}
        <div className={clsx(
          "w-48 text-center p-3 rounded-none border transition-all duration-500",
          !isTrapActive && hasIncident ? "border-red-600 bg-red-50" : "border-zinc-900 bg-zinc-900",
          isDbPredicted && !isTrapActive ? "border-dashed border-red-600" : ""
        )}>
           <div className="flex justify-between items-center mb-1">
            <div className={clsx("text-xs font-bold", !isTrapActive && hasIncident ? "text-red-700" : "text-white")}>Production DB</div>
            {isDbPredicted && !isTrapActive && <Target className="w-4 h-4 text-red-600" />}
          </div>
          <div className={clsx("font-mono text-sm", !isTrapActive && hasIncident ? "text-red-600" : "text-zinc-300")}>10.0.2.45</div>
        </div>
      </div>
    </div>
  );
}
