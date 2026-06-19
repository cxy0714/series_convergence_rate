# Build the paper and (re)generate the figures it embeds.
#
#   make            # compile main.pdf (assumes figures/ already populated)
#   make figures    # rerun all numerical experiments -> figures/*.pdf
#   make all        # figures + paper
#   make clean      # remove LaTeX build artifacts
#   make distclean  # also remove main.pdf and figures

.PHONY: all paper figures clean distclean

all: figures paper

paper: main.pdf

main.pdf: main.tex references.bib $(wildcard figures/*.pdf)
	latexmk -pdf -interaction=nonstopmode main.tex

figures:
	cd code && python3 run_all.py

clean:
	latexmk -c main.tex 2>/dev/null || true
	rm -f build.log code/run_log.txt
	rm -rf code/__pycache__

distclean: clean
	rm -f main.pdf
	rm -f figures/*.pdf
