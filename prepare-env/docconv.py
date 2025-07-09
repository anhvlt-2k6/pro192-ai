from os import path, walk, makedirs, getcwd
from sys import stderr
from docling.document_converter import DocumentConverter

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
    makedirs(OUT_DIR, exist_ok=True)

    converter = DocumentConverter()
    try:
        result = converter.convert(full_path)
        markdown = result.document.export_to_markdown()
    except Exception as e:
        print(f"Error converting '{full_path}': {e}", file=stderr)
        return

    out_path = path.join(OUT_DIR, f"{out_name}.md")
    print("Out_path:", out_path)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    print(f"Written: {out_path}")

if __name__ == "__main__":
    ROOT = r"../../FPT_BIT_SE_RES/S2 - OSG202"

    for full_path in find_documents(ROOT):
        rel = path.relpath(full_path, ROOT)
        rel = rel.replace('\\', '/').strip('/')
        safe_name = rel.replace('/', '_').replace(' ', '_')
        export_to_out_path(full_path, safe_name)
