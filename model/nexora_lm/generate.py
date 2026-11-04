import argparse, torch
from model.nexora_lm.config import ModelConfig
from model.nexora_lm.model import NexoraLM
from model.nexora_lm.tokenizer import ByteTokenizer

def main():
    p=argparse.ArgumentParser(); p.add_argument('--checkpoint',required=True); p.add_argument('--prompt',default='Nexora AI'); p.add_argument('--tokens',type=int,default=200); p.add_argument('--device',default='auto'); a=p.parse_args()
    device='cuda' if a.device=='auto' and torch.cuda.is_available() else ('cpu' if a.device=='auto' else a.device)
    ckpt=torch.load(a.checkpoint,map_location=device,weights_only=False); cfg=ModelConfig(**ckpt['config']); model=NexoraLM(cfg).to(device); model.load_state_dict(ckpt['state_dict'])
    tok=ByteTokenizer(); start=torch.tensor([tok.encode(a.prompt) or [32]],dtype=torch.long,device=device)
    output=model.generate(start,max_new_tokens=a.tokens); print(tok.decode(output[0].tolist()))
if __name__=='__main__': main()
