# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 01:42:00 2018

@author: Prashant
"""
import os
import sys

import mistune
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5 import uic
from PyQt5.uic import loadUi

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

class Output(QDialog):
    def __init__(self,html):
        super(Output, self).__init__()
        loadUi('ui/output.ui', self)
        self.output.setHtml(html)
        self.show()

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
        self.filename = "untitled.md"
        self.path = "./"

        super(MainApp, self).__init__()
        uic.loadUi('ui/editor.ui', self)
        self.setWindowTitle(self.filename + ' - Markdown Editor')
        self.show()

        self.instant_run_icon.clicked.connect(self.instant_run)

        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_As.triggered.connect(self.save_as)
        self.actionClose.triggered.connect(self.close_file)
        self.actionExit.triggered.connect(self.quit)

        self.actionSave_HTML.triggered.connect(self.save_html)

        self.actionReadme_Tamplate.triggered.connect(self.readme_insert)
        self.actionText_Styling_Template.triggered.connect(self.style_insert)
        self.actionMarkdown_Guide_Template.triggered.connect(self.guide_insert)

        self.actionRun.triggered.connect(self.run)
        self.actionInstant_Run.triggered.connect(self.instant_run)
        self.actionShow_Preview.triggered.connect(self.hidesmalloutput)
        self.hidesmalloutput()

    def readme_insert(self):
        self.close_file()
        self.__open_file_with_path("tamplate_readme.md")
    def style_insert(self):
        self.close_file()
        self.__open_file_with_path("tamplate_style.md")
    def guide_insert(self):
        self.close_file()
        self.__open_file_with_path("tamplate_guide.md")

    def new_file(self, ctn=" "):
        path, ext = QFileDialog.getSaveFileName(self, "Create a new File", "", "Markdown File (*.md);;RST File (*.rst);;Text File (*.txt);")
        if path:
            if ext == "Markdown File (*.md)":
                ext = ".md"
            elif ext == "RST File (*.rst)":
                ext = ".rst"
            elif ext == "Text File (*.txt)":
                ext = ".txt"
            else:
                ext = path.split('.')[-1]
            self.filename = path.split('/')[-1]
            self.path = "/".join(str(i) for i in path.split('/')[:-1]) + "/"
            self.label.setText(self.path + self.filename)
            if ctn:
                self.markdown.setPlainText(str(ctn))
            else:
                self.markdown.setPlainText("")
            self.setWindowTitle(self.filename + ' - Markdown Editor')
            self.save()

    def __open_file_with_path(self, path):
        try:
            f = open(path, 'r')
            self.markdown.setPlainText(f.read())
            f.close()
        except Exception as e:
            print(e)

    def open_file(self):
        path, ext = QFileDialog.getOpenFileName(self, "Open File", "", "Markdown File (*.md);;RST File (*.rst);;Text File (*.txt);;All Files (*);")
        if path:
            self.path = "/".join(str(i) for i in path.split('/')[:-1]) + "/"
            self.filename = path.split('/')[-1]
            self.__open_file_with_path(self.path + self.filename)
            self.label.setText(self.path + self.filename)
            self.setWindowTitle(self.filename + ' - Markdown Editor')

    def save_html(self):
        md_script = self.markdown.toPlainText()
        renderer = HighlightRenderer()
        markdown = mistune.Markdown(renderer=renderer)
        html = markdown(md_script)
        path, ext = QFileDialog.getSaveFileName(self, "Open File", "", "HTML File (*.html);;All Files (*);")
        if path:
            f = open(path, 'w+')
            f.write(html)
            f.close()

    def close_file(self):
        self.filename = "untitled.md"
        self.path = "./"
        self.label.setText(' ')
        self.markdown.setPlainText(" ")
        self.setWindowTitle(self.filename + ' - Markdown Editor')

    def save(self):
        if self.filename == "untitled.md":
            self.save_as()
        else:
            self.label.setText(self.path + self.filename)
            self.setWindowTitle(self.filename + ' - Markdown Editor')
            f = open(self.path + self.filename, 'w+')
            f.write(self.markdown.toPlainText())
            f.close()

    def save_as(self):
        self.new_file(self.markdown.toPlainText())

    def quit(self):
        self.close()

    def instant_run(self):
        md_script = self.markdown.toPlainText()
        renderer = HighlightRenderer()
        markdown = mistune.Markdown(renderer=renderer)
        html = markdown(md_script)
        self.output.setHtml(html)

    def hidesmalloutput(self):
        if self.actionShow_Preview.isChecked():
            self.instant_run_icon.show()
            self.output.show()
        else:
            self.instant_run_icon.hide()
            self.output.hide()

    def run(self):
        md_script = self.markdown.toPlainText()
        renderer = HighlightRenderer()
        markdown = mistune.Markdown(renderer=renderer)
        html = markdown(md_script)

        dialog = Output(html)
        dialog.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())