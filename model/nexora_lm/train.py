import argparse, math
from pathlib import Path
import torch
from model.nexora_lm.config import ModelConfig
from model.nexora_lm.model import NexoraLM
from model.nexora_lm.tokenizer import ByteTokenizer

def main():
    parser = argparse.ArgumentParser(description="Train a small byte-level NexoraLM research model")
    parser.add_argument('--data', required=True); parser.add_argument('--out', default='checkpoints/nexora-tiny.pt')
    parser.add_argument('--steps', type=int, default=500); parser.add_argument('--batch-size', type=int, default=16)
    parser.add_argument('--block-size', type=int, default=128); parser.add_argument('--lr', type=float, default=3e-4)
    parser.add_argument('--device', default='auto'); args = parser.parse_args()
    if args.steps < 1 or args.batch_size < 1: parser.error('steps and batch-size must be positive')
    text = Path(args.data).read_text(encoding='utf-8')
    ids = torch.tensor(ByteTokenizer().encode(text), dtype=torch.long)
    if len(ids) < args.block_size + 2: raise SystemExit('Dataset too small. Add more text or reduce --block-size.')
    device = 'cuda' if args.device == 'auto' and torch.cuda.is_available() else ('cpu' if args.device == 'auto' else args.device)
    cfg = ModelConfig(block_size=args.block_size)
    model = NexoraLM(cfg).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    def batch():
        starts = torch.randint(0, len(ids)-args.block_size-1, (args.batch_size,))
        x = torch.stack([ids[i:i+args.block_size] for i in starts]).to(device)
        y = torch.stack([ids[i+1:i+args.block_size+1] for i in starts]).to(device)
        return x,y
    model.train()
    for step in range(1, args.steps+1):
        x,y=batch(); _,loss=model(x,y); optimizer.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        if step==1 or step%50==0: print(f"step={step}/{args.steps} loss={loss.item():.4f} ppl={math.exp(min(loss.item(),20)):.2f}")
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    torch.save({'config':cfg.__dict__,'state_dict':model.state_dict(),'step':args.steps},out)
    print(f"Saved {out} ({sum(p.numel() for p in model.parameters()):,} parameters) on {device}")
if __name__=='__main__': main()
