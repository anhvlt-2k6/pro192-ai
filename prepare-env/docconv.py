from os import path, walk, makedirs, getcwd
from sys import stderr
from markitdown import MarkItDown

EXTENSIONS = (
    '.pdf', '.docx', '.xlsx', '.pptx',
    '.md', '.markdown', '.adoc', '.asciidoc',
    '.html', '.xhtml', '.csv',
    '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp'
)

OUT_DIR = path.join(getcwd(), 'out')

def find_documents(root_dir):
    for dirpath, dirnames, filenames in walk(root_dir):
        for fname in filenames:
            lower = fname.lower()
            if any(lower.endswith(ext) for ext in EXTENSIONS):
                yield path.join(dirpath, fname)

def export_to_out_path(full_path, out_name):
    md_engine = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
    result = md_engine.convert(full_path)
    out_path = path.join(OUT_DIR, f"{out_name}.md")
    print("Out_path:", out_path)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result.text_content)
    print(f"Written: {out_path}")

if __name__ == "__main__":
    ROOT = r"../../FPT_BIT_SE_RES/S2 - OSG202" # <- Change the directory

    for full_path in find_documents(ROOT):
        rel = path.relpath(full_path, ROOT)
        rel = rel.replace('\\', '/').strip('/')
        safe_name = rel.replace('/', '_').replace(' ', '_')
        export_to_out_path(full_path, safe_name)
