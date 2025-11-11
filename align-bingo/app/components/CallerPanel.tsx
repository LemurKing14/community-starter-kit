'use client';
import { useMemo, useState } from 'react';
import { AlignCaller } from '../lib/caller';
import { VerifiableCaller } from '../lib/verifiableCaller';

export default function CallerPanel(){
  const [history, setHistory] = useState<number[]>([]);
  const [mode, setMode] = useState<'rng'|'vrf'>('rng');
  const [secret, setSecret] = useState<`0x${string}`>('0x11'.padEnd(66,'0') as `0x${string}`);
  const [resetNonce, setResetNonce] = useState(0);
  const caller = useMemo(() => {
    void resetNonce; // include resetNonce to intentionally refresh the instance
    return mode === 'rng' ? new AlignCaller() : new VerifiableCaller(secret);
  }, [mode, secret, resetNonce]);

  return (
    <div className="panel">
      <div className="row">
        <label>Mode:</label>
        <select value={mode} onChange={e=>{ setHistory([]); setMode(e.target.value as any); setResetNonce(n=>n+1); }}>
          <option value="rng">Random</option>
          <option value="vrf">Commit-Reveal</option>
        </select>
        {mode==='vrf' && <div className="commit">Commit: {new VerifiableCaller(secret).commitHash().slice(0,18)}…</div>}
      </div>
      {mode==='vrf' && (
        <div className="row">
          <label>Secret:</label>
          <input value={secret} onChange={e=>{ setSecret(e.target.value as `0x${string}`); setHistory([]); setResetNonce(n=>n+1); }} style={{flex:1}}/>
        </div>
      )}
      <div className="row">
        <button onClick={()=>{
          const result = caller.draw();
          if (result===null) return;
          const n = typeof result === 'number' ? result : result.number;
          setHistory(h=>[...h, n]);
        }}>Draw</button>
        <button onClick={()=>{ setHistory([]); setResetNonce(n=>n+1); }}>Reset</button>
      </div>
      <div className="history">Drawn: {history.join(', ') || '—'}</div>
    </div>
  );
}
