from knn_ui import *
from knn import *
from PyQt5.QtCore import QObject, pyqtSlot
from browseFile import BrowseFile


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    data = []
    data_df = []
    training_data = []
    training_data_df = []
    test_data = []
    test_data_df = []
    labels = []

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
        if self.browseFile.getFileContent():
            self.textBrowser.setText( str(self.data) )

    def renderData( self ):
        print("coma" + str(self.separador_1.isChecked()))
        if self.separador_2.isChecked():
            sep = ";"
        else:
            sep = ","

        if self.checkBox.isChecked():
            header = 0
        else:
            header = None
        if self.input_entrenamiento.value() != 0:
            self.data = leer_dataset(self.browseFile.getFileName(), self.input_k.value(), self.input_entrenamiento.value(), sep, header)[0].values.tolist()
            self.data_df = leer_dataset(self.browseFile.getFileName(), self.input_k.value(), self.input_entrenamiento.value(), sep, header)[0]
            self.labels = leer_dataset(self.browseFile.getFileName(), self.input_k.value(), self.input_entrenamiento.value(), sep, header)[1]
            self.textBrowser.setText(str(self.data))
        else: self.textBrowser_2.setText("Seleccione un porcentaje de entrenamiento y vuelva a hacer click en Validar Datos")

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

            # Fill table with data
            for row in range(numrows):
                for column in range(numcols):
                    item = QtWidgets.QTableWidgetItem(str(self.data[row][column]))
                    self.tableWidget.setItem(row, column, item)

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
        dibujar_puntos(self.data_df, self.labels)
        plotear_grid(self.data_df, self.input_k, self.labels)


    @pyqtSlot( )
    def testSlot( self ):
        # call method clasificar data test
        self.textBrowser_2.setText( "test button clicked" + " entrenamiento = " + str(self.input_entrenamiento.value()) )
        print("testdata" + str(self.test_data))
        print("testtraining" + str(self.training_data))
        test = clasificar_datatest(self.training_data, self.test_data, self.labels)
        print("testslot" + str(test))
        self.textBrowser_2.setText("\nK:%s => Acertados: %s, Porcentaje: %s%s , Tiempo(seg): %s\n" % (
            k, acertados, round(acertados / len(test) * 100, 3), '%', time.time() - startTime))

    @pyqtSlot( )
    def updateTrainingSet( self ):
        self.renderData()
        divided_sets = dividir_dataset(self.data_df, self.input_entrenamiento.value())
        self.training_data = divided_sets[0]
        self.test_data = divided_sets[1]
        self.textBrowser.setText(str(self.training_data))

    @pyqtSlot( )
    def classifySlot( self ):
        # call predecir_clasificacion method
        coord = [ self.input_x.value() , self.input_y.value() ]
        self.textBrowser_2.setText(str(coord))
        if not self.data:
            self.textBrowser_2.setText("Cargue un dataset para poder realizar la predicción")
        elif not self.training_data:
            self.textBrowser_2.setText("Seleccione un porcentaje de entrenamiento")
        else:
            pred = predecir_clasificacion(self.training_data, coord, self.input_k.value())
            self.textBrowser_2.setText("El punto pertenece a la clase: " + str(pred))

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
        # print("salida control" + str(control))
        # if control:
        #     self.textBrowser_2.setText("Es posible realizar operaciones")
        # else:
        #     self.textBrowser_2.setText(control[1])

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()