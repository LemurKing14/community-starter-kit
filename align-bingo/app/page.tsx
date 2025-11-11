'use client';
import Connect from './components/Connect';
import AlignCardView from './components/AlignCardView';
import CallerPanel from './components/CallerPanel';

export default function Page(){
  return (
    <Connect>
      <main className="wrap">
        <AlignCardView />
        <CallerPanel />
      </main>
    </Connect>
  );
}
