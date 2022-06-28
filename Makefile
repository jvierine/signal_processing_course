all:
	pdflatex signal_processing.tex
	bibtex signal_processing
	pdflatex signal_processing.tex

clean:
	rm -f signal_processing.aux  signal_processing.bbl  signal_processing.blg  signal_processing.idx signal_processing.ilg signal_processing.ind signal_processing.log signal_processing.out signal_processing.toc
	rm -f signal_processing.pdf
