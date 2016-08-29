from __future__ import division
from pattern.vector import Document, PORTER, Model, TFIDF
from model.Documento import *

class CrankController(object):
    """docstring for CrankController."""
    query = ""
    unModelo = Model(documents=[],weight=TFIDF)

    def __init__(self,query):
        super(CrankController, self).__init__()
        self.query = Document(query,stemmer=PORTER)

    def calcularScore(self):
        self.calcularScoreRelevance()
        self.calcularScoreContribution()
        self.calcularScoreFinal()

    def calcularScoreRelevance(self):
        with db_session:
            for unDocumento in Documento.select():
                unDocumentoPattern = Document(self.leerArchivo(unDocumento),stemmer=PORTER,name=unDocumento.url)
                self.unModelo.append(unDocumentoPattern)

        for unDocumento in self.unModelo:
            scoreRelevance = 0
            var_coord = self.coord(unDocumento,self.query)
            for unTermino in self.query:
                scoreRelevance += unDocumento.tfidf(unTermino) * self.norm(unDocumento,unTermino) * var_coord
            unDocumento.scoreRelevance = scoreRelevance



    def calcularScoreContribution(self):
        pass

    def calcularScoreFinal(self):
        pass

    def leerArchivo(self,documento):
        rutaArchivo = "FilesDownload/"+str(documento.id)+".txt";
        return open(rutaArchivo,'r').read()

    def coord(self,documento, consulta):
        contador = 0
        for word in consulta:
            if word in documento.words:
                contador +=1
        return (contador / len(consulta))

    def norm(self,documento, un_termino):
        valor = 0
        if un_termino in documento.words:
            valor = documento.tf(un_termino)
        return valor
