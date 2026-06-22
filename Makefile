# Build the paper and (re)generate the figures it embeds.
#
#   make             # compile main.pdf (assumes figures/ already populated)
#   make examples    # compile examples.pdf (the short 4-example note)
#   make classification  # compile classification.pdf (the easy/hard-axis note)
#   make edgeworth   # compile edgeworth.pdf (the U-statistic Edgeworth note)
#   make figures     # rerun all numerical experiments -> figures/*.pdf
#   make all         # figures + all documents
#   make clean       # remove LaTeX build artifacts
#   make distclean   # also remove PDFs and figures

.PHONY: all paper examples classification edgeworth figures clean distclean

all: figures paper examples classification edgeworth

paper: main.pdf

examples: examples.pdf

classification: classification.pdf

edgeworth: edgeworth.pdf

main.pdf: main.tex references.bib $(wildcard figures/*.pdf)
	latexmk -pdf -interaction=nonstopmode main.tex

examples.pdf: examples.tex $(wildcard figures/*.pdf)
	latexmk -pdf -interaction=nonstopmode examples.tex

classification.pdf: classification.tex $(wildcard figures/*.pdf)
	latexmk -pdf -interaction=nonstopmode classification.tex

edgeworth.pdf: edgeworth.tex $(wildcard figures/*.pdf)
	latexmk -pdf -interaction=nonstopmode edgeworth.tex

figures:
	cd code && python3 run_all.py

clean:
	latexmk -c main.tex 2>/dev/null || true
	latexmk -c examples.tex 2>/dev/null || true
	latexmk -c classification.tex 2>/dev/null || true
	latexmk -c edgeworth.tex 2>/dev/null || true
	rm -f build.log code/run_log.txt
	rm -rf code/__pycache__

distclean: clean
	rm -f main.pdf examples.pdf classification.pdf edgeworth.pdf
	rm -f figures/*.pdf
