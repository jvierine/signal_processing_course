all:
	pdflatex signal_processing.tex
	bibtex signal_processing
	pdflatex signal_processing.tex

figures:
	cd ch03/code ; python3 ex3.6.py noplot

clean:
	rm -f signal_processing.aux  signal_processing.bbl  signal_processing.blg  signal_processing.idx signal_processing.ilg signal_processing.ind signal_processing.log signal_processing.out signal_processing.toc
	rm -f signal_processing.pdf
