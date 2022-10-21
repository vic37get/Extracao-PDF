from markdown import markdown
from bs4 import BeautifulSoup
import re

def markDownToText(text_markdown):
    html = markdown(text_markdown)
    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)
    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))
    print(text)
    return text

def readMarkDownFile(fileMarkDown):
    with open(fileMarkDown, 'r') as file:
        dataFile = file.read()
    return dataFile

def saveMarkdownToText(dataText, fileName):
    with open(fileName, 'w') as file:
        file.write(dataText)

mkfile = readMarkDownFile('manipulations/sampleFile.md')
data = markDownToText(mkfile)
saveMarkdownToText(data, 'exemplomd.txt')


