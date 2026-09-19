import React from 'react';
import { ShieldAlert, Activity, RefreshCw } from 'lucide-react';
import clsx from 'clsx';

export default function TopNav({ 
  autoMode, 
  setAutoMode, 
  onInject, 
  onReset, 
  loading 
}) {
  return (
    <div className="flex items-center justify-between p-4 bg-white border-b border-zinc-200">
      <div className="flex items-center space-x-3">
        <ShieldAlert className="text-zinc-900 w-8 h-8" />
        <h1 className="text-xl font-bold tracking-widest text-zinc-900">ATHEUS <span className="text-zinc-500 font-normal">// Autonomous Cyber Defense Engine</span></h1>
      </div>

      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-2 bg-white px-4 py-1.5 border border-zinc-200 shadow-sm">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="tracking-widest text-[10px] font-semibold text-zinc-900">ACTIVE DEFENSE ARMED</span>
        </div>

        <div className="flex items-center space-x-3">
          <span className="tracking-widest text-[10px] font-semibold text-zinc-900 uppercase">Autonomous Mode</span>
          <button 
            onClick={() => setAutoMode(!autoMode)}
            className={clsx(
              "w-12 h-6 rounded-full transition-colors relative",
              autoMode ? "bg-yellow-400" : "bg-zinc-200"
            )}
          >
            <div className={clsx(
              "w-4 h-4 bg-white rounded-full absolute top-1 transition-transform",
              autoMode ? "translate-x-7" : "translate-x-1"
            )}></div>
          </button>
        </div>

        <button 
          onClick={onReset}
          disabled={loading}
          className="flex items-center space-x-2 px-4 py-2 bg-white hover:bg-zinc-50 text-zinc-800 border border-zinc-300 shadow-sm transition-colors"
        >
          <RefreshCw className={clsx("w-4 h-4", loading && "animate-spin")} />
          <span>Reset</span>
        </button>

        <button 
          onClick={onInject}
          disabled={loading}
          className="flex items-center space-x-2 px-5 py-2 bg-yellow-400 hover:bg-yellow-500 text-black font-semibold tracking-wide border border-yellow-500 shadow-sm transition-all active:scale-[0.98] disabled:opacity-50 disabled:shadow-none"
        >
          <Activity className="w-4 h-4" />
          <span>Inject APT Attack Chain</span>
        </button>
      </div>
    </div>
  );
}
