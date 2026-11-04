# NexoraLM — Model Training Guide

## Purpose and limitations

The included model is a small educational decoder-only Transformer used to validate the mechanics of tokenization, causal attention, next-token loss, checkpoint saving, and generation. It is not a competitive general-purpose LLM and is not pretrained at download time. Its byte tokenizer is reversible for UTF-8 but inefficient and not a production tokenizer.

## Environment

Install the standard app dependencies, then install a PyTorch build appropriate for your operating system and CUDA version. The convenience file `requirements-model.txt` installs a generic PyTorch package; for GPU training, check the official PyTorch installation selector and install the matching wheel.

## Dataset requirements

Use content you have rights to use. Keep a manifest of source URL/name, license, acquisition date, permitted use, processing steps, hashes, and exclusions. Remove secrets and personal data, deduplicate near-identical documents, filter low-quality material, and create separate train/validation/test sets. Do not scrape websites in violation of their terms or assume publicly reachable means licensed for model training.

## Train

```bash
python scripts/prepare_dataset.py --input datasets/sample_corpus.txt --output datasets/processed/corpus.txt
python -m model.nexora_lm.train --data datasets/processed/corpus.txt --steps 500 --batch-size 8 --block-size 128 --out checkpoints/nexora-tiny.pt
```

For a tiny corpus, this is only a smoke test. More steps do not compensate for inadequate or unrepresentative data.

## Generate

```bash
python -m model.nexora_lm.generate --checkpoint checkpoints/nexora-tiny.pt --prompt "Nexora AI" --tokens 100
```

## Next research upgrades

1. Adopt a versioned BPE/SentencePiece tokenizer with special-token policy and normalization tests.
2. Build a high-quality licensed corpus and immutable data manifest.
3. Add a deterministic train/validation split and evaluate validation loss/perplexity at intervals.
4. Add checkpoint resume, random seed control, gradient accumulation, mixed precision, gradient clipping, and learning-rate schedule.
5. Add experiment tracking and hardware utilization reporting.
6. Evaluate on appropriate language, reasoning, coding, multilingual, and safety benchmarks; document contamination controls.
7. Add supervised instruction fine-tuning and preference tuning only after base-model behavior and evaluation are understood.
8. Add efficient inference (KV cache, batching, quantization) and provider integration.

## Compute expectations

A small prototype can run on CPU or a modest GPU with reduced configuration. Useful general language capability requires much larger data and compute. Model size, token count, sequence length, hardware throughput, and training efficiency determine cost. Measure before scaling; do not promise a 1B model or production quality based only on repository structure.
