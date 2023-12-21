import AutomatoFD as AF
import time
import Minimizacao 
import AutomatosEquivalentes

while True:
    print("\n\n----*-----*----- BEM VINDO! -----*-----*-----\n"
          "O que deseja fazer?\n"
          "Carregar autômato ---------------------- 1\n"
          "Fechar programa ------------------------ 0\n")
    op = int(input("Digite o número correspondente à opção desejada: "))
    if op == 0:
        break
    elif op == 1:
        print("\n----*----*----*----*----*----*----*----*----\n"
              "Quantos autômatos deseja carregar?\n"
              "Digite 1 para carregar um automato\n"
              "Digite 2 para carregar dois automatos\n")
        qtdAF = int(input("Opção desejada: "))

        if qtdAF == 1: #menu para o caso do usuário usar operações que demandam apenas um autômato

            print("\n-----*----- CARREGANDO AUTÔMATO -----*-----")
            alfabeto = input("Informe o alfabeto do automato: ")
            afd = AF.AutomatoFD(alfabeto) #instancia o objeto para o autômato
            diretorio = input("Informe o diretorio do automato: ")
            afdXml = afd.leXML(diretorio) #lê o arquivo xml
            if afdXml is None:
                print("Não foi possível ler o arquivo.Tente novamente.")
                break
            else:
                print("\n*-*-*-*-* Autômato lido com sucesso! *-*-*-*-* \n")
                afd.carregaAFD(afdXml)
            while True:
                print("\n-----*----- MENU DE OPÇÕES -----*-----\n"
                      "Printar autômato ------------------- 1\n"
                      "Rodar cadeia no autômato ----------- 2\n"
                      "Minimizar autômato ----------------- 3\n"
                      "Salvar autômato -------------------- 4\n"
                      "Sair do menu de opções ------------- 0\n")
                opcao = int(input("Opção desejada: "))

                if opcao == 0: #SAIR DO MENU DE OPÇÕES
                    break

                elif opcao == 1: #PRINTAR AUTÔMATO
                    
                    print("\n----*----*----*-----------------------------------------------------------------------------------------------------------------------------------*----*----*----\n")
                    print(afd)
                    print("\n----*----*----*-----------------------------------------------------------------------------------------------------------------------------------*----*----*----\n")

                elif opcao == 2: #RODAR CADEIA
                    while True:
                        print("\n-----*----- INSERINDO CADEIA -----*-----\n"
                              "Inserir cadeia ------------------------- 1\n"
                              "Sair desse menu ------------------------ 0\n")
                        opcaoCadeia = int(input("Opção desejada: "))

                        if opcaoCadeia == 0:
                            break

                        elif opcaoCadeia == 1:
                            cadeia = input("Digite a cadeia que deseja testar: ")
                            afd.limpaAfd() #inicializa o autômato
                            parada = afd.move(cadeia) #roda a cadeia e retorna o estado de parada
                            if afd.deuErro():
                                print("Não foi possível rodar a cadeia. Tente novamente.")
                            else:
                                if not afd.deuErro() and afd.estadoFinal(parada):
                                    print('Aceita cadeia "{}"'.format(cadeia))
                                else:
                                    print('Rejeita cadeia "{}"'.format(cadeia))

                elif opcao == 3: #MINIMIZAR AUTÔMATO 
                    minimizarAFD = Minimizacao.Minimizacao() 

                    minAFD = minimizarAFD.estadosEquivalentes(afd, alfabeto)

                    if not minAFD:
                        print("Esse AFD não tem como minimizar.")
                    else:
                        minafd = AF.AutomatoFD(alfabeto) #instancia o objeto para o autômato
                        for estado in minAFD['Estados']:
                            minafd.criaEstado(estado)
                        for transicao in minAFD['Transições']:
                            minafd.criaTransicao(transicao[0],minAFD['Transições'][transicao],transicao[1])
                        minafd.mudaEstadoInicial(minAFD['Estado Inicial'])
                        for final in minAFD['Estado final']:
                            minafd.mudaEstadoFinal(final, True)
                        
                        print("O automato minimizado:")
                        print(minafd)

                        salvar = input("Deseja salvar o arquivo, digite S para sim e N para não: ").upper()
                        if salvar == 'S':
                            nomeArquivo = input("\nInforme o nome que deseja dar ao arquivo. Coloque a extensão (Ex: meuAfd.txt, meuAfd.xml): ")
                            sucesso = minafd.gravaXml(nomeArquivo)
                                                
                elif opcao == 4: #SALVAR AUTÔMATO
                    nomeArquivo = input("\nInforme o nome que deseja dar ao arquivo. Coloque a extensão (Ex: meuAfd.txt, meuAfd.xml): ")
                    sucesso = afd.gravaXml(nomeArquivo)
                    if sucesso == 0:
                        print("\n*-*-*-*-* Autômato salvo com sucesso! *-*-*-*-* \n")
                    else:
                        print("Não foi possível salvar o Autômato. Tente novamente.")

        elif qtdAF == 2: #menu para o caso do usuário usar operações que demandam apenas um autômato

            print("\n-----*----- CARREGANDO AUTÔMATOS -----*-----")
            alfabeto = input("Informe o alfabeto do 1º automato: ")
            afd1 = AF.AutomatoFD(alfabeto)  # instancia o objeto para o 1º autômato
            diretorio = input("Informe o diretorio do 1º automato: ")
            afd1Xml = afd1.leXML(diretorio)  # lê o arquivo xml
            if afd1Xml is None:
                print("Não foi possível ler o arquivo.Tente novamente.")
                break
            else:
                print("\n*-*-*-*-* 1º Autômato lido com sucesso! *-*-*-*-* \n")
                afd1.carregaAFD(afd1Xml) #carrega o afd (cria os estados e as transições)

            alfabeto = input("\nInforme o alfabeto do 2º automato: ")
            afd2 = AF.AutomatoFD(alfabeto)  # instancia o objeto para o 2º autômato
            diretorio = input("Informe o diretorio do 2º automato: ")
            afd2Xml = afd2.leXML(diretorio)  # lê o arquivo xml
            if afd2Xml is None:
                print("Não foi possível ler o arquivo.Tente novamente.")
                break
            else:
                print("\n*-*-*-*-* 2º Autômato lido com sucesso! *-*-*-*-* \n")
                afd2.carregaAFD(afd2Xml) #carrega o afd (cria os estados e as transições)

            while True:
                print("\n------*------ MENU DE OPÇÕES ------*------\n"
                      "Printar autômato(s) ---------------------- 1\n"
                      "Rodar cadeia no(s) autômato(s) ----------- 2\n"
                      "Multiplicar os autômatos ----------------- 3\n"
                      "Minimizar autômatos ---------------------- 4\n"
                      "Salvar autômato(s) ----------------------- 5\n"
                      "Sair do menu de opções ------------------- 0\n")
                opcaoMult = int(input("Opção desejada: "))

                if opcaoMult == 0:  # SAIR DO MENU DE OPÇÕES
                    break

                elif opcaoMult == 1: #PRINTAR AUTÔMATOS
                    print("\n-----*----- PRINTAR AUTÔMATOS -----*-----\n"
                          "Printar o 1º autômato ------------------- 1\n"
                          "Printar o 2º autômato ------------------- 2\n"
                          "Printar os 2 autômatos ------------------ 3\n"
                          "Sair desse menu ------------------------- 0\n")
                    opPrintar = int(input("Opção desejada: "))
                    if opPrintar == 0:
                        break

                    elif opPrintar == 1:
                        print("\n----*----*----*---------------------------------------------------- 1º AUTÔMATO ------------------------------------------------------------------*----*----*----\n")
                        print(afd1)
                        print("\n----*----*----*-----------------------------------------------------------------------------------------------------------------------------------*----*----*----\n")

                    elif opPrintar == 2:
                        print("\n----*----*----*---------------------------------------------------- 2º AUTÔMATO ------------------------------------------------------------------*----*----*----\n")
                        print(afd2)
                        print("\n----*----*----*-----------------------------------------------------------------------------------------------------------------------------------*----*----*----\n")

                    elif opPrintar == 3:
                        print("\n----*----*----*---------------------------------------------------- 1º AUTÔMATO ------------------------------------------------------------------*----*----*----\n")
                        print(afd1)
                        print("\n----*----*----*---------------------------------------------------- 2º AUTÔMATO ------------------------------------------------------------------*----*----*----\n")
                        print(afd2)
                        print("\n----*----*----*-----------------------------------------------------------------------------------------------------------------------------------*----*----*----\n")

                elif opcaoMult == 2:  #RODAR CADEIAS NOS AUTÔMATOS
                    while True:
                        print("\n-----*----- INSERINDO CADEIA -----*-----\n"
                              "Inserir cadeia no 1º autômato ---------- 1\n"
                              "Inserir cadeia no 2º autômato ---------- 2\n"
                              "Sair desse menu ------------------------ 0\n")
                        opcaoCadeia = int(input("Opção desejada: "))

                        if opcaoCadeia == 0:
                            break

                        elif opcaoCadeia == 1:
                            print("----*---- RODANDO CADEIAS NO 1º AUTÔMATO ----*----")
                            cadeia = input("Digite a cadeia que deseja testar: ")
                            afd1.limpaAfd()  # inicializa o autômato
                            parada = afd1.move(cadeia)  # roda a cadeia e retorna o estado de parada
                            if afd1.deuErro():
                                print("Não foi possível rodar a cadeia. Tente novamente.")
                            else:
                                if not afd1.deuErro() and afd1.estadoFinal(parada):
                                    print('Aceita cadeia "{}"'.format(cadeia))
                                else:
                                    print('Rejeita cadeia "{}"'.format(cadeia))

                        elif opcaoCadeia == 2:
                            print("----*---- RODANDO CADEIAS NO 2º AUTÔMATO ----*----")
                            cadeia = input("Digite a cadeia que deseja testar: ")
                            afd2.limpaAfd()  # inicializa o autômato
                            parada = afd2.move(cadeia)  # roda a cadeia e retorna o estado de parada
                            if afd2.deuErro():
                                print("Não foi possível rodar a cadeia. Tente novamente.")
                            else:
                                if not afd2.deuErro() and afd2.estadoFinal(parada):
                                    print('Aceita cadeia "{}"'.format(cadeia))
                                else:
                                    print('Rejeita cadeia "{}"'.format(cadeia))

                elif opcaoMult == 3: #MULTIPLICAR AUTÔMATOS
                        print("\n---*---*--- MULTIPLICAR AUTÔMATOS ---*---*---\n")
                        print("Multiplicando os autômatos. Aguarde um momento...\n")
                        time.sleep(3)
                        alfabeto = afd1.verificaAlfabeto(afd1.alfabeto, afd2.alfabeto) #verifica se os dois autômatos possuem o mesmo alfabeto
                        if alfabeto is None:
                            print("Os autômatos devem possuir o mesmo alfabeto. Tente novamente.")
                        elif alfabeto is not None:
                            afdMulti = AF.AutomatoFD(alfabeto) #instanciando o objeto que guardará o autômato resultante da multiplicação
                            afdMulti.multiplicaAFD(afd1.estados, afd1.transicoes, afd2.estados, afd2.transicoes) #multiplicando e criando os estados e as transições do automato resultante
                            print("---*---*--- Automatos multiplicados com sucesso! ---*---*---\n\n"
                                  "Informe a operação de conjuntos que deseja realizar sobre os autômatos que foram multiplicados:\n"
                                  "União ------------------------------------- 1\n"
                                  "Intercessão ------------------------------- 2\n"
                                  "Complemento da união ---------------------- 3\n"
                                  "Complemento da intercessão ---------------- 4\n"
                                  "Complemento da diferença (AFD1 - AFD2) ---- 5\n"
                                  "Complemento da diferença (AFD2 - AFD1) ---- 6\n"
                                  "Diferença (AFD1 - AFD2) ------------------- 7\n"
                                  "Diferença (AFD2 - AFD1) ------------------- 8\n"
                                  "Sair desse menu --------------------------- 0\n")
                            operacao = int(input("Opção desejada: "))
                            afdMulti.operacoes(afd1.estados, afd1.inicial, afd1.finais, afd2.estados, afd2.inicial, afd2.finais, operacao)#define os estados finais e iniciais do autômato resultante
                            print("\n----*----*----*-------------------------------------------------------------------------------------------- AUTÔMATO RESULTANTE DA MULTIPLICAÇÃO ----------------------------------------------------------------------------------------------------*----*----*----\n")
                            print(afdMulti)
                            print("\n----*----*----*--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*----*----*----\n")
                            print("\n------*------*------ SALVAR AUTÔMATO ------*-----*-----\n"
                                  "Deseja salvar o autômato?\n"
                                  "Sim, desejo salvar esse autômato ---------------------- 1\n"
                                  "Não, voltar para o menu ------------------------------- 0\n")
                            op = int(input("Opção desejada: "))

                            if op == 1:
                                nomeArquivo = input("\nInforme o nome que deseja dar ao arquivo. Coloque a extensão (Ex: meuAfd.txt, meuAfd.xml): ")
                                sucesso = afdMulti.gravaXml(nomeArquivo)
                                if sucesso == 0:
                                    print("\n*-*-*-*-* Autômato salvo com sucesso! *-*-*-*-* \n")
                                else:
                                    print("Não foi possível salvar o Autômato. Tente novamente.")
                
                elif opcaoMult == 4: #MINIMIZAR AUTÔMATOS 
                    minimizarAFD1 = Minimizacao.Minimizacao() 

                    minAFD1 = minimizarAFD1.estadosEquivalentes(afd1, alfabeto)

                    if not minAFD1:
                        print("Esse AFD não tem como minimizar.")
                    else:
                        minafd1 = AF.AutomatoFD(alfabeto) #instancia o objeto para o autômato
                        for estado in minAFD1['Estados']:
                            minafd1.criaEstado(estado)
                        for transicao in minAFD1['Transições']:
                            minafd1.criaTransicao(transicao[0],minAFD1['Transições'][transicao],transicao[1])
                        minafd1.mudaEstadoInicial(minAFD1['Estado Inicial'])
                        for final in minAFD1['Estado final']:
                            minafd1.mudaEstadoFinal(final, True)
                        
                        print("\n----*----*----*---------------------------------------------------- 1º AUTÔMATO ------------------------------------------------------------------*----*----*----\n")
                        print(minafd1)
                        print("\n----*----*----*-----------------------------------------------------------------------------------------------------------------------------------*----*----*----\n")

                    minimizarAFD2 = Minimizacao.Minimizacao() 

                    minAFD2 = minimizarAFD2.estadosEquivalentes(afd2, alfabeto)

                    if not minAFD2:
                        print("Esse AFD não tem como minimizar.")
                    else:
                        minafd2 = AF.AutomatoFD(alfabeto) #instancia o objeto para o autômato
                        for estado in minAFD2['Estados']:
                            minafd2.criaEstado(estado)
                        for transicao in minAFD2['Transições']:
                            minafd2.criaTransicao(transicao[0],minAFD2['Transições'][transicao],transicao[1])
                        minafd2.mudaEstadoInicial(minAFD2['Estado Inicial'])
                        for final in minAFD2['Estado final']:
                            minafd2.mudaEstadoFinal(final, True)
                        
                        print("\n----*----*----*---------------------------------------------------- 2º AUTÔMATO ------------------------------------------------------------------*----*----*----\n")
                        print(minafd2)
                        print("\n----*----*----*-----------------------------------------------------------------------------------------------------------------------------------*----*----*----\n")

                        while True:
                            print("---*--- SALVAR AUTÔMATOS ---*---\n"
                                "Salvar 1º autômato ----------- 1\n"
                                "Salvar 2º autômato ----------- 2\n"
                                "Sair desse menu -------------- 0\n")
                            opSalvar = int(input("Opção desejada: "))
                            if opSalvar == 0:
                                break

                            elif opSalvar == 1:
                                nomeArquivo = input("\nInforme o nome que deseja dar ao arquivo. Coloque a extensão (Ex: meuAfd.txt, meuAfd.xml): ")
                                sucesso = minafd1.gravaXml(nomeArquivo)
                                if sucesso == 0:
                                    print("\n*-*-*-*-* Autômato salvo com sucesso! *-*-*-*-* \n")
                                else:
                                    print("Não foi possível salvar o Autômato. Tente novamente.")

                            elif opSalvar == 2:
                                nomeArquivo = input("\nInforme o nome que deseja dar ao arquivo. Coloque a extensão (Ex: meuAfd.txt, meuAfd.xml): ")
                                sucesso = minafd2.gravaXml(nomeArquivo)
                                if sucesso == 0:
                                    print("\n*-*-*-*-* Autômato salvo com sucesso! *-*-*-*-* \n")
                                else:
                                    print("Não foi possível salvar o Autômato. Tente novamente.")  

                    equivalentes = input("\nQuer saber se os dois autômatos são equivalnes, aperta S para sim e N para não: ").upper()
                    if equivalentes == 'S':
                        afdEqui = AutomatosEquivalentes.saoEquivalentes(minafd1, minafd2)
                        if afdEqui:
                            print("\nOs automatos são equivalentes.\n")
                        else:
                            print("\nOs automatos não são equivalentes.\n")
                
                elif opcaoMult == 5: #SALVAR AUTÔMATOS
                    while True:
                        print("---*--- SALVAR AUTÔMATOS ---*---\n"
                              "Salvar 1º autômato ----------- 1\n"
                              "Salvar 2º autômato ----------- 2\n"
                              "Sair desse menu -------------- 0\n")
                        opSalvar = int(input("Opção desejada: "))
                        if opSalvar == 0:
                            break

                        elif opSalvar == 1:
                            nomeArquivo = input("\nInforme o nome que deseja dar ao arquivo. Coloque a extensão (Ex: meuAfd.txt, meuAfd.xml): ")
                            sucesso = afd1.gravaXml(nomeArquivo)
                            if sucesso == 0:
                                print("\n*-*-*-*-* Autômato salvo com sucesso! *-*-*-*-* \n")
                            else:
                                print("Não foi possível salvar o Autômato. Tente novamente.")

                        elif opSalvar == 2:
                            nomeArquivo = input(
                                "\nInforme o nome que deseja dar ao arquivo. Coloque a extensão (Ex: meuAfd.txt, meuAfd.xml): ")
                            sucesso = afd2.gravaXml(nomeArquivo)
                            if sucesso == 0:
                                print("\n*-*-*-*-* Autômato salvo com sucesso! *-*-*-*-* \n")
                            else:
                                print("Não foi possível salvar o Autômato. Tente novamente.")
