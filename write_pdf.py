# Step1: Install tectonic & Import deps
from langchain_core.tools import tool        # To define the function as a LangChain tool
from datetime import datetime                # For timestamped filenames
from pathlib import Path                     # For handling file paths
import subprocess                            # To run external commands (Tectonic CLI)
import shutil                                # To locate executables

# Set explicit path to Tectonic executable if not found in system PATH
TECTONIC_PATH = shutil.which("tectonic") or r"E:\tectonic-0.15.0+20250814-x86_64-pc-windows-msvc\tectonic.exe"

@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The LaTeX document content as a string

    Returns:
        Path to the generated PDF document
    """
    # Optional check (commented out): Ensure Tectonic is installed
    # if shutil.which("tectonic") is None:
    #     raise RuntimeError(
    #         " tectonic is not installed. Install it first on your system."
    #     )

    # Verify Tectonic path exists; raise error if not found
    if not TECTONIC_PATH or not Path(TECTONIC_PATH).exists():
        raise RuntimeError("Tectonic is not installed or not found in PATH.")

    try:
        # Step2: Create an output directory if it doesn't exist
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)

        # Step3: Create timestamp-based filenames for .tex and .pdf files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"

        # Step4: Write LaTeX content into a .tex file
        tex_file = output_dir / tex_filename
        tex_file.write_text(latex_content)

        # Run Tectonic to compile the LaTeX file into a PDF
        result = subprocess.run(
                    ["tectonic", tex_filename, "--outdir", str(output_dir)],
                    cwd=output_dir,          # Set working directory to output folder
                    capture_output=True,     # Capture stdout/stderr
                    text=True,               # Return output as string instead of bytes
                )

        # Check if PDF file was successfully created
        final_pdf = output_dir / pdf_filename
        if not final_pdf.exists():
            raise FileNotFoundError("PDF file was not generated")

        # Print success message and return the PDF file path
        print(f"Successfully generated PDF at {final_pdf}")
        return str(final_pdf)

    except Exception as e:
        # Print and re-raise any errors during PDF generation
        print(f"Error rendering LaTeX: {str(e)}")
        raise
