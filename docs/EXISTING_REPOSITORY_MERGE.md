# Merging this package into your existing `nexora-lm` GitHub repository

This ZIP is delivered as a separate folder so your current repository is not overwritten. Review the files before merging them.

## Recommended safe workflow (Windows PowerShell)

```powershell
# 1. Clone your current repository into a separate working directory
git clone https://github.com/shivamkumar130/nexora-lm.git
cd nexora-lm

# 2. Create a safety branch before merging
git switch -c integrate/nexora-ai-v1

# 3. Copy the extracted Nexora-AI-Complete contents into this clone.
#    Use File Explorer or copy selected folders after reviewing existing files.
#    Do not overwrite your existing model/tokenizer/training files without comparing them.

# 4. Inspect exactly what changed
git status
git diff --stat

# 5. Create/activate a Python environment, install dependencies, and test
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m compileall -q backend model scripts tests
python -m unittest discover -s tests -v

# 6. Commit and push the integration branch
git add .
git commit -m "feat: integrate Nexora AI application platform"
git push -u origin integrate/nexora-ai-v1
```

Open a pull request on GitHub and review the diff before merging into `main`. Keep the original repository intact until the integrated branch passes tests.

## Important merge guidance

- Preserve any working custom SentencePiece tokenizer, previous checkpoints, dataset tools, or model layers from your original repository.
- This package's byte tokenizer and toy Transformer live in `model/nexora_lm/`; rename or adapt them if your current code already has those modules.
- Do not commit model weights, private datasets, API keys, `.env`, uploaded documents, or database files.
- Compare dependency versions and Python package names before replacing your current dependency manifest.
- The archive does not push to GitHub or modify your remote repository.
