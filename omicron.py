#!/usr/bin/python
import sys,mechanize,os, socket, platform
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebKitWidgets import *
from datetime import datetime

__version__ = "1.0.0"
HomeURL = "file:///usr/share/kali-defaults/web/homepage.html"
head = ["Omicron"]
#Showing time
def tt():
    t = datetime.now()
    h,m,s = t.hour, t.minute, t.second
    h,m,s = str(h), str(m), str(s)
    tt = h+"."+m+"."+s
    return tt
def fav(url):
    browser = mechanize.Browser()
    page = browser.open(url)
    source_code = page.readlines()
    for favicon in source_code[:]:
        if "favicon" in favicon:
            favicon = favicon.strip("\n")
            favicon = favicon.split(" ")
            for i in range(len(favicon)):
                if favicon[i].startswith("href"):
                    fav = favicon[i].split("=")
                    fav = fav[1].strip('"')
                    return fav
def url_to_path_dir(url):
    if url.startswith("file"):
        path = url.split(":")
        path = path[1]
        path = "/" + path.strip("//")
        path = path.split("/")
        path.pop(len(path)-1)
        path = "/".join(path) + "/"
        return path
    elif url.startswith("http") or url.startswith("https"):
        path = url.split("/")
        main = path[2]
        path = main + "/"
        #path = path.strip("//") + "/"
##        path = path.split("/")
##        path.pop(len(path)-1)
##        path = "/".join(path) + "/"
        return path
def pingSweep(url):
    ip = socket.getfqdn(url)
    oper = platform.system()
    if oper == "Windows":
        ping = "ping -n "+"1"+" "
        comm = ping+addr
        resp = os.popen(comm)
        inf = resp.readlines()
        print inf
    elif oper == "Linux":
        ping = "ping -c "+"1"+" "
        comm = ping+addr
        resp = os.popen(comm)
        inf = resp.readlines()
        print inf
    else:
        ping = "ping -c "+"1"+" "
        comm = ping+addr
        resp = os.popen(comm)
        inf = resp.readlines()
        print inf
    if inf[:] == []:
        print "Unable to Connect"
        return False
    else:
        print "Connection OK"
        return True
class TabNav(QWidget):
    def __init__(self, url, q):
        super(QWidget, self).__init__()
        self.window = QMainWindow(self)
        self.layout = QVBoxLayout()
        self.browser = QWebView()
        #plugins
        self.browser.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebSettings.JavascriptEnabled, True)  
                
        self.browser.setUrl(QUrl(url))
        #Initialize tab screen
        self.tabs = q       
        #Create tab 1
        self.newtab = QWidget()
        #Add tab 1
        self.browser.urlChanged.connect(self.update_urlbar)
        #Create content of tab 1
        self.newtab.layout = QVBoxLayout(self)
        ##Navigation ToolBar
        navtb = QToolBar("NAVIGATION")
        self.window.setIconSize(QSize(15, 15))
        self.window.addToolBar(navtb)
        self.newtab.layout.addWidget(navtb)
        ##Back Button
        back_btn = QAction(QIcon("icons/leftbs.png"), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)
        back_btn.triggered.connect(self.browser.back)
        ##Forward Button
        next_btn = QAction(QIcon("icons/rightb.png"), "Foward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)
        next_btn.triggered.connect(self.browser.forward)
        ##Reload Button
        reload_btn = QAction(QIcon("icons/updater.png"), "Reload", self)
        reload_btn.setStatusTip("Reload Current Page")
        reload_btn.setShortcut("Ctrl+R")
        navtb.addAction(reload_btn)
        reload_btn.triggered.connect(self.browser.reload)
        ##Home Button
        home_btn = QAction(QIcon("icons/home.png"), "Home", self)
        home_btn.setStatusTip("Home Page")
        navtb.addAction(home_btn)
        home_btn.triggered.connect(self.navigate_home)
        
        navtb.addSeparator()
        #Secure
        self.secure_site = QLabel()
        self.secure_site.setStatusTip("Security Levels of The Site")
        self.secure_site.setPixmap(QPixmap("icons/globe.svg").scaled(14,14))
        navtb.addWidget(self.secure_site)        
        navtb.addSeparator()
        ##Serv Indicator
        self.serv_icon = QLabel()
        self.serv_icon.setStatusTip("Show Site Information")
        self.serv_icon.setPixmap(QPixmap("icons/notice.svg").scaled(14,14))
        navtb.addWidget(self.serv_icon)
        ##URL Search Bar
        self.urlbar = QLineEdit()
        font = self.urlbar.font()
        font.setPointSize(9)
        self.urlbar.setFont(font)#self.urlbar.resize(30000,5)
        ##Completer
##        names = ["George", "Marcus", "Samantha", "Maria", "Steven"]
##        completer = QCompleter(names)
##        self.urlbar.setCompleter(completer)
        self.urlbar.setPlaceholderText("Search with DuckDuckGo or enter url/address")
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)#self.browser.load(self, QUrl url)
        ##ComboBox
        self.search_engine = QComboBox()
        self.search_engine.addItem(QIcon(), "Yandex")
        self.search_engine.addItem(QIcon(), "DuckDuckGo")
        self.search_engine.addItem(QIcon("icons/google.png"), "Google")
        self.search_engine.addItem(QIcon("icons/google+.png"), "Google+")
        self.search_engine.addItem(QIcon("icons/twitter.png"), "Twitter")
        self.search_engine.addItem(QIcon("icons/github-64.png"), "GitHub")
        self.search_engine.addItem(QIcon("icons/youtube.jpg"), "YouTube")
##        self.search_engine.currentTextChanged.connect(self.searchEngine)
        navtb.addWidget(self.search_engine)
        ##Stop Loading Button
        stop_btn = QAction(QIcon(os.path.join('icons', 'close_popup.svg')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        navtb.addSeparator()
        bookmark = QAction(QIcon("icons/bookmark_add.png"), "Bookmark This Page (Ctrl+D)", self)
        bookmark.setShortcut("Ctrl+D")
        bookmark.setStatusTip("Bookmark This Page")
        navtb.addAction(bookmark)
        navtb.addSeparator()
        
        navtb.addSeparator()        
        ##Browser Page
        self.newtab.layout.addWidget(self.browser)
        self.newtab.setLayout(self.newtab.layout)
        #Add tabs to widget
        self.layout.addWidget(self.tabs)
        #self.setLayout(self.layout)
    def linkError(self,url):
        h1 = "\tFile Not Found"
        h2 = "Omicron can't find the file at "+str(url)
        h3 = "\n-Check the file name for capitalization or other typing errors.\n"
        h4 = "-Check to see if the file was moved, renamed or deleted.\n"
        h5 = "\t\tTry Again?"
        mess = h1+"\n"+h2+h3+h4+h5
        print h1
        buttonReply = QMessageBox.question(self, "Problem Loading Page", mess, QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            print('Affirmative Exit Confirmed')
            self.browser.setUrl(QUrl(url))
    def update_urlbar(self, query):
        print query.scheme(),"url: ",query.toString()
        serv = query.scheme()
        if serv == "https":
            self.serv_icon.setPixmap(QPixmap("icons/lock-ssl.png"))
            self.secure_site.setPixmap(QPixmap("icons/ok.svg"))
        elif serv == "http":
            self.serv_icon.setPixmap(QPixmap("icons/lock-nossl.png"))
            self.secure_site.setPixmap(QPixmap("icons/warning.svg").scaled(13,13))
        elif serv == "file":
            self.serv_icon.setPixmap(QPixmap("icons/notice.svg").scaled(14,14))
            self.secure_site.setPixmap(QPixmap("icons/question.png"))
        #Change Title and Tab Title
        url = query.toString()
        browser = mechanize.Browser()
        try:
            page = browser.open(url)
            print "Works"
            #self.browser.setUrl(QUrl(url))
            self.newtab.layout.addWidget(self.browser)
        except mechanize.URLError:
            if serv == "https" or serv == "http":
                print "Is Soo True"
                url = query.toString()
                print "Pinga",url
                print "Cant Open"
                flav = QIcon("icons/warning.png")
                i = self.tabs.addTab(self.newtab, flav, "Unable To Connect")
                self.tabs.setCurrentIndex(i)
        else:
            #Getting Tab Title
            source = page.read()
            if "<title>" in source:
                if 'rel="icon"' and "favicon" in source:
                    favref = fav(url)
                    print "[+] Favicon",favref
                    favref = str(url_to_path_dir(url)) + favref
                    favicon = QIcon(favref)
                else:
                    print "[-] No Favicon"
                    favicon = QIcon("")
                st = source.index("<title>")
                en = source.index("</title>")
                line = source[st+7:en]
                print "\t\tTitle:",line
                app_title = line + " - Omicron"
                #self.setWindowTitle(app_title)
                i = self.tabs.addTab(self.newtab, favicon, line)
                self.tabs.setCurrentIndex(i)
            elif not "<title>" in source:
                line = url
                ind = line.index(":")
                line = line[ind:]
                line = "".join(line.split("//"))
                line = "".join(line.split(":"))
                print "\t\tTitle:",line
                app_title = line + " - Omicron"
                self.setWindowTitle(app_title)
                i = self.tabs.addTab(self.newtab, line)
                self.tabs.setCurrentIndex(i)
        finally:
            self.urlbar.setText(query.toString())
            self.urlbar.setCursorPosition(0)
    def navigate_to_url(self):
        urlText = self.urlbar.text()
        query = QUrl(urlText)
        serv = query.scheme()
        print "urlText:",urlText,"| service:",serv
        searchEngine = self.search_engine.currentText()
        print "Search Engine:",searchEngine
        if serv == "" and not urlText.startswith("/") or serv == "http":
            query.setScheme("http")
            self.update_urlbar(query)
            self.browser.setUrl(query)
        elif serv == "" and urlText.startswith("/") or serv == "file":
            query.setScheme("file")
            path = "".join(query.toString().split('file://'))
            print "Path", path
            if os.path.isfile(path) == True:
                #self.update_urlbar(query)
                self.browser.setUrl(query)
            elif os.path.isfile(path) == False or os.path.isdir(path) == False:
                flav = QIcon("icons/warning.png")
                i = self.tabs.addTab(self.newtab, flav, "File Not Found")
                self.tabs.setCurrentIndex(i)
                self.browser.setUrl(query)
            elif os.path.isdir(path) == True:
                self.model = QFileSystemModel()
                self.model.setRootPath(path)
                self.tree = QTreeView()
                self.tree.setModel(self.model)
                self.tree.setAnimated(True)
                self.tree.setIndentation(20)
                self.tree.setSortingEnabled(True)

                windowLayout = QVBoxLayout()
                windowLayout.addWidget(self.tree)
                self.setLayout(windowLayout)
                self.show()
                #i = self.tabs.addTab(self.newtab, line)
                #self.tabs.setCurrentIndex(i)
                #self.browser.setUrl(query)
        elif serv == "https":
            query.setScheme("https")
            self.update_urlbar(query)
            self.browser.setUrl(query)
    def navigate_home(self):
        url = HomeURL
        self.urlbar.setText("LOADING...")
        self.urlbar.setText(url)
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.setUrl(QUrl(url))

class AppUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.browser = QWebView()
        #Browser plugins and additions
        self.browser.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        #Window Title
        self.setWindowTitle("Omicron")
        self.setWindowIcon(QIcon("icons/i.jpeg"))
        #Window Dimensions
        self.setGeometry(170, 105, 1070, 590)
        #Menu Bar
        self.initUI()
        #Home Page
        url = HomeURL
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        d = QIcon("icons/home.png")
        i = self.tabs.addTab(TabNav(url, self.tabs), d, "New Tab")
        self.tabs.setCurrentIndex(i)
        self.setCentralWidget(self.tabs)
        self.tabs.removeTab(i)
    def close(self,i):
        num = self.tabs.count()
        title = "Confirm Close"
        alert = "You are about to close the last tab. This will exit Mystica Browser. Are you sure you want to continue?"
        if self.tabs.count() < 2:
            buttonReply = QMessageBox.question(self, title, alert, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                print('Affirmative Exit Confirmed')
                self.tabs.removeTab(i)
                sys.exit(0)
            else:
                print('Negative Exit Confirmed')
                return
        self.tabs.removeTab(i)
        print tt(),"Closed tab ",i, "of ",num
    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.create_new_tab(False)
    def create_new_tab(self,url):
        print url
        if url == False:
            url = "file:///root/Documents/webdev/index.html"
            i = self.tabs.addTab(TabNav(url, self.tabs), "New Blank Tab")
            #i = self.tabs.addTab(startpage.NewStartPage(self.tabs), "Start Page")
            self.tabs.setCurrentIndex(i)
            print "Tab No.",i, url
            self.setCentralWidget(self.tabs)
            self.tabs.removeTab(i)
        else:
            i = self.tabs.addTab(TabNav(url, self.tabs), "New Blank Tab")
            self.tabs.setCurrentIndex(i)
            print "Tab No.",i, url
            self.setCentralWidget(self.tabs)
            self.tabs.removeTab(i)
    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)",options=options)
##        if filename:
##            with open(filename, 'r') as f:
##                html = f.read()
##            f.close()
        filename = "file://"+filename
        print "URL as ",filename
        self.create_new_tab(filename)
    def save_file_as(self):
        #SAVE FILE AS NEEDS MORE WORK
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)",options=options)
        if filename:
            html = self.tabs.currentWidget().page().mainFrame().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))
        
    def print_current_page(self):
        ##PRINT NEEDS MORE WORK
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()
    def about(self):
        dlg = AboutDialog()
        dlg.exec_()
    def helpPage(self):
        url = "file:///root/Documents/webd/OneWeb/index.html"
        self.create_new_tab(url)
    def home_page(self):
        url = "file:///root/Documents/webd/OneWeb/index.html"
        self.create_new_tab(url)
        
    def initUI(self):               
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        editMenu = mainMenu.addMenu("Edit")
        viewMenu = mainMenu.addMenu("View")
        toolsMenu = mainMenu.addMenu("Tools")
        prefMenu = mainMenu.addMenu("Preferences")
        helpMenu = mainMenu.addMenu("Help")
        #Applications to run on File Menu
        #Open New Tab
        newtab = QAction(QIcon("icons/ui-tab--plus.png"), "New Tab", self)
        newtab.setShortcut("Ctrl+T")
        newtab.setStatusTip("Open New Tab")
        newtab.triggered.connect(self.create_new_tab)
        fileMenu.addAction(newtab)
        #Open File
        open_file = QAction(QIcon("icons/new-file.gif"), "Open File...", self)
        open_file.setShortcut("Ctrl+O")
        open_file.setStatusTip("Open From File")
        open_file.triggered.connect(self.open_file)
        fileMenu.addAction(open_file)
        #Save File
        save_file = QAction(QIcon("icons/save.png"), "Save Page As...", self)
        save_file.setShortcut("Ctrl+S")
        save_file.setStatusTip("Save Current Page to File")
        save_file.triggered.connect(self.save_file_as)
        fileMenu.addAction(save_file)
        #Print Page
        print_page = QAction(QIcon("icons/printer.png"), "Print...", self)
        print_page.setStatusTip("Print Current Page")
        print_page.setShortcut("Ctrl+P")
        print_page.triggered.connect(self.print_current_page)
        fileMenu.addAction(print_page)
        #closing Application
        exitbutton = QAction(QIcon("icons/cross.png"), "Quit", self)
        exitbutton.setShortcut("Ctrl+Q")
        exitbutton.setStatusTip("Close The Browser")
        exitbutton.triggered.connect(self.close)
        fileMenu.addAction(exitbutton)

        ##Applications to Run on Help Menu
        #HomePage
        homepage = QAction(QIcon("icons/audit_icon.svg"), "Mystica HomePage", self)
        homepage.setStatusTip("Go To Mystic HomePage")
        homepage.triggered.connect(self.home_page)
        helpMenu.addAction(homepage)
        #Hr
        mainMenu.addSeparator()
        #Help Page
        help_page = QAction(QIcon("icons/question-msg.gif"), "Mystica Help", self)
        help_page.setStatusTip("Mystica Help Page")
        help_page.triggered.connect(self.helpPage)
        helpMenu.addAction(help_page)
        mainMenu.addSeparator()
        #About
        about = QAction(QIcon("icons/infop.png"), "About Mystica", self)
        about.setStatusTip("Find Out More About Mystica")
        about.triggered.connect(self.about)
        helpMenu.addAction(about)
          
        #Status Bar
        self.statusBar().showMessage("Message in a Status Bar")
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    #app.setApplicationName("Omicron")
    app.setOrganizationName("Karoki")
    app.setOrganizationDomain("com")
    #Set Styles
    app.setStyle("Fusion")
    ex = AppUI()
    ex.show()
    app.exec_()
##    def run():
##        l = url_to_path_dir("https://www.google.com/")
##        print l,"sd"
##        #print l.strip("\n")
##    run()
