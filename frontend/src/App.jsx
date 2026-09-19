import React, { useState } from 'react';
import TopNav from './components/TopNav';
import TelemetryTerminal from './components/TelemetryTerminal';
import AttackGraph from './components/AttackGraph';
import ActionCenter from './components/ActionCenter';
import { simulateBurst, simulateReset, executeContainment } from './services/api';

function App() {
  const [autoMode, setAutoMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [events, setEvents] = useState([]);
  const [dossier, setDossier] = useState(null);
  const [containmentActions, setContainmentActions] = useState([]);

  const handleReset = async () => {
    setLoading(true);
    try {
      await simulateReset();
      setEvents([]);
      setDossier(null);
      setContainmentActions([]);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleInject = async () => {
    setLoading(true);
    try {
      const res = await simulateBurst();
      console.log("Injection triggered, response:", res);
      
      // Simulate real-time streaming of events to the terminal
      if (res.dossiers && res.dossiers.length > 0) {
        // Flatten alerts into events for the terminal just to show them, 
        // normally we would fetch the raw stream. For demo, we just use alerts.
        const ingestedEvents = res.dossiers[0].alerts.map(a => a.event);
        setEvents(ingestedEvents);
        
        // Wait for 1s to simulate AI processing time before showing dossier
        setTimeout(() => {
          setDossier(res.dossiers[0]);
          
          if (autoMode) {
            // Wait 1.5s then trigger containment
            setTimeout(async () => {
              await triggerContainment(res.dossiers[0].incident_id);
            }, 1500);
          }
        }, 1000);
      } else {
        console.warn("No new dossiers generated from burst. Ensure backend state is reset.");
      }
    } catch (e) {
      console.error("Error during injection:", e);
    }
    setLoading(false);
  };

  const triggerContainment = async (incidentId) => {
    try {
      const res = await executeContainment({
        incident_id: incidentId,
        attacker_ip: "198.51.100.23",
        compromised_user: "svc_deployer",
        bastion_ip: "10.0.1.10",
        trigger_deception: true,
        target_ip: "10.0.2.45"
      });
      setContainmentActions(res.actions);
      
      // Update dossier to show deception is active
      setDossier(prev => ({
        ...prev,
        deception_status: "TRAP_ACTIVE",
        decoy_details: res.deception_status
      }));
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-zinc-50 overflow-hidden">
      <TopNav 
        autoMode={autoMode} 
        setAutoMode={setAutoMode} 
        onInject={handleInject} 
        onReset={handleReset} 
        loading={loading}
      />
      
      <main className="flex-1 p-4 grid grid-cols-12 gap-4 h-[calc(100vh-73px)]">
        {/* Left Panel */}
        <div className="col-span-4 h-full">
          <TelemetryTerminal events={events} />
        </div>
        
        {/* Center Panel */}
        <div className="col-span-4 h-full">
          <AttackGraph dossier={dossier} actions={containmentActions} />
        </div>
        
        {/* Right Panel */}
        <div className="col-span-4 h-full">
          <ActionCenter dossier={dossier} actions={containmentActions} />
        </div>
      </main>
    </div>
  );
}

export default App;
