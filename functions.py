from bs4 import BeautifulSoup
from bs4 import Comment
import re

def striphtml(data):
    p = re.compile(r'<.*?>')    
    return p.sub('', data)

def cleanMe(html):
    soup = BeautifulSoup(html) # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    for ch in ['\\a','\\b', '\\t', '\\n', '\\v', '\\f', '\\r', '\\xe2', '\\x80', '\\xc2', '\\xb7', '\\x9c', '\\x9d', '\\x93']:
        if ch in text:
            text=text.replace(ch,"")
    text = re.sub(r'(.*)/USEPA/US@EPA',r'', text)
    text = re.sub(r'[^\x00-\x7f]',r'', text)
    bad_chars = ['https://', 'http://', ':', ';', ',', '*', '\'', '\"', '\\', '/']
    rx = '[' + re.escape(''.join(bad_chars)) + ']'
    text = re.sub(rx, '', striphtml(text))

    return text
