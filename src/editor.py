# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 01:42:00 2018

@author: Prashant
"""

import mistune
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5 import uic
import sys


from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre style="background:#d7d9dd;"><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter(linenos=True, cssclass="source")
        
        return "<style>"+formatter.get_style_defs()+"</style>"+highlight(code, lexer, formatter)

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        uic.loadUi('ui/markdown_editor.ui', self)
        self.show()
        self.setWindowTitle('Markdown Editor :: filename.md')
        self.move(50, 50)
        self.actionExit.triggered.connect(self.quit)
        self.actionRun.triggered.connect(self.rander)

    def quit(self):
        self.close()

    # def copy():
    #     self.markdown.clipboard_clear()
    #     self.markdown.clipboard_append(self.markdown.selection_get()) 

    # def paste():
    #     try:
    #         teext = self.markdown.selection_get(selection='CLIPBOARD')
    #         text.insert(INSERT, teext)
    #     except:
    #         pass

    def rander(self):
        md_script = self.markdown.toPlainText()
        renderer = HighlightRenderer()
        markdown = mistune.Markdown(renderer=renderer)
        html = markdown(md_script)
        self.output.setHtml(html)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())