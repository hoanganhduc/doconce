#!/usr/bin/env python
#
# (c) Ilya V. Schurov <ilya@schurov.com>, 2016
# Based on example_and_colorbox example by Hans Petter Langtangen
# Licensed under BSD 3-Clause License (like the rest of DocOnce, see LICENSE)
#
# -*- coding: utf-8 -*-
from mako.template import Template
from doconce.latex import aux_label2number
import re

def proof(text, titleline, counter, format):
	s = r"""
\begin{proof}%s
""" % titleline
	s += r"""
%s

\end{proof}
""" % text
	return s

def do_proof(text, titleline, counter, format):
	if titleline:
		s = r"""
__Proof %s.__
%s
""" % (titleline, text)
	else:
		s = r"""
__Proof.__
%s
""" % text
	return s
	
def tables(text, titleline, counter, format):
	label, titleline = get_label(titleline)
	titleline = titleline.strip()
	s = r"""
\begin{table}
\begin{center}

%s

\end{center}
\caption{%s}
label{%s}
\end{table}
""" % (text, titleline, label)
	return s
	
def html_tables(text, titleline, counter, format):
	label, titleline = get_label(titleline)
	titleline = titleline.strip()
	label2number = aux_label2number()
	no = label2number[label]
	s = r"""
<!-- custom environment: label=%s, number=%s -->
<br />
<center>
<p> Table %s: %s </p>
%s
</center>
<br />
""" % (label, no, no, titleline, text)
	return s

envir2format = {
    'intro': {
        'latex': u"""
%\\usepackage{amsthm}
%\\theoremstyle{definition}
%\\newtheorem{remark}{Remark}
%\\newtheorem{example}{Example}
%\\newtheorem{definition}{Definition}
""",},
	'proof': {
		'latex': proof,
		'do': do_proof,
	},
	'tables': {
		'latex': tables,
		'html': html_tables,
	},
}

envirs = ['proposition', 'lemma', 'theorem', 'claim']
for env in envirs:
    envir2format.update({
        env: {
            'latex': lambda text, titleline, counter, format, env=env: latex_env(env, text, titleline, counter, format),
            'do': lambda text, titleline, counter, format, env=env: do_env(env, text, titleline, counter, format),
            'html': lambda text, titleline, counter, format, env=env: html_env(env, text, titleline, counter, format),
        },
    })

def get_label(titleline):
    """
    Extract label from title line in begin environment.
    Return label and title (without label).
    """
    label = ''
    if 'label=' in titleline:
        pattern = r'label=([^\s]+)'
        m = re.search(pattern, titleline)
        if m:
            label = m.group(1)
            titleline = re.sub(pattern, '', titleline).strip()
    return label, titleline

def latex_env(env, text, titleline, counter, format):
    """LaTeX typesetting of theorem-style environment."""
    label, titleline = get_label(titleline)
    titleline = titleline.strip()
    template = ur"""
\begin{${env}}${titleline}
% if label:
label{${label}}
% endif
${text}
\end{${env}}
"""
    return Template(template).render(**vars())

def do_env(env, text, titleline, counter, format):
    """General typesetting of theorem-style environment via a section."""
    label, titleline = get_label(titleline)
    titleline = titleline.strip()
    label2number = aux_label2number()
    no = label2number[label]
    template = ur"""
===== ${env.capitalize()} ${no} ${titleline} =====
% if label:
label{${label}}
% endif
${text}

"""
    return Template(template).render(**vars())

def html_env(env, text, titleline, counter, format):
    """HTML typesetting of theorem-style environment."""
    label, titleline = get_label(titleline)
    titleline = titleline.strip()
    label2number = aux_label2number()
    no = label2number[label]
    template = ur"""
% if label:
<!-- custom environment: label=${label}, number=${no} -->
% endif
% if titleline:
<p class='env-${env}'><strong>${env.capitalize()} ${no} ${titleline}.</strong> 
% else:
<p class='env-${env}'><strong>${env.capitalize()} ${no}.</strong>
% endif 
${text}
</p>
"""
    return Template(template).render(**vars())

