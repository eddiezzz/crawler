from bs4 import BeautifulSoup
import sys

def dfs(root, level, cur_level = 0):
    ret = []
    if cur_level == level:
        ret.append(root)
        return ret
    for child in root.find_all(recursive=False):
        sub_ret = dfs(child, level, cur_level + 1)
        ret = ret + sub_ret
    return ret

def get_all_text(root):
    text = ""
    tags = root.find_all(['p', 'a'])
    for tag in tags:
        text += tag.get_text() + "<br /> "
    return text

class Parser():
    def __init__(self, doc):
        self.doc = doc
        self.new_doc = None
        pass

    def extractText(self):
        soup = BeautifulSoup(self.doc, 'lxml')
        text = ""
        tags = soup.find_all(['title', 'p', 'a'])
        for tag in tags:
            text += tag.get_text() + " "
        soup.decode()
        return text

    def _tripToomanyLevel(self, doc, level = 10):
        soup = BeautifulSoup(doc, 'lxml')
        roots = soup.find_all(recursive=False)
        tags = dfs(roots[0], level)
        for tag in tags:
            parent = tag.find_parent()
            text = get_all_text(tag)
            new_tag = soup.new_tag("p")
            new_tag.string = text
            parent.append(new_tag)
            tag.decompose()
        return soup.decode()

    def _formatImage(self, doc):
        doc = doc.replace('data-src', 'src')
        soup = BeautifulSoup(doc, 'lxml')
        filters = ['image', 'img']
        tags = soup.find_all(filters)
        for tag in tags:
            if tag.has_attr('src'):
                if len(tag['src']) < 5:
                    tag.decompose()
            elif tag.has_attr('data-src'):
                if len(tag['data-src']) < 5:
                    tag.decompose()
            else: 
                tag.decompose()
        return soup.decode()


    def formatForWechat(self):
        new_doc = self._tripToomanyLevel(self.doc)
        new_doc = self._formatImage(new_doc)
        soup = BeautifulSoup(new_doc, 'lxml')
        filters = ['title', 'style', 'script']
        #filters = ['title', 'script']
        tags = soup.find_all(filters)
        for tag in tags:
            tag.decompose()
        return soup.decode()

if __name__ == '__main__':
    fd = open('a_processed.html', 'r')
    doc = fd.read()
    fd.close()
    parser = Parser(doc)
    new_doc = parser.formatForWechat()
    new_fd = open('todo.html', 'w')
    new_fd.write(new_doc.encode('utf8'))
    new_fd.close()
