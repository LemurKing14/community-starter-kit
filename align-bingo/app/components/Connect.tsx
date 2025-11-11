'use client';
import '@rainbow-me/rainbowkit/styles.css';
import type { ReactNode } from 'react';
import { RainbowKitProvider, ConnectButton, getDefaultConfig, lightTheme } from '@rainbow-me/rainbowkit';
import { WagmiProvider, http } from 'wagmi';
import { baseSepolia } from 'wagmi/chains';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const config = getDefaultConfig({
  appName: 'ALIGN',
  projectId: 'align-demo',
  chains: [baseSepolia],
  transports: { [baseSepolia.id]: http() },
});
const qc = new QueryClient();
export default function Connect({children}:{children:ReactNode}){
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={qc}>
        <RainbowKitProvider theme={lightTheme()}>
          {children}
          <div style={{marginTop:8}}><ConnectButton /></div>
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
