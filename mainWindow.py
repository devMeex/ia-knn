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
        self.setInputTest()
        self.probar_btn.setDisabled(True)
        self.graficar_btn.setDisabled(True)
        self.clasificar_btn.setDisabled(True)
        self.clasificar_btn_2.setDisabled(True)

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
            self.data = self.browseFile.getFileContent()
        else:
            self.data = None

    def checked(self):
        if (self.separador_1.isChecked() or self.separador_2.isChecked()):
            self.graficar_btn.setDisabled(False)
            self.probar_btn.setDisabled(False)
            self.clasificar_btn.setDisabled(False)
            self.clasificar_btn_2.setDisabled(False)
        else:
            self.textBrowser_2.setText("Seleccione marcador asociado al dataset")

    def setInputTest( self ):
        testPercentage = 100 - self.input_entrenamiento.value()
        self.input_test.setText( str(testPercentage) )


    def renderData( self ):
        if self.separador_2.isChecked():
            sep = ";"
        else:
            sep = ","

        if self.checkBox.isChecked():
            header = 0
        else:
            header = None
        try:
            action = leer_dataset(self.browseFile.getFileName(), self.input_k.value(), self.input_entrenamiento.value(), sep, header)
            print('action')
            print(action)
            print('endaction')
            if action:
                self.data = action[0].values.tolist()
                self.checked()
                self.data_df = action[0]
                self.labels = action[1]
            else:
                self.textBrowser_2.setText(action)
        except:
            if self.input_entrenamiento.value() == 0:
                self.textBrowser_2.setText("Seleccione un porcentaje de entrenamiento mayor a cero")
            else:
                self.textBrowser_2.setText("El dataset ingresado no es valido. Ingrese otro dataset para poder realizar operaciones")

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
            try:
                for row in range(numrows):
                    for column in range(numcols):
                        item = QtWidgets.QTableWidgetItem(str(self.data[row][column]))
                        self.tableWidget.setItem(row, column, item)
                self.textBrowser_2.clear()
            except:
                self.textBrowser_2.setText("El separador elegido no coincide con el separador del Dataset cargado")
                self.clearTable()

    def clearTable( self ):
        self.tableWidget.setRowCount(0)

    @pyqtSlot( )
    def browseSlot( self ):
        ''' Called when the user presses Cargar Archivo button'''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                    None,
                    "Search File",
                    "",
                    "Plain text files (*.txt);;CSV files (*.csv)",
                    options=options)
        if fileName:
            self.browseFile.setFileName( fileName )
            self.refreshAll()

    @pyqtSlot( )
    def graphSlot( self ):
        # call graph method
        if not (self.data is None):
            dibujar_puntos(self.data_df, self.labels)
        else:
            self.textBrowser_2.setText("Seleccione marcador asociado al dataset")



    @pyqtSlot( )
    def testSlot( self ):
        # call method clasificar data test
        if not (self.data is None):
            test = clasificar_datatest(self.training_data, self.test_data, self.labels)
            self.radioButton.isChecked()
            if self.radioButton.isChecked():
                self.textBrowser_2.clear()
                for i in range(1, len(test)+1):
                    (self.textBrowser_2.append("K: " + str(test[i]['k']) + "\n"
                        + str(test[i]["acertados"]) + " aciertos" + "\n"
                        + "Porcentaje: " + str(test[i]["porcentaje"]) + "\n"
                        + "Tiempo: " + str(test[i]["time"]) + "\n" + "\n"
                    ))
            else:
                proc = medir_procesamiento(test)
                (self.textBrowser_2.setText("El k óptimo es: " + str(proc[0]['k']) + "\n"
                    + str(proc[0]["acertados"]) + " aciertos" + "\n"
                    + "Porcentaje: " + str(proc[0]["porcentaje"]) + "\n"
                    + "Tiempo: " + str(proc[0]["time"]) + "\n" + "\n"
                    "El peor k es: " + str(proc[1]['k']) + "\n"
                    + str(proc[1]["acertados"]) + " aciertos" + "\n"
                    + "Porcentaje: " + str(proc[1]["porcentaje"]) + "\n"
                    + "Tiempo: " + str(proc[1]["time"]) + "\n" + "\n"
                    + "Promedio: " + str(proc[2]) + "\n" + "\n"
                    + "Desvío Estándar: " + str(proc[3]) + "\n"
                ))
        else:
            self.textBrowser_2.setText("Cargue un dataset válido para poder probar el rendimiento")

    @pyqtSlot( )
    def updateTrainingSet( self ):
        if (not (self.data is None)):
            if (self.input_entrenamiento.value() > 0):
                self.renderData()
                print(self.data_df)
                divided_sets = dividir_dataset(self.data_df, self.input_entrenamiento.value())
                self.training_data = divided_sets[0]
                self.test_data = divided_sets[1]
            else:
                self.textBrowser_2.setText("Introduzca un porcentaje de entrenamiento mayor a cero")
        else:
            self.textBrowser_2.setText("Cargue un dataset válido para poder realizar operaciones")

    @pyqtSlot( )
    def classifySlot( self ):
        # call predecir_clasificacion method
        coord = [ self.input_x.value() , self.input_y.value() ]
        self.textBrowser_2.setText(str(coord))
        if self.data is None:
            self.textBrowser_2.setText("Cargue un dataset válido para poder realizar la predicción")
        elif not self.training_data:
            self.textBrowser_2.setText("Seleccione un porcentaje de entrenamiento")
        else:
            pred = predecir_clasificacion(self.training_data, coord, self.input_k.value())
            self.textBrowser_2.setText("El punto " + str(coord) + " pertenece a la clase: " + str(pred))

    @pyqtSlot( )
    def plotGrid( self ):
        # call plotear_grid method

        if (not (self.data is None)):
            plotear_grid(self.data_df, self.input_k.value(), self.labels)
        else:
            self.textBrowser_2.setText("Cargue un dataset válido para graficar")

    @pyqtSlot( )
    def updateTest( self ):
        # call predecir_clasificacion method
        if self.input_entrenamiento.value() > 0:
            self.textBrowser_2.clear()
        else:
            self.textBrowser_2.setText("Introduzca un porcentaje de entrenamiento mayor a cero")
        self.setInputTest()

    @pyqtSlot( )
    def updateTable( self ):
        # self.textBrowser_2.clear()
        if (not (self.data is None)):
            self.renderData()
            if self.input_entrenamiento.value() > 0:
                self.renderData()
                self.createTable()
            else:
                self.clearTable()
                self.textBrowser_2.setText("Introduzca un porcentaje de entrenamiento mayor a cero")
        else:
            self.clearTable()
            self.textBrowser_2.setText("Cargue un dataset valido los datos para poder realizar operaciones")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()