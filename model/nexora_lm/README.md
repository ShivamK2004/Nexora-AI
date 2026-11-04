# NexoraLM research prototype

This folder contains a minimal decoder-only Transformer for learning and validating the training loop. It uses a byte-level tokenizer, learned positional embeddings, causal self-attention, residual MLP blocks, and next-token cross-entropy.

It is deliberately not a production foundation model. Before a serious pretraining run, upgrade tokenizer quality, data deduplication and licensing checks, rotary embeddings, RMSNorm, GQA, mixed precision, distributed training, checkpoint resume, experiment tracking, and a robust benchmark suite. Do not interpret a tiny corpus or toy model as general intelligence.
