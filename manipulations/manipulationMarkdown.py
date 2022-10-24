import repackage
repackage.up()
from utils.regularExpressions import *
from bs4 import BeautifulSoup
from markdown import markdown

def markDownToTextBs(text_markdown):
    text_markdown = markdown(text_markdown)
    text_markdown = ''.join(BeautifulSoup(text_markdown, features="html.parser").findAll(text=True))
    text_markdown = removeTables(text_markdown)
    text_markdown = removeBreakPage(text_markdown)
    text_markdown = removeAsterisk(text_markdown)

    return text_markdown

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

def readMarkDownFileMK(fileMarkDown):
    with open(fileMarkDown, 'r') as file:
        release_note = file.read()
        description = bytes(release_note, 'utf-8')
    return description.decode("utf-8")

#-----------------

'''mkfile = readMarkDownFile('manipulations/100024-49203.md')
data = markDownToText(mkfile)
saveMarkdownToText(data, 'exemplomd.txt')'''
'''mk = readMarkDownFileMK('manipulations/samplefile.md')
mk = markDownToTextBs(mk)
saveMarkdownToText(mk, 'exemplomd.txt')'''

