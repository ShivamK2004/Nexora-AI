import torch
from torch import nn
from torch.nn import functional as F
from model.nexora_lm.config import ModelConfig

class CausalBlock(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.n_embd)
        self.attn = nn.MultiheadAttention(cfg.n_embd, cfg.n_head, dropout=cfg.dropout, batch_first=True)
        self.ln2 = nn.LayerNorm(cfg.n_embd)
        self.mlp = nn.Sequential(nn.Linear(cfg.n_embd, 4*cfg.n_embd), nn.GELU(),
                                  nn.Linear(4*cfg.n_embd, cfg.n_embd), nn.Dropout(cfg.dropout))
        self.dropout = nn.Dropout(cfg.dropout)
    def forward(self, x):
        length = x.size(1)
        mask = torch.triu(torch.ones(length, length, device=x.device, dtype=torch.bool), diagonal=1)
        h = self.ln1(x)
        attn, _ = self.attn(h, h, h, attn_mask=mask, need_weights=False)
        x = x + self.dropout(attn)
        return x + self.mlp(self.ln2(x))

class NexoraLM(nn.Module):
    def __init__(self, cfg: ModelConfig | None = None):
        super().__init__()
        self.cfg = cfg or ModelConfig()
        self.token_embedding = nn.Embedding(self.cfg.vocab_size, self.cfg.n_embd)
        self.position_embedding = nn.Embedding(self.cfg.block_size, self.cfg.n_embd)
        self.blocks = nn.Sequential(*[CausalBlock(self.cfg) for _ in range(self.cfg.n_layer)])
        self.final_norm = nn.LayerNorm(self.cfg.n_embd)
        self.lm_head = nn.Linear(self.cfg.n_embd, self.cfg.vocab_size, bias=False)
        self.lm_head.weight = self.token_embedding.weight
    def forward(self, idx, targets=None):
        batch, length = idx.shape
        if length > self.cfg.block_size:
            raise ValueError(f"Sequence length {length} exceeds block size {self.cfg.block_size}")
        pos = torch.arange(length, device=idx.device)
        x = self.token_embedding(idx) + self.position_embedding(pos)[None,:,:]
        logits = self.lm_head(self.final_norm(self.blocks(x)))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        return logits, loss
    @torch.no_grad()
    def generate(self, idx, max_new_tokens=100, temperature=0.8, top_k=40):
        self.eval()
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.cfg.block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / max(temperature, 1e-5)
            if top_k:
                values, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < values[:, [-1]]] = -float('inf')
            probs = F.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, next_id), dim=1)
        return idx
