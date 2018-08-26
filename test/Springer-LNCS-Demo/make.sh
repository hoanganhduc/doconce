#!/bin/sh

name=main

if [ "$1" = "pdf" ]; then
	doconce format latex $name --latex_style=Springer_llncs --latex_title_layout=Springer_llncs --latex_preamble=preamble.tex
	doconce ptex2tex $name
	doconce replace "\includegraphics[width=1.0\linewidth]" "\includegraphics[scale=0.7]" $name.tex
	doconce replace "\bibliography{papers}" "\bibliography{references}" $name.tex
	doconce replace "\bibliographystyle{plain}" "\bibliographystyle{splncs}" $name.tex
	doconce replace "\paragraph{Acknowledgement.}" "\subsubsection*{Acknowledgement.}" $name.tex
	for sect in "Graph notation" "Notation for {\sc Sliding Token}"
	do # No section numbering for the above sections
		doconce replace "\subsection{$sect}" "\subsection*{$sect}" $name.tex
	done
	latex $name.tex
	bibtex $name
	latex $name.tex
	dvips $name.dvi
	ps2pdf $name.ps
fi

if [ "$1" == "html" ]; then
	doconce format html $name --html_output=index --html_template=template.html --encoding=utf-8 --section_numbering=on --replace_ref_by_latex_auxno=$name.aux
	for prob in "satisfiability" "independent set" "Sliding Token" "vertex-colouring" "matching" "clique" "yes" "no" "CheckConfined"
	do
	doconce replace "{\sc $prob}" "<span style='font-variant:small-caps;'>$prob</span>" index.html
	done
	doconce replace "\figurename" "<b>Fig.</b>" index.html
	doconce replace "[$\circ$]" "" index.html
	doconce replace "[$\bullet$]" "" index.html
	doconce replace "[(" "(" index.html
	doconce replace ")]" ")" index.html
	doconce replace "[{" "[" index.html
	doconce replace "}]" "]" index.html
fi
