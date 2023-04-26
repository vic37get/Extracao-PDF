import re

def removeTables(text):
    remove_tables = re.compile('(\|.*\|)')
    text = re.sub(remove_tables, '', text)
    return text

def removeBreakPage(text):
    remove_breakPage = re.compile('(---)')
    text = re.sub(remove_breakPage, '', text)
    return text

def removeAsterisk(text):
    remove_asterisk = re.compile('(\*)')
    text = re.sub(remove_asterisk, '', text)
    return text