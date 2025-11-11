'use client';
import Image from 'next/image';
import { useAccount } from 'wagmi';
import { useEffect, useMemo, useState } from 'react';
import QRCode from 'qrcode';
import { makeAlignCard } from '../lib/alignCard';
import { truncateSig } from '../lib/eip712';

export default function AlignCardView(){
  const { address } = useAccount();
  const [seed, setSeed] = useState<`0x${string}`>('0x'.padEnd(66,'0') as `0x${string}`);
  const [sig, setSig] = useState<string>('0x');
  const [qr, setQr] = useState<string>('');
  const gameId = 1;

  // demo: derive a pseudo-seed per wallet (real flow: after mint we know tokenId & seed from event)
  useEffect(()=>{ if(address){ setSeed(('0x'+address.slice(2).padEnd(64,'0')) as `0x${string}`); }},[address]);

  const card = useMemo(()=> makeAlignCard(seed), [seed]);

  useEffect(()=>{
    const proof = JSON.stringify({ wallet: address, seed, gameId, sig });
    QRCode.toDataURL(proof).then(setQr);
  },[address, seed, sig]);

  return (
    <div className="card">
      <div className="badge">A:1–15 · L:16–30 · I:31–45 · G:46–60 · N:61–75</div>
      <h1>ALIGN</h1>
      <div className="grid">
        {card.grid.map((c,i)=>(
          <div key={i} className={'cell'+(c.col==='FREE'?' free':'')}>
            {c.col==='FREE' ? 'A26Z' : c.val}
          </div>
        ))}
      </div>
      <div className="footer">
        <div>Seed: {seed.slice(0,10)}…{seed.slice(-6)}</div>
        <div>Sig: {sig==='0x'?'—':truncateSig(sig)}</div>
        {qr && (
          <Image
            src={qr}
            alt="ALIGN QR proof"
            width={96}
            height={96}
            unoptimized
            style={{ marginTop: 8, width: 96, height: 96 }}
          />
        )}
      </div>
      <button className="btn" onClick={async ()=>{
        if (!address) return;
        const res = await fetch('/api/sign',{method:'POST',headers:{'content-type':'application/json'},
          body: JSON.stringify({
            wallet: address, tokenId: 1, seed, gameId,
            verifyingContract: process.env.NEXT_PUBLIC_CONTRACT,
            chainId: Number(process.env.NEXT_PUBLIC_CHAIN_ID) || 0
          })
        }).then(r=>r.json());
        setSig(res.signature);
      }}>Get Signature</button>
    </div>
  );
}
