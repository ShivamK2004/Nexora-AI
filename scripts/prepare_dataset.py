import argparse, hashlib, re
from pathlib import Path

def clean(text: str) -> str:
    text=text.replace('\r\n','\n').replace('\r','\n')
    text=re.sub(r'[\t ]+',' ',text)
    text=re.sub(r'\n{3,}','\n\n',text)
    return text.strip()

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    source=Path(a.input); target=Path(a.output); target.parent.mkdir(parents=True,exist_ok=True)
    text=clean(source.read_text(encoding='utf-8',errors='replace'))
    if not text: raise SystemExit('No text remains after cleaning')
    target.write_text(text+'\n',encoding='utf-8')
    print(f'input_chars={source.stat().st_size} output_chars={len(text)} sha256={hashlib.sha256(text.encode()).hexdigest()}')
if __name__=='__main__':main()
