from model.Documento import *
import os.path
import sys
from pattern.web import URL, plaintext

class ModelController(object):
    """docstring for ModelController."""
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        super(ModelController, self).__init__()


    def lectura_archivo(self,archivo):
        lista_documentos = []
        archivo = open(archivo,'r')
        archivo = archivo.read()
        for unaLinea in archivo.split('\n'):
            if unaLinea:
                datos = unaLinea.split(';')
                with db_session:

                    documentoSource = Documento.get(url=datos[1])
                    if not documentoSource:
                        documentoSource = Documento(url=datos[1])
                        commit()
                    self.descargarPagina(documentoSource)


                    documento = Documento.get(url=datos[0])
                    if not documento:
                        documento = Documento(url=datos[0])
                        documento.set(Target=documentoSource)
                        commit()
                    self.descargarPagina(documento)


    def getInlink(self,url):
        with db_session:
            unDocumento = Documento.get(url=url)
            for inlink in unDocumento.Target:
                print inlink.url


    def descargarPagina(self,documento):
        rutaArchivo = "FilesDownload/"+str(documento.id)+".txt";
        if not os.path.isfile(rutaArchivo):
            descarga = URL(documento.url).download()
            f = open(rutaArchivo, 'wb')
            f.write(plaintext(descarga))
