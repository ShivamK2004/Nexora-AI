class ByteTokenizer:
    """Deterministic UTF-8 byte tokenizer for a tiny research prototype.

    IDs 0..255 represent bytes; 256=BOS and 257=EOS. This is intentionally
    simple and is not a replacement for a production multilingual tokenizer.
    """
    bos_token_id = 256
    eos_token_id = 257
    vocab_size = 258
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        ids = list(text.encode("utf-8"))
        return ([self.bos_token_id] + ids + [self.eos_token_id]) if add_special_tokens else ids
    def decode(self, ids: list[int]) -> str:
        data = bytes(int(i) for i in ids if 0 <= int(i) <= 255)
        return data.decode("utf-8", errors="replace")
