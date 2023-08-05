# rho-pdf-diff

Package forked from https://github.com/JoshData/pdf-diff

## Installation
This package relies on the system dependency `pdftotext`.  After that is 
installed, simply install using `setup.py` with `pip install -e .[dev,test].

## Usage
### Script
There is an included script for generating a text diff between two PDF 
documents, `rho-pdf-diff`.  The simplest usage is:

`rho-pdf-diff <old-pdf-path> <new-pdf-path> <output-path>`

To see additional options run `rho-pdf-diff --help`.  There are a number of 
flags for disabling some filters which attempt to remove unimportant diffs.

### Library
The main workflow for creating diff images from raw documents can be found in 
the source of the `rho-pdf-diff` script.  This essentially involves creating a 
`Document` object for both of the old and new PDFs, and passing these to 
initialize a `DiffResult`.  `DiffResult` also can take a sequence of 
`DiffFilter` objects, which are essentially rules for using information 
available at the `Document` level for removing unwanted diffs from being 
included in the final result.

After the text diff is created by the logic in `DiffResult`, a searchable PDF
containing the side-by-side documents with diffs marked is generated using the 
`DiffImageWriter` class.  Note: the page alignment step is currently *very* slow
for long documents with many diffs.

