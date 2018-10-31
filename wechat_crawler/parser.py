from bs4 import BeautifulSoup

class Parser():
    def __init__(self, doc):
        self.soup1 = BeautifulSoup(doc, 'lxml')
        self.soup2 = BeautifulSoup(doc, 'lxml')
        pass

    def extractText(self):
        styles = self.soup1.find_all('style')
        for style in styles:
            style.decompose()
        return self.soup1.getText().replace('/\s/g','')

    def formatForWechat(self):
        tags = self.soup2.find_all(['script', 'image', 'style', 'link', 'img', 'title'])
        for tag in tags:
            tag.decompose()
        tags = self.soup2.find_all(['p'])
        for tag in tags:
            del tag.attrs
        return self.soup2.decode()

if __name__ == '__main__':
    fd = open('a.html')
    doc = fd.read()
    fd.close()
    parser = Parser(doc)
    new_doc = parser.formatForWechat()
    print new_doc
    new_fd = open('a_processed.html', 'w')
    new_fd.write(new_doc.encode('utf8'))
    new_fd.close()

    text = parser.extractText()
    print text
