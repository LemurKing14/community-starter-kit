# ALIGN (Bingo) One-Card System

## Quickstart
1. `cp .env.example .env` and fill values (Base Sepolia RPC, keys).
2. Install:
   - `npm i` (root)
   - `npx hardhat compile`
3. Deploy:
   - `npx hardhat run scripts/deploy.ts --network baseSepolia`
   - Put contract address into `NEXT_PUBLIC_CONTRACT` in `.env`
4. Dev:
   - `npm run dev` (Next.js)
5. Use:
   - Connect wallet (Base Sepolia).
   - Click **Get Signature** to fetch a demo EIP-712 sig.
   - Card shows **A26Z** center, gradient, and footer proof.
   - Caller panel: draw/reset; switch to commit-reveal to see a commit hash.

## One-per-wallet
Enforced in contract: `minted[msg.sender] = true`. Extension: make non-transferable if needed.

## Verifiability
- Seed is shown and used to deterministically lay out the grid.
- Signature (EIP-712 over wallet, tokenId, seed, gameId) is printed; can be verified.

## To-do for production
- Replace demo `/api/sign` with secure backend.
- Hook mint flow: listen to `CardMinted` event to capture real `tokenId` + `seed`.
- Gate game lobby by NFT ownership.
