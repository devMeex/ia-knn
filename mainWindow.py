from knn_ui import *
from knn import *
from PyQt5.QtCore import QObject, pyqtSlot
from browseFile import BrowseFile


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    data = []
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.browseFile = BrowseFile()

        self.cargarArchivo_btn.clicked.connect(self.browseSlot)
        self.createTable()

    def refreshAll( self ):
        '''
        Updates the widgets whenever an interaction happens.
        Typically some interaction takes place, the UI responds,
        and informs the model of the change.  Then this method
        is called, pulling from the model information that is
        updated in the GUI.
        '''
        self.input_archivo.setText( self.browseFile.getFileName() )
        self.textBrowser.setText( str(self.data) )

    def renderData( self ):
        if self.separador_1:
            sep = ","
        else:
            sep = ";"

        if self.checkBox.isChecked:
            header = 0
        else:
            header = None

        self.data = tratar_csv(self.browseFile.getFileName(), sep, header)
        self.textBrowser_2.setText(str(len(self.data)))
        print(type(self.data))

    def createTable( self ):
        # Column count
        numcols = 3
        self.tableWidget.setColumnCount(numcols)
        header_labels = ['X', 'Y', 'Clase']
        self.tableWidget.setHorizontalHeaderLabels(header_labels)

        if self.data:
            # Row count
            numrows = len(self.data)
            self.tableWidget.setRowCount(numrows)

            for row in range(numrows):
                for column in range(numcols):
                    item = QtWidgets.QTableWidgetItem(str(self.data[row][column]))
                    # item = QtWidgets.QTableWidgetItem("Holis")
                    print(item)
                    self.tableWidget.setItem(row, column, item)

            # print(type(rows))
            # self.tableWidget.setRowCount(21)

            #set header titles
            # self.tableWidget.setHorizontalHeaderLabels(QString("Name;Age;Sex;Add").split(";"))
            # self.tableWidget.setItem(0,2, QTableWidgetItem("Clase"))


    @pyqtSlot( )
    def browseSlot( self ):
        ''' Called when the user presses Cargar Archivo button'''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "Plain text files (*.txt);;CSV files (*.csv)",
                        options=options)
        if fileName:
            self.browseFile.setFileName( fileName )
            self.refreshAll()

    @pyqtSlot( )
    def graphSlot( self ):
        # call graph method
        self.textBrowser_2.setText( "graph button clicked" + "  , = " + str(self.separador_1.isChecked()) + "  ; = " + str(self.separador_2.isChecked()) + "  k = " + str(self.input_k.value()) )
        # control_entrada(self.browseFile.getFileContent(), self.input_k, self.input_entrenamiento)

    @pyqtSlot( )
    def testSlot( self ):
        # call method
        self.textBrowser_2.setText( "test button clicked" + " entrenamiento = " + str(self.input_entrenamiento.value()) )

    @pyqtSlot( )
    def classifySlot( self ):
        # call predecir_clasificacion method
        self.textBrowser_2.setText( "classify button clicked" + "x =  " + str(self.input_x.value()) + "y =  " + str(self.input_y.value()) )

    @pyqtSlot( )
    def updateTest( self ):
        # call predecir_clasificacion method
        testPercentage = 100 - self.input_entrenamiento.value()
        self.input_test.setText( str(testPercentage) )

    @pyqtSlot( )
    def updateTable( self ):
        self.renderData()
        self.createTable()

    @pyqtSlot( )
    def entryControl( self ):
        self.textBrowser_2.setText("controlando entrada")
        # control = control_entrada(self.data, self.input_k, self.input_entrenamiento)
        # if control:
        #     self.textBrowser_2.setText("Es posible realizar operaciones")
        # else:
        #     self.textBrowser_2.setText(control[1])

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()