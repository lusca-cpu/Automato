def saoEquivalentes(minafd1, minafd2):

    trans1 = minafd1.transicoes
    trans2 = minafd2.transicoes
    final1 = minafd1.finais
    final2 = minafd2.finais
    final_equi1 = []
    final_equi2 = []

    if minafd1.alfabeto != minafd2.alfabeto:
        return False

    if minafd1.finais != minafd2.finais:
        return False

    for i in final1:
        for chaves in trans1.items():
            if i == chaves[0][0]:
                final_equi1.append(chaves)


    for i in final2:
        for chaves in trans2.items():
            if i == chaves[0][0]:
                final_equi2.append(chaves)

    if final_equi1 != final_equi2:
        return False

    return True