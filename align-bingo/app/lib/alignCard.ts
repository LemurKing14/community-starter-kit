export type Cell = { col: 'A'|'L'|'I'|'G'|'N'; val: number } | { col:'FREE'; val:'A26Z' };
export type AlignCard = { title:'ALIGN'; grid: Cell[]; seed: `0x${string}`; };

const COLS = ['A','L','I','G','N'] as const;
const RANGES: Record<typeof COLS[number], [number,number]> = {
  A:[1,15], L:[16,30], I:[31,45], G:[46,60], N:[61,75]
};

// simple xorshift PRNG for layout
function prng(seed: bigint) {
  let x = seed || 1n;
  return () => { x ^= x<<13n; x ^= x>>7n; x ^= x<<17n; return Number(x & ((1n<<53n)-1n))/2**53; };
}
function sampleUnique([lo,hi]:[number,number], k:number, rnd:()=>number): number[] {
  const pool = Array.from({length: hi-lo+1}, (_,i)=>lo+i);
  for (let i=pool.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); [pool[i],pool[j]]=[pool[j],pool[i]]; }
  return pool.slice(0,k).sort((a,b)=>a-b);
}
export function makeAlignCard(seedHex: `0x${string}`): AlignCard {
  const rnd = prng(BigInt(seedHex));
  const cols: number[][] = [];
  (['A','L','I','G','N'] as const).forEach((c)=> cols.push(sampleUnique(RANGES[c],5,rnd)));
  cols[2][2] = -1; // center FREE
  const grid: Cell[] = [];
  for (let r=0;r<5;r++) for (let ci=0;ci<5;ci++){
    const col = COLS[ci]; const val = cols[ci][r];
    grid.push(val===-1? {col:'FREE', val:'A26Z'} : {col, val});
  }
  return { title:'ALIGN', grid, seed: seedHex };
}
