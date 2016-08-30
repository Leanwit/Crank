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
        self.limpiarScores()
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
                unDocumentoBD = Documento.get(url=unDocumento.name)
                unDocumentoBD.scoreRelevance = scoreRelevance


    def calcularScoreContribution(self):
        listaDocumentos = []
        analizados = []
        with db_session:
            for documento in self.unModelo:
                unDocumento = Documento.get(url=documento.name)
                unDocumento.scoreContribution = self.calcularScoreContributionRecursividad(unDocumento,0,analizados)

    def calcularScoreContributionRecursividad(self,doc,nivel,analizados):
        score = 0
        if nivel < 4:
            if not doc in analizados:
                analizados.append(doc)
                if doc.Target:
                    for inlink in doc.Target:

                        score += self.calcularScoreContributionRecursividad(inlink,nivel+1,analizados)
                        if inlink.Target:
                            score_inlink = 0
                            for aux_inlink in inlink.Target:
                                score_inlink += aux_inlink.scoreRelevance
                            if inlink.scoreRelevance != 0:
                                score += (doc.scoreRelevance/(inlink.scoreRelevance+score_inlink))*inlink.scoreRelevance
                        else:
                            score += doc.scoreRelevance
        return score

    def calcularScoreFinal(self):
        with db_session:
           for unDocumento in Documento.select():
               unDocumento.scoreFinal = 0
               print unDocumento.scoreRelevance
               unDocumento.scoreFinal = 0.80 * unDocumento.scoreRelevance + 0.20 * unDocumento.scoreContribution
               commit()

    def limpiarScores(self):
        with db_session:
           for unDocumento in Documento.select():
               unDocumento.scoreRelevance = 0
               unDocumento.scoreContribution = 0
               unDocumento.scoreFinal = 0


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
