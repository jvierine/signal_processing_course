all:
	pdflatex signal_processing.tex
	bibtex signal_processing
	pdflatex signal_processing.tex
	bibtex signal_processing

figures:
	cd ch02/code ; python3 ex2_2.py noplot
	cd ../..
	cd ch03/code ; python3 ex3.6.py noplot
	cd ../..
	cd ch04/code ; python3 ex4.7.py noplot ; python3 ex4.8.py noplot
	cd ../..
	cd ch06/code ; python3 ex6.1.py noplot ; python3 ex6.6.py noplot
	cd ../..
	cd ch07/code ; python3 ex7_3a.py noplot ; python3 ex7_3b.py noplot ; python3 ex7_3c.py noplot
	cd ../..
	cd ch10/code ; python3 ex10_2g.py noplot ; python3 ex10_3.py noplot
	cd ../..
	cd ch11/code ; python3 ex11_1.py noplot ; python3 ex11_2.py noplot ; python3 ex11_3.py noplot
	cd ../..
	cd ch13/code ; python3 ex13_2.py noplot
	cd ../..
	cd ch14/code ; python3 ex14_1.py noplot
	cd ../..
	cd ch16/code ; python3 ex16_1b.py noplot ; python3 ex16_1c.py noplot
	cd ../..
	cd ch17/code ; python3 ex17_1.py noplot ; python3 ex17_1a.py noplot ; python3 ex17_1b.py noplot
	cd ../..
	cd ch18/code ; python3 ex18_2.py noplot ; python3 ex18_3.py noplot ; python3 ex18_4.py noplot
	cd ../..
	cd ch19/code ; python3 ex19_5.py noplot
	cd ../..

clean:
	rm -f signal_processing.aux  signal_processing.bbl  signal_processing.blg  signal_processing.idx signal_processing.ilg signal_processing.ind signal_processing.log signal_processing.out signal_processing.toc
	rm -f signal_processing.pdf
