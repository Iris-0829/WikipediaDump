# WikipediaDump

The goal of the project is to crawl all Wikipedia pages from the Wikipedia dump which contain math expressions and convert them to html files in an automated way. 

Before running the code, you will need to install LaTeXML (see https://dlmf.nist.gov/LaTeXML/), BeautifulSoup4 and Python version newer than Python 3.6. (I am using python3.8)

To run the code, type in ```python3.8 main.py```. Each time you run the code, it will automatically check if there are update of the wikipedia dump, and convert all the files if there are newer version. 
