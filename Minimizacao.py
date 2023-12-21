class Minimizacao:

    def __init__(self):
        self.estados_equi = []
        self.minAFD = []
        self.matrix = [[]]
        self.flagEqui = bool

    def incializaMatrix(self, afd):
        finais = list(afd.finais)
        #criando a matriz de equivalencia
        self.matrix = [[0 for _ in range(len(afd.estados))] for _ in range(len(afd.estados))]

        #inicialixando a lista com os estados nao utilizados e os estados esquivalentes
        for i in range(0, len(afd.estados)):          
            lista = []
            for j in range(0, len(afd.estados)):
                if(j>=i):
                    lista.append(2)
                else:
                    lista.append(0)
            self.matrix[i] = lista

        #inicializando os finais com nao finais
        for i in range(0, len(afd.estados)):
            for j in range(0, len(afd.estados)):
                    if((i in finais or j in finais) and self.matrix[i][j] != 2):
                        if i in finais and j in finais:
                            self.matrix[i][j] = 0
                        else:
                            self.matrix[i][j] = 1

    # achando os estados equivalentes
    def estadosEquivalentes(self, afd, alfabeto):

        estados = list(afd.estados)

        if(self.matrix == [[]]):
            self.incializaMatrix(afd)

        for i in range(0, len(afd.estados)):
            for j in range(0, len(afd.estados)):
                if(self.matrix[i][j]==2):
                    break
                
                for k in range(0, len(alfabeto)):
                    if((afd.transicoes[estados[i], alfabeto[k]] != afd.transicoes[estados[j], alfabeto[k]] and
                       self.matrix[afd.transicoes[estados[j], alfabeto[k]]][afd.transicoes[estados[i], alfabeto[k]]]==1) or
                       (afd.transicoes[estados[i], alfabeto[k]] in afd.finais and afd.transicoes[estados[j], alfabeto[k]] not in afd.finais) or
                       (afd.transicoes[estados[i], alfabeto[k]] not in afd.finais and afd.transicoes[estados[j], alfabeto[k]] in afd.finais)):
                            self.matrix[i][j] = 1
                
        # salvando estados equivalentes
        for i in range(0, len(afd.estados)):
            for j in range(0, len(afd.estados)):
                if(self.matrix[i][j]==0):
                    self.estados_equi.append((i,j))

        # mostrando a tabela dos esatdos equivalentes
        print("A tabela para encontrar os estados equivalentes: ", end='')
        for i in range(0, len(afd.estados)):
            for j in range(0, len(afd.estados)):
                if (i!=j and i>j):
                    print(f'[{self.matrix[i][j]:^5}]', end='')
            print()
        print()
        
        if self.estados_equi is []:
            return self.estados_equi
        else:
            minAFD = {}
            afd1Inicial = afd.inicial
            afd1 = list(afd.estados)
            removeEstados = []
            afd1Final = list(afd.finais)
            removeFinal = []
            trans1 = afd.transicoes
            removeTrans = [] 
            chaves_trans = list(trans1.keys())
            
            for estados_equi in self.estados_equi:
                for i in range(len(afd1)):
                    if estados_equi[0] == afd1[i]:
                        removeEstados.append(i)

                for i in range(len(afd1Final)):
                    if estados_equi[0] == afd1Final[i]:
                        removeFinal.append(i)

                for i in trans1.keys():
                    if estados_equi[0] == i[0]:
                        removeTrans.append(i)

            for estados_equi in self.estados_equi :
                for chaves in chaves_trans:
                    if estados_equi[0] == trans1[chaves]:
                        trans1[chaves] = estados_equi[1]
                              
            for i in reversed(removeEstados):
                afd1.pop(i)     

            for i in reversed(removeFinal):
                afd1Final.pop(i)   

            for i in reversed(removeTrans):
                trans1.pop(i)

            minAFD.update({'Estados': afd1,'Estado Inicial': afd1Inicial, 'Estado final': afd1Final, 'Transições': trans1})

            return minAFD
