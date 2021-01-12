# -*- coding: utf-8 -*-
import xml.dom.minidom
ELEMENT_NODE = xml.dom.Node.ELEMENT_NODE
class SimpleXmlGetter(object):
    def __init__(self, data):
        if type(data) == str:
            self.root = xml.dom.minidom.parse(data)
        else:
            self.root = data
    def __getattr__(self, name):    #support . operation
        if name == 'data':
            return self.root.firstChild.data
        for c in self.root.childNodes:
            if c.nodeType == ELEMENT_NODE and c.tagName == name:
                return SimpleXmlGetter(c)
    def __getitem__(self, index):    #support [] operation
        eNodes = [ e for e in self.root.parentNode.childNodes
                   if e.nodeType == ELEMENT_NODE and e.tagName == self.root.tagName]
        return SimpleXmlGetter(eNodes[index])
    def __call__(self, *args, **kwargs): #support () openration, for query conditions
        for e in self.root.parentNode.childNodes:
            if e.nodeType == ELEMENT_NODE:
                for key in kwargs.keys():
                    if e.getAttribute(key) != kwargs[key]:
                        break
                else:
                    return SimpleXmlGetter(e)
if __name__ == "__main__":
    x = SimpleXmlGetter("sysd.xml")
    print(x.sysd.sysagent.param[2].data)
    print(x.sysd.sysagent.param(name="querytimeout", type="second").data)