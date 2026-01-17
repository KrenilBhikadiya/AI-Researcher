import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from langchain_core.tools import tool


latex_content = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{graphicx}
\title{Exported Paper}
\author{Auto-generated}
\date{\today}"""


# create a directory for exported PDFs
export_dir = Path("exported_pdfs").absolute()
export_dir.mkdir(exist_ok=True)

# create unique filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
tex_file = export_dir / f"paper_{timestamp}.tex"
pdf_file = export_dir / f"paper_{timestamp}.pdf"

# export as TEX and PDF
tex_file.write_text(latex_content)