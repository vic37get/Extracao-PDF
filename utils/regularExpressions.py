import re

def removeTextAspose(text):
    remove_aspose = re.compile('(Created.*\/)')
    text = re.sub(remove_aspose, '', text)
    return text
