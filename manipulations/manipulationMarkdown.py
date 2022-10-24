import repackage
repackage.up()
from utils.regularExpressions import *

def markDownToText(text_markdown):
    text_markdown = removeTables(text_markdown)
    text_markdown = removeAsterisk(text_markdown)
    text_markdown = removeBreakPage(text_markdown)
    return text_markdown

def readMarkDownFile(fileMarkDown):
    with open(fileMarkDown, 'r') as file:
        dataFile = file.read()
    return dataFile

def saveMarkdownToText(dataText, fileName):
    with open(fileName, 'w') as file:
        file.write(dataText)

#-----------------
mkfile = readMarkDownFile('manipulations/sampleFile.md')
data = markDownToText(mkfile)
saveMarkdownToText(data, 'exemplomd.txt')


