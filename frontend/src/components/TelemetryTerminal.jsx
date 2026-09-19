import React, { useEffect, useRef } from 'react';
import clsx from 'clsx';
import { Terminal } from 'lucide-react';

export default function TelemetryTerminal({ events = [] }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  const getEventColor = (severity) => {
    if (severity >= 80) return "bg-yellow-400 text-black font-bold border-yellow-400 rounded-none";
    if (severity >= 50) return "bg-yellow-400 text-black font-bold border-yellow-400 rounded-none";
    return "text-zinc-500 border-zinc-800 bg-transparent rounded-none";
  };

  return (
    <div className="flex flex-col h-full bg-zinc-950 text-zinc-300 rounded-none border border-zinc-300 overflow-hidden relative">
      <div className="bg-zinc-900 px-4 py-2 flex items-center border-b border-zinc-800 shrink-0">
        <Terminal className="w-4 h-4 text-zinc-500 mr-2" />
        <span className="text-xs font-mono text-zinc-500">telemetry_stream.log</span>
      </div>
      
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 font-mono text-sm terminal-scroll space-y-2"
      >
        {events.map((evt, idx) => {
          const colorClass = getEventColor(evt.severity_baseline);
          return (
            <div key={idx} className={clsx("p-2 border", colorClass)}>
              <div className="flex justify-between items-start mb-1">
                <span className="opacity-80">[{new Date(evt.timestamp).toLocaleTimeString()}]</span>
                <span className="px-1.5 py-0.5 text-[10px] tracking-wider uppercase border border-current opacity-70">
                  {evt.source_type}
                </span>
              </div>
              <div className="mb-1">{evt.action}</div>
              <div className="text-xs opacity-70">
                {evt.source_ip} {evt.destination_ip ? `-> ${evt.destination_ip}` : ''}
              </div>
              <div className="text-xs opacity-50 mt-1 truncate">
                {JSON.stringify(evt.payload_meta)}
              </div>
            </div>
          );
        })}
        {events.length === 0 && (
          <div className="text-zinc-600 flex items-center justify-center h-full">
            Waiting for telemetry...
          </div>
        )}
      </div>
    </div>
  );
}
