from model.Documento import *
from controller.ModelController import *
from controller.CrankController import *

unModelController = ModelController()
unModelController.lectura_archivo('FilesUpload/documentos.csv')

unCrankController = CrankController("Green Tea")
unCrankController.calcularScore()
