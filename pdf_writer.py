import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from langchain_core.tools import tool


# latex_content = r"""\documentclass{article}
# \usepackage[utf8]{inputenc}
# \usepackage{amsmath}
# \usepackage{graphicx}
# \title{Exported Paper}
# \author{Auto-generated}
# \date{\today}

# \begin{document}
# \maketitle

# Hello, World! This is a test PDF generated with tectonic.

# \end{document}
# """

@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The LaTeX document content as a string

    Returns:
        Path to the generated PDF document
    """
    if shutil.which("tectonic") is None:
        raise RuntimeError(
            "tectonic is not installed. Install it first on your system."
        )

    try:
        # Step2: Create directory
        output_dir = Path("exported_pdfs").absolute()
        output_dir.mkdir(exist_ok=True)
        # Step3: Setup filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"
        # Step4: Export as tex & pdf
        tex_file = output_dir / tex_filename
        tex_file.write_text(latex_content, encoding='utf-8')

        result = subprocess.run(
                    ["tectonic", tex_filename, "--outdir", str(output_dir)],
                    cwd=output_dir,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )

        # Check if compilation was successful
        if result.returncode != 0:
            error_msg = f"Tectonic compilation failed:\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            print(error_msg)
            return f"Error: LaTeX compilation failed. Check the .tex file at {tex_file}"

        final_pdf = output_dir / pdf_filename
        if not final_pdf.exists():
            error_msg = f"PDF file was not generated.\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            print(error_msg)
            return f"Error: PDF was not generated. Check the .tex file at {tex_file}"

        print(f"Successfully generated PDF at {final_pdf}")
        return str(final_pdf)

    except Exception as e:
        error_msg = f"Error rendering LaTeX: {str(e)}"
        print(error_msg)
        return error_msg
