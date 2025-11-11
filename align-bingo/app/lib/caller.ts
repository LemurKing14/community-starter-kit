export class AlignCaller {
  private pool: number[] = []; private drawn: number[] = [];
  constructor(){ this.reset(); }
  reset(){ this.pool = Array.from({length:75},(_,i)=>i+1); this.drawn=[]; }
  draw(): { number:number; remaining:number } | null {
    if (!this.pool.length) return null;
    const j = Math.floor(Math.random()*this.pool.length);
    const [n] = this.pool.splice(j,1); this.drawn.push(n);
    return { number:n, remaining:this.pool.length };
  }
  history(){ return [...this.drawn]; }
}
