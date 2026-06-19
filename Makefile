# Build the paper and (re)generate the figures it embeds.
#
#   make            # compile main.pdf (assumes figures/ already populated)
#   make examples   # compile examples.pdf (the short 4-example note)
#   make figures    # rerun all numerical experiments -> figures/*.pdf
#   make all        # figures + both documents
#   make clean      # remove LaTeX build artifacts
#   make distclean  # also remove PDFs and figures

.PHONY: all paper examples figures clean distclean

all: figures paper examples

paper: main.pdf

examples: examples.pdf

main.pdf: main.tex references.bib $(wildcard figures/*.pdf)
	latexmk -pdf -interaction=nonstopmode main.tex

examples.pdf: examples.tex $(wildcard figures/*.pdf)
	latexmk -pdf -interaction=nonstopmode examples.tex

figures:
	cd code && python3 run_all.py

clean:
	latexmk -c main.tex 2>/dev/null || true
	latexmk -c examples.tex 2>/dev/null || true
	rm -f build.log code/run_log.txt
	rm -rf code/__pycache__

distclean: clean
	rm -f main.pdf examples.pdf
	rm -f figures/*.pdf
