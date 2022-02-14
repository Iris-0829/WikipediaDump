# WikipediaDump

The goal of the project is to crawl all Wikipedia pages from the Wikipedia dump which contain math expressions and convert them to html files in an automated way. 

Before running the code, you will need to install LaTeXML (see https://dlmf.nist.gov/LaTeXML/), BeautifulSoup4 and Python version newer than Python 3.6. (I am using python3.8)


## Running test

The usage of the test function is `test.py [-h] [-v] dir dir`

Two `dir` are the argument for the path of directory with generated files and the path of directory with expected files. 

`-v` and `--verbose` is to show more informative output, which displays the difference between files line by line. 

For example, run 


```python3.8 test.py result/ test/ -v```


to compare the result in `result/` and `test/` with detailed output. 

## Conversion from WikiText to HTML

The usage of the conversion function is `convert_html.py path`

`path` argument is the path of input WikiText. 

For example, run 

```python3.8 convert_html.py example.txt```


will print corresponding HTML on stdout. You can also call `convert_to_html` directly. 
