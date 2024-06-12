from moviepy.editor import VideoFileClip
import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Thread(qt2.QThread):
    finished=qt2.pyqtSignal(bool)
    def __init__(self,p,path,outputFolder):
        super().__init__()
        self.p=p
        self.path=path
        self.outputDIR=outputFolder
    def run(self):
        OutputPath=self.outputDIR + "/" + self.path.split("/")[-1].split(".")[0] + ".mp3"
        try:
            video=VideoFileClip(self.path)
            audio=video.audio
            audio.write_audiofile(OutputPath)
            self.finished.emit(True)
        except Exception as error:
            self.finished.emit(False)
class ConvertGUI(qt.QDialog):
    def __init__(self,p,path,outputFolder):
        super().__init__(p)
        self.setWindowTitle(_("extracting ..."))
        self.thread=Thread(p,path,outputFolder)
        layout=qt.QVBoxLayout(self)
        self.cancel=guiTools.QPushButton(_("cancel"))
        self.cancel.clicked.connect(self.thread.terminate)
        layout.addWidget(self.cancel)
        self.thread.finished.connect(self.on_finish)
        self.thread.start()
    def on_finish(self,state):
        if state:
            qt.QMessageBox.information(self,_("done"),_("extracted"))
        else:
            qt.QMessageBox.warning(self,_("error"),"")
        self.close()