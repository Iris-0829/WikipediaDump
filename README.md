# WikipediaDump

The goal of the project is to crawl all Wikipedia pages from the Wikipedia dump which contain math expressions and convert them to html files in an automated way. 

Before running the code, you will need to install LaTeXML (see https://dlmf.nist.gov/LaTeXML/), BeautifulSoup4 and Python version newer than Python 3.6. (I am using python3.8)

## Running main 

The usage of the test function is `main.py [-h] [-v VERBOSE] [-l LOCATION] [-r RESULT] [-n NAME NAME] [-d DATE]`

`-h` shows help messages. 

`-v` or `--verbose` shows more informative output. The expected argument is 1, 2, or 3. 

`-l` or `--location` sets the location of downloaded dump files. 

`-r` or `--result` sets the location of result files after conversion. 

`-n` or `--name` sets the name and index of the dump file. 

`-d` or `--date` sets the date of the dump file. 

For example,

`python3.8 main.py` will create "dump/" and "result/" by default. The code downloads first 100 pages and index in the latest dump by default. 

`python3.8 main.py --location newdump --result newresult --name enwiki-20211001-pages-articles-multistream1.xml-p1p41242.bz2 enwiki-20211001-pages-articles-multistream-index1.txt-p1p41242.bz2 --date 20211001` will create directory newdump and newresult, and download first 100 pages and index in 20211001's dump.


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

For example,  

```python3.8 convert_html.py test/Albedo.html```


will print corresponding HTML on stdout. 

```python3.8 convert_html.py test/Albedo.html > test4.html```

will save the output as html file. 


You can also call `convert_to_html` directly. 
