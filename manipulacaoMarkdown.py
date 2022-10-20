from os import remove
from markdown import markdown
from bs4 import BeautifulSoup
from regularExpressions import removeTextAspose

def markDownToText(text_markdown):
    removeTextAspose(text_markdown)
    text_html = markdown(text_markdown)
    print(text_html)
    #text = ''.join(BeautifulSoup(text_html).findall(text=True))
    return text_html #text

def readMarkDownFile(fileMarkDown):
    with open(fileMarkDown, 'r') as file:
        dataFile = file.read()
    return dataFile