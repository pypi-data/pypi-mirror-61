.. Topoly documentation master file, created by
   sphinx-quickstart on Wed Jan 29 18:30:03 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Topoly
==================================
Topoly is a **Python** package that collects programs useful for **polymer topology** analysis.
List of programs which are included in this module:

* surfaces  - Lasso topology analyzer. Counts how many times tail crosses surface spanned by loop, finds residues closest to the crossing and identifies lasso topology.
* homflylink - HOMFLY polynomial calculator. Finds polynomial invariant and suggests knot topology.
* knot_net - Alexander polynomial calculator.
* Yamada polynomial calculator.
* Polymer structure simplifier which preserves topology.
* polygongen - Lasso generator. Creates .xyz files with coordinates for equilateral lasso or loop polygon.
* Kauffman method for theta-curves.
* knot map picture generator.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started.rst
   installation.rst
   modules.rst
   license.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Contact
==================
.. image:: _static/index_logo_sulk.png
    :width: 100px

Questions should be addressed to Joanna Sułkowska (jsulkowska AT cent.uw.edu.pl)
Any technical difficulties and remarks please report to Bartosz Greń (b.gr AT cent.uw.edu.pl)
