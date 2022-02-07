import os

def convert_to_html(file_name:str):
    with open(file_name, 'w') as f:
        content = f.read().replace("\n", "")
        page_title = file_name[:file_name.find('.')] + "_html"
        os.system(
            'var="' + content + '" && printf \'%s\n\' \"$var\" | node node_modules/parsoid/bin/parse.js > result/' + page_title + '.html')
