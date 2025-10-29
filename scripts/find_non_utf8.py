import os

root = r"c:\Users\kanis\Documents\personal-projects\streamlit-ml-observability"
skip_dirs = {'.venv', 'venv', '__pycache__', '.git'}
errors = []

for dirpath, dirs, files in os.walk(root):
    # mutate dirs in-place to skip certain folders
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for fname in files:
        if not fname.endswith('.py'):
            continue
        path = os.path.join(dirpath, fname)
        try:
            with open(path, 'rb') as fh:
                data = fh.read()
            data.decode('utf-8')
        except UnicodeDecodeError as e:
            print(f"BAD: {path} -> {e}")
            pos = e.start
            start = max(0, pos - 40)
            end = min(len(data), pos + 40)
            snippet = data[start:end]
            print("Hex around pos:", snippet.hex())
            # show a latin-1 decoded preview (lossless single-byte mapping)
            try:
                print("Preview (latin-1):", snippet.decode('latin-1'))
            except Exception:
                pass
            print('-' * 60)
            errors.append(path)

if not errors:
    print("No non-UTF-8 .py files found")
else:
    print(f"Found {len(errors)} file(s) with decode errors")
