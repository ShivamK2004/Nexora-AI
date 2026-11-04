from dataclasses import dataclass
@dataclass
class ModelConfig:
    vocab_size: int = 258  # 256 byte values + BOS/EOS
    block_size: int = 256
    n_layer: int = 4
    n_head: int = 4
    n_embd: int = 128
    dropout: float = 0.1
    @property
    def n_params_estimate(self) -> int:
        # Rough estimate; exact count is available from model.parameters().
        return 12 * self.n_layer * self.n_embd * self.n_embd + self.vocab_size * self.n_embd
