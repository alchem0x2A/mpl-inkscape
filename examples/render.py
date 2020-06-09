############################################################
# A simple cmd tool to convert Inkscape-flavor svg --> pdf #
############################################################
from pathlib import Path
from subprocess import run
from argparse import ArgumentParser


def svg_to_pdftex(fname):
    # fname ends with .svg
    fname = Path(fname)
    if fname.suffix not in (".svg", ".svgz"):
        raise NameError("File must end in .svg")
    cmd = "inkscape --export-latex --export-filename={fnew} {fname}".format(
        fnew=fname.with_suffix(".pdf").as_posix(),
        fname=fname.as_posix())
    ec = run(cmd, shell=True)
    return ec


def compound_tex(fname):
    # fname ends with .svg
    fname = Path(fname)
    if fname.suffix not in (".svg", ".svgz", "pdf_tex"):
        raise NameError("File ending error")
    tex_header = ("\\documentclass[size=8pt, paper=A4]{article}\n"
                  "\\usepackage{fontspec}\n"
                  "\\usepackage{amsmath}\n"
                  "\\usepackage{graphicx}\n"
                  "\\usepackage{transparent}\n"
                  "\\usepackage{import}\n"
                  "\\usepackage{xcolor}\n"
                  "\\usepackage[active, graphics, floats, tightpage]{preview}\n"
                  "\\begin{document}\n")

    tex_footer = "\\end{document}"

    figure_env = ("\\begin{{figure}}\n"
                  "\\centering\n"
                  "\\import{{{parent}}}{{{filename}}}\n"
                  "\\end{{figure}}\n")

    s = tex_header
    s += figure_env.format(parent=fname.parent.resolve().as_posix() + "/",
                           filename=fname.with_suffix(".pdf_tex").name)
    s += tex_footer

    with open(fname.with_suffix(".rendered.tex"), "w") as f:
        f.write(s)
    ftex = fname.with_suffix(".rendered.tex")
    ftarget = fname.with_suffix(".rendered.pdf")
    return ftex, ftarget


def render(fname):
    if fname.suffix not in (".tex"):
        raise NameError("File must end in .tex")
    # Render TeX
    cmd = ("latexmk -pdf -quiet -pdflatex=\"lualatex "
           "-interaction=nonstopmode\" -cd {fname}"
           .format(fname=fname.as_posix()))
    ec = run(cmd, shell=True)
    # Convert to png only for demo
    cmd2 = ("convert  -density 300x300 -units pixelsperinch"
            " {pdf} {png}".format(pdf=fname.with_suffix(".pdf").as_posix(),
                                  png=fname.with_suffix(".png").as_posix()))
    ec2 = run(cmd2, shell=True)
    return ec


def main():
    parser = ArgumentParser()
    parser.add_argument("filename",
                        help="SVG file to convert")
    args = parser.parse_args()
    fname = Path(args.filename)
    svg_to_pdftex(fname)
    ftex, fpdf = compound_tex(fname)
    render(ftex)


if __name__ == "__main__":
    main()
