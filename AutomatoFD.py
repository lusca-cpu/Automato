#Esqueleto de código Python para implementar algoritmos sobre automatos finitos.
import xmltodict

class AutomatoFD:

    #a função init é a função construtora da classe
    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.inicial = None
        self.finais = set()

    #inicializa variaveis utilizadas no processamento de cadeias ("zera" o autômato)
    def limpaAfd(self):
        self.__deuErro = False
        self.__estadoAtual = self.inicial

    # Cria o estado int(id) se ele ainda não existe e retorna True. Se o estado já existe, não faz nada e retorna falso.
    def criaEstado(self, id, inicial=False, final=False):

        id = int(id)
        if id in self.estados: #verifica se o estado já está no conjunto de estados existentes, se ele já existe não faz nada
            return False
        self.estados = self.estados.union({id}) #se o estado ainda não existe, adiciona ele no conjunto de estados
        if inicial:
            self.inicial = id
        if final:
            self.finais = self.finais.union({id})
        return True

    #Cria a transição "(origem,simbolo)->destino", se os parametros são validos e retorna True. Caso contrário, não faz nada e retorna False.
    def criaTransicao(self, origem, destino, simbolo):

        origem = int(origem)
        destino = int(destino)
        simbolo = str(simbolo)

        if not origem in self.estados: #verifica se o estado está no conjunto de estados  # noqa: E713
            return False
        if not destino in self.estados: #verifica se o estado está no conjunto de estados  # noqa: E713
            return False
        if len(simbolo) != 1 or not simbolo in self.alfabeto: #verifica se o simbolo digitado possui apenas 1 caractere e se ele está no conjunto do alfabeto  # noqa: E713
            return False

        self.transicoes[(origem, simbolo)] = destino #se estiver tudo certo, a transição é criada
        return True

    #Define um estado já existente como inicial
    def mudaEstadoInicial(self, id):
        if not id in self.estados: #verifica se o estado faz parte do conjunto de estados  # noqa: E713
            return
        self.inicial = id #coloca o estado passado no parâmetro como sendo o novo estado inicial

    def mudaEstadoFinal(self, id, final):
        if not id in self.estados:  # noqa: E713
            return
        if final: #se o estado for final, ele será incluído no conjunto de estados finais
            self.finais = self.finais.union({id})
        else: #se o estado não for final e estiver no conjunto dos estados finais, ele é retirado
            self.finais = self.finais.difference({id})

    #Partindo do estado atual, processa a cadeia e retorna o estado de parada. Se ocorrer erro, liga a variavel __deuErro.
    def move(self, cadeia):
        for simbolo in cadeia: #o for percorre cada símbolo da cadeia
            if not simbolo in self.alfabeto: #verifica se o símbolo está presente no alfabeto.  # noqa: E713
                self.__deuErro = True #da erro se o símbolo nao estiver no alfabeto
                break
            if(self.__estadoAtual, simbolo) in self.transicoes.keys(): #verifica se a transição existe
                novoEstado = self.transicoes[(self.__estadoAtual, simbolo)] #o novo estado passa a ser o estado resultante da transição
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True #da erro se a transição não existir
                break
        return self.__estadoAtual #a ultima vez que rodar no loop, o estado atual será o que tiver parado

    #a função retorna o valor da variavel __deuErro (usada na função move)
    def deuErro(self):
        return self.__deuErro

    # a função retorna o valor da variavel __estadoAtual (usada na função move)
    def estadoAtual(self):
        return self.__estadoAtual

    # a função retorna o estado final
    def estadoFinal(self, id):
        return id in self.finais

    #sempre que o python precisar enxergar o AFD como string, ele usa essa função. Essa função imprime o AFD
    def __str__(self):
        s = 'AFD(E, A, T, i, F): \n'
        s += ' E = { '
        for e in self.estados:
            s += '{}, '.format(str(e))
        s += '} \n'
        s += '  A = {'
        for a in self.alfabeto:
            s += "'{}', ".format(a)
        s += '} \n'
        s += '  T = {'
        for (e, a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += "({}, '{}')-->{} ".format(e, a, d)
        s += '} \n'
        s += '  i = {} \n'.format(self.inicial)
        s += ' F = { '
        for e in self.finais:
            s += '{}, '.format(str(e))
        s += '}'
        return s

    #função que carrega o automato (cria os estados, as transições e define os estados finais e iniciais)
    def carregaAFD(self, afdXml):
        # laco for para criar os estados
        for i in range(len(afdXml["structure"]["automaton"]["state"])):  # o parâmetro: len(afdXml["structure"]["automaton"]["state"]) + 1 me retorna o comprimento da lista que contém os estados e acrescenta em uma unidade, já que o for percorre de 0 a n - 1.
            self.criaEstado(i)

        # trecho do código chama o método que procura o estado inicial e o define como estado inicial
        inicial = int(self.procuraInicial(afdXml["structure"]["automaton"]["state"], len(afdXml["structure"]["automaton"]["state"])))
        self.mudaEstadoInicial(inicial)

        # trecho do código que chama o método que procura o(s) estado(s) final(is) e o define como estado final
        finais = []  # como pode haver mais de um estado final, eu crio uma lista para receber esses estados
        finais = self.procuraFinal(afdXml["structure"]["automaton"]["state"], len(afdXml["structure"]["automaton"]["state"]))
        for i in range(0, len(finais)):
            self.mudaEstadoFinal(int(finais[i]), True)

        # trecho do código que cria as transições
        for i in range(0, len(afdXml["structure"]["automaton"]["transition"])):
            self.criaTransicao(afdXml["structure"]["automaton"]["transition"][i]["from"], afdXml["structure"]["automaton"]["transition"][i]["to"], afdXml["structure"]["automaton"]["transition"][i]["read"])


    #a função le uma arquivo xml gerado pelo JFLAP
    def leXML(self, diretorio):
        try:
            with open(diretorio) as file:
                meuXml = file.read()
                # xmltodict.parse() analisa o conteúdo da variável e converte em um Dicionário
                meuXml = xmltodict.parse(meuXml)
        except:  # noqa: E722
            return None
        return meuXml

    #a função procura o estado inicial dentro da lista de estados gerada pelo arquivo XML
    def procuraInicial(self, estados, tam):
        for i in range(0, tam):
            if "initial" in estados[i]:
                return estados[i]["@id"]

    #a função procura o estado final dentro da lista de estados gerada pelo arquivo XML
    def procuraFinal(self, estados, tam):
        finais = [] #lista que guardará os estados finais
        for i in range(0, tam):
            if "final" in estados[i]:
                finais.append(estados[i]["@id"])

        return finais

    #a função salva o autômato em um arquivo
    def gravaXml(self, nomeArquivo):
        # Estados é a lista que guardará os dicionários de cada estado
        Estados = list(self.estados)

        for i in range(len(self.estados)):
            Estados[i] = {"@id": Estados[i]}
            if str(Estados[i]["@id"]) in str(self.inicial):
                Estados[i].update({"initial": None})
            if str(Estados[i]["@id"]) in str(self.finais):
                Estados[i].update({"final": None})

        # a lista Transições guardará os dicionários de cada transição
        Transicoes = []
        TransicoesChave = list(self.transicoes.keys())
        TransicoesValor = list(self.transicoes.values())
        for i in range(len(self.transicoes)):
            Transicoes.append({"from": TransicoesChave[i][0], "to": TransicoesValor[i], "read": TransicoesChave[i][1]})

        # Tendo feito as listas (que guardarão os estados e as transições) no formato do JFLAP basta montar o resto da estrutura para poder gravar o XML
        afd = {"structure": {"type": 'fa', "automaton": {"state": Estados, "transition": Transicoes}}}
        try:
            with open(nomeArquivo, 'w') as arquivo:
                afd = xmltodict.unparse(afd) #converte o dicionário em xml
                arquivo.write(afd)
                return 0
        except:  # noqa: E722
            return None

    #a função verifica se os dois autômatos possuem o mesmo alfabeto para a operação de multiplicação dos autômatos
    def verificaAlfabeto(self, alfabetoAfd1, alfabetoAfd2):
        if alfabetoAfd1 == alfabetoAfd2:
            return self.alfabeto
        else:
            return None


    #a função realiza a multiplicação entre dois autômatos
    def multiplicaAFD(self, estadosAFD1, transicoesAFD1, estadosAFD2, transicoesAFD2):
        estadosaf1 = list(estadosAFD1) #{0, 1, 2, 3}
        estadosaf2 = list(estadosAFD2) #{0, 1}
        alfabeto = set(self.alfabeto) #conversão do alfabeto para set para separar os caraceteres do alfabeto (o alfabeto é recebido como string)
        simbolo = list(alfabeto) #conversão do set que contém os caracteres do alfabeto para lista, para poder manipular os caracteres
        estados = list()
        transicoes = list()

        #DEFININDO OS ESTADOS DO AFD RESULTANTE
        for i in range(len(estadosAFD1)):
            for j in range(len(estadosAFD2)):
                estados.append((estadosaf1[i], estadosaf2[j]))

        #DEFININDO AS TRANSIÇÕES DO AFD RESULTANTE
        for i in range(len(estadosAFD1)):
            for j in range(len(estadosAFD2)):
                for k in range(len(simbolo)):
                    origem = (estadosaf1[i], estadosaf2[j])
                    destino = (transicoesAFD1[(estadosaf1[i], simbolo[k])], transicoesAFD2[(estadosaf2[j], simbolo[k])])
                    transicoes.append([[(origem), simbolo[k]], (destino)])

        #RENOMEANDO OS ESTADOS (Do formato [(1,1), (1,2), ...] para [1, 2, ...])
        for i in range(len(estados)):
            for j in range(len(transicoes)):
                if transicoes[j][0][0] == estados[i]: #verifica se o estado de origem é igual ao estado na posição i
                    transicoes[j][0][0] = i

                if transicoes[j][1] == estados[i]: #verifica se o estado de destino é igual ao estado na posição i
                    transicoes[j][1] = i

            estados[i] = i

        #define os estados do afd resultante
        for i in range(len(estados)):
            self.criaEstado(estados[i])

        #define as transições do afd resultante
        for i in range(len(transicoes)):
            self.criaTransicao(transicoes[i][0][0], transicoes[i][1], transicoes[i][0][1])


    #a função realiza as operações de conjunto sobre os autômatos multiplicados
    def operacoes(self, estadosAF1, inicialAF1, finaisAF1, estadosAF2, inicialAF2, finaisAF2, operacao):
        estadosaf1 = list(estadosAF1)
        estadosaf2 = list(estadosAF2)
        finais = list()

        #ENCONTRANDO OS ESTADOS FINAIS E O ESTADO INICIAL DO AFD RESULTANTE
        for i in range(len(estadosAF1)):
            for j in range(len(estadosAF2)):
                if operacao == 1: #UNIÃO
                    #estados finais
                    if (estadosaf1[i] in finaisAF1) or (estadosaf2[j] in finaisAF2):
                        finais.append(1) #os índices das posições da lista finais corresponde ao nome dos estados. Logo os índices que receberem 1, correspondem aos estados finais
                    else:
                        finais.append(0)
                    #estado inicial
                    if(estadosaf1[i] == inicialAF1) and (estadosaf2[j] == inicialAF2):
                        inicial = i

                elif operacao == 2: #INTERCESSÃO
                    #estados finais
                    if (estadosaf1[i] in finaisAF1) and (estadosaf2[j] in finaisAF2):
                        finais.append(1) #os índices das posições da lista finais corresponde ao nome dos estados. Logo os índices que receberem 1, correspondem aos estados finais
                    else:
                        finais.append(0)
                    #estado inicial
                    if(estadosaf1[i] == inicialAF1) and (estadosaf2[j] == inicialAF2):
                        inicial = i

                elif operacao == 3: #COMPLEMENTO DA UNIÃO
                    #estados finais
                    if (estadosaf1[i] in finaisAF1) or (estadosaf2[j] in finaisAF2):
                        finais.append(0)  # os índices das posições da lista finais corresponde ao nome dos estados. Logo os índices que receberem 1, correspondem aos estados finais
                    else:
                        finais.append(1)
                    #estado inicial
                    if (estadosaf1[i] == inicialAF1) and (estadosaf2[j] == inicialAF2):
                        inicial = i

                elif operacao == 4: #COMPLEMENTO DA INTERCESSÃO
                    #estados finais
                    if (estadosaf1[i] in finaisAF1) and (estadosaf2[j] in finaisAF2):
                        finais.append(0) #os índices das posições da lista finais corresponde ao nome dos estados. Logo os índices que receberem 1, correspondem aos estados finais
                    else:
                        finais.append(1)
                    #estado inicial
                    if(estadosaf1[i] == inicialAF1) and (estadosaf2[j] == inicialAF2):
                        inicial = i

                elif operacao == 5: #COMPLEMENTO DA DIFERENÇA AFD1 - AFD2
                    # estados finais
                    if (estadosaf1[i] in finaisAF1) and (estadosaf2[j] not in finaisAF2):
                        finais.append(0)  # os índices das posições da lista finais corresponde ao nome dos estados. Logo os índices que receberem 1, correspondem aos estados finais
                    else:
                        finais.append(1)
                    # estado inicial
                    if (estadosaf1[i] == inicialAF1) and (estadosaf2[j] == inicialAF2):
                        inicial = i

                elif operacao == 6: #COMPLEMENTO DA DIFERENÇA AFD2 - AFD1
                    # estados finais
                    if (estadosaf1[i] not in finaisAF1) and (estadosaf2[j] in finaisAF2):
                        finais.append(0)  # os índices das posições da lista finais corresponde ao nome dos estados. Logo os índices que receberem 1, correspondem aos estados finais
                    else:
                        finais.append(1)
                    # estado inicial
                    if (estadosaf1[i] == inicialAF1) and (estadosaf2[j] == inicialAF2):
                        inicial = i

                elif operacao == 7: #DIFERENÇA AFD1 - AFD2
                    # estados finais
                    if (estadosaf1[i] in finaisAF1) and (estadosaf2[j] not in finaisAF2):
                        finais.append(1)  # os índices das posições da lista finais corresponde ao nome dos estados. Logo os índices que receberem 1, correspondem aos estados finais
                    else:
                        finais.append(0)
                    # estado inicial
                    if (estadosaf1[i] == inicialAF1) and (estadosaf2[j] == inicialAF2):
                        inicial = i

                elif operacao == 8: #DIFERENÇA AFD2 - AFD1
                    # estados finais
                    if (estadosaf1[i] not in finaisAF1) and (estadosaf2[j] in finaisAF2):
                        finais.append(1)  # os índices das posições da lista finais corresponde ao nome dos estados. Logo os índices que receberem 1, correspondem aos estados finais
                    else:
                        finais.append(0)
                    # estado inicial
                    if (estadosaf1[i] == inicialAF1) and (estadosaf2[j] == inicialAF2):
                        inicial = i

        #define os estados finais do automato resultante
        for i in range(len(finais)):
            if finais[i] == 1:
               self.finais.add(i)

        #definindo o estado inicial do autômato resultante
        self.inicial = inicial
