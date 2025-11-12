import os
from datetime import date, datetime, timedelta
import json
from colorama import init, Fore, Style # tem q instalar a bibloteca: pip install colorama
init(autoreset=True)

prioridades = ["Urgente", "Alta", "Media", "Baixa"]
mapa_prioridade = {
    "Urgente": 0,
    "Alta": 1,
    "Media": 2,
    "Baixa": 3
}

os.system('cls')
tarefas = []
tarefas_arquivadas = []
agora = datetime.now()
formato_esperado = "%d/%m/%Y"

def carregar_json_arquivada():
    '''
    carregando arquivo json arquivados dentro de um try e com with open para mais segurança
    '''

    try:
        if os.path.exists("tarefas_arquivadas.json"):
            with open("tarefas_arquivadas.json", "r", encoding='utf-8') as f:
                dados = json.load(f)
                if not dados:
                    print(f"\n {Fore.RED} === Nenhum arquivo {Style.BRIGHT}JSON arquivadas{Style.RESET_ALL}{Fore.RED} encontrado. Vamos iniciar com uma lista vazia === \n")                    
                    return []
                
                return dados
        else:
            print(f"\n {Fore.RED} === Nenhum arquivo {Style.BRIGHT}JSON arquivadas{Style.RESET_ALL}{Fore.RED} encontrado. Vamos iniciar com uma lista vazia === \n")
            return []
    except Exception as ex:
        print(f"\n-- {Fore.RED}ERRO: Ocorreu um erro inesperado em carregar {Style.BRIGHT}JSON arquivadas{Style.RESET_ALL}{Fore.RED}: {ex} [❗]\n")

def salvar_json_arquivados():
    '''
    transformando a lista de dicionários "tarefas" em um arquivo json
    '''  

    try:
        with open("tarefas_arquivadas.json", "w", encoding='utf-8') as f:
            json.dump(tarefas_arquivadas, f, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(f"\n-- {Fore.RED}ERRO: Ocorreu um erro em salvar {Style.BRIGHT}JSON arquivadas{Style.RESET_ALL}{Fore.RED}: {ex} [❗]\n")

def organizar_lista():
    '''
    Usando sort para alterar a lista original e ordenar com abse no mapa de prioridade
    '''
    if not tarefas:
        print(f"\n{Fore.RED}=== Nenhum arquivo encontrado. Vamos iniciar com uma lista vazia === \n")
        return
    
    print(f"{Fore.YELLOW}\n=== Ordenando a lista ===\n")
    tarefas.sort(key=lambda tarefa: mapa_prioridade.get(tarefa["Prioridade"], 99))
    print(f"{Fore.YELLOW}\n=== Lista Ordenada!  ===\n")

def carregar_json():
    '''
    carregando arquivo json dentro de um try e com with open
    '''

    try:
        if os.path.exists("tarefas_salvas.json"):
            with open("tarefas_salvas.json", 'r', encoding='utf-8') as f:
                dados = json.load(f)
                if not dados:
                    print(f"\n {Fore.RED} === Nenhum item encontrado em {Style.BRIGHT}JSON Tarefas{Style.RESET_ALL}{Fore.RED}s. Vamos iniciar com uma lista vazia === \n")                    
                    return []
                
                return dados
        else:
            print(f"\n {Fore.RED} === Nenhum arquivo {Style.BRIGHT}JSON tarefas{Style.RESET_ALL}{Fore.RED} encontrado. Vamos iniciar com uma lista vazia === \n")
            return []
        
    except Exception as e:
        print(f"\n-- {Fore.RED}ERRO: Ocorreu um erro inesperado em carregar {Style.BRIGHT}JSON tarefas{Style.RESET_ALL}{Fore.RED}: {e} [❗]\n")

def salvar_json():
    '''
    transformando a lista de dicionários "tarefas" em um arquivo json
    '''

    print(f"\n{Fore.GREEN}=== Salvando Tarefas ===\n")
    organizar_lista()
    try:
        with open("tarefas_salvas.json", 'w', encoding='utf-8') as f:
            json.dump(tarefas, f, indent=4, ensure_ascii=False)
            print(f"\n{Fore.GREEN}=== Tarefas salvas com sucesso [✅] ===\n")
    except IOError as e:
        print(f"\n-- {Fore.RED}ERRO: Ocorreu um erro inesperado na função salvar_json em {Style.BRIGHT}JSON tarefas{Style.RESET_ALL}{Fore.RED}: {e} [❗]\n")
        return

def criar_tarefa(nome_tarefa, descricao_tarefa, prioridade_tarefa, origem_tarefa):
    '''
    criando uma nova tafera com os parâmetros que a função recebe e adicionando a lista de tarefas com o método append
    '''
    print(F"\n {Fore.BLUE}=== Entrando na função 'Criar Tarefa' ===\n")
    tarefa = {"Nome da tarefa": nome_tarefa, "Descrição": descricao_tarefa, "Prioridade": prioridade_tarefa, "Origem": origem_tarefa, "Status": "Pendente", "Conclusão": "Não Definido"}
    tarefas.append(tarefa)
    print(f"\n{Fore.BLUE}=== Tarefa Adicionada, função concluída com sucesso. === \n")
    organizar_lista()
    return

def procurar_tarefa():
    '''
    usano um input dentro de um try para pedir o índice da tarefa que o usuário quer, e depois usando um for dentro da lista com a função enumarete
    para pegar o índice e o valor do item, se o índice for o mesmo, ele retorna a tarefa, caso não, ele não retorna nada além de um print
    '''

    print(f'''
======================
          
Você entrou na função {Fore.GREEN}"Procurar Tarefa"{Style.RESET_ALL}

{Fore.YELLOW}Digite o número da tarefa que você deseja atualizar.{Style.RESET_ALL}
          
======================''')
    relatorio()
    try: 
        indice_tarefa = int(input("Digite o número da tarefa que você está escolhendo: "))
    except Exception as e:
        print(f"\n-- {Fore.RED}ERRO: Ocorreu um erro inesperado: {e} [❗]\n")

    for indice, tarefa in enumerate(tarefas):
        if indice == indice_tarefa:
            print(f"\n {Fore.GREEN}=== Tarefa Encontrada === \n")
            return indice_tarefa
    else:
        print(f"\n{Fore.RED}=== Tarefa com índice {indice_tarefa} não existe [❗] ===")

def verificar_se_arquiva(data_realizada):
    '''
    essa função recebe a data que o usuário passou já convertida em um obj timedelta, e então ele tira a diferença
    Se a diferença for maior ou igual a 7 dias, ela é arquivada.
    '''
        
    print(f"\n {Fore.YELLOW}=== Entrando na função de Verificação de Tempo [📒] === \n")
    diferenca = agora - data_realizada

    if diferenca.days >= 7:
        print(f"\n {Fore.GREEN}=== Arquivar tarefa === \n")
        return True
    else:
        print(f"\n {Fore.GREEN}=== Não arquivar tarefa === \n")
        return None

def concluir_tarefa():
    '''
    A função concluir tarefa busca o item no topo da lista que é o item com a maior prioridade, pois foi organizado pela função organizar_lista
    e então executa ela.
    '''

    print(f"\n {Fore.YELLOW}=== Entrando na função de Concluir Tarefa [📒] === \n")
    if not tarefas:
        print(f"{Fore.RED}--ERRO: Lista está vazia [❗]")
    organizar_lista()
    verificar_urgencia()
    for tarefa in tarefas:
        if tarefa["Status"] == "Pendente":
            while True:
                print(f'''
{Fore.YELLOW}{Style.BRIGHT}Agora informe a data em que a atividade foi concluida, mas siga as orientaçôes:
A data da atividade deve ser informada desse jeito: {agora.day}/{agora.month}/{agora.year}

{Style.RESET_ALL}{Fore.BLACK}{Style.BRIGHT}Digite "sair" para cancelar.''')
                
                try:
                    data_conclusao = input(f"\n-> Quando a tarefa {Fore.GREEN}{tarefa["Nome da tarefa"]}{Style.RESET_ALL} foi realizada?: ")
                    
                    if data_conclusao == "sair":
                        print(f"\n {Fore.YELLOW}=== Saindo... === \n")
                        return
                    
                    data_objeto = datetime.strptime(data_conclusao, formato_esperado)
                    tarefa["Conclusão"] = data_conclusao
                    ver_se_arquivar = verificar_se_arquiva(data_objeto)

                    if ver_se_arquivar:
                        print(f"\n {Fore.GREEN}=== Tarefa {tarefa} arquivada === \n")
                        tarefas_arquivadas.append(tarefa)
                    break
                    
                except Exception as ex:
                    print(f"\n-- {Fore.RED}ERRO: Ocorreu um erro inesperado: {ex} [❗]\n")
                    print(f"\n{Fore.GREEN}=== Tente novamente ===\n")

            tarefa["Status"] = "Concluido"
            print(f"\n{Fore.GREEN}=== A tarefa {tarefa["Nome da tarefa"]} foi realizada ===\n")
            return
    else:
        print(f"\n{Fore.GREEN}=== Todas as Tarefas já foram realizadas [✅] ===\n")

def alterar_tarefa(ind_tarefa):
    '''
    A função alterar tarefa já recebe um parametro que é o indice da tarefa e então usamos uma estrutua de condição para ver o que o usuário quer alterar.
    Também tem um processo de validação que verifica se o nome já é o mesmo ou não
    '''

    print(f"\n {Fore.YELLOW}=== Entrando na função de Alterar Tarefa [📒] === \n")

    print(f"{Fore.GREEN}{ind_tarefa} | Nome: {tarefas[ind_tarefa]["Nome da tarefa"]} - Descrição: {tarefas[ind_tarefa]["Descrição"]} - Prioridade: {tarefas[ind_tarefa]["Prioridade"]}{Style.RESET_ALL}")
    alterar = input(f'''
======================
O que você deseja alterar?: 
                    
{Style.BRIGHT}{Fore.BLUE}1. Nome
2. Descrição
3. Prioridade{Style.RESET_ALL}
                    
======================

-> Sua escolha: ''')
    
    if alterar == "1":
        novo_nome = input("\n-> Qual vai ser o novo nome?: ").title()
        if novo_nome == tarefas[ind_tarefa]["Nome da tarefa"]:
            print(f"\n{Fore.RED}--ERRO: Escolha um novo nome.{Style.RESET_ALL}\n")
            return
        tarefas[ind_tarefa]["Nome da tarefa"] = novo_nome
        print(f"\n {Fore.GREEN} === Nome atualizado com sucesso === \n")

    elif alterar == "2":
        nova_desc = input("\n-> Qual vai ser o nova descrição?: ").title()
        if nova_desc == tarefas[ind_tarefa]["Descrição"]:
            print(f"\n{Fore.RED}--ERRO: Escolha uma nova descrição.{Style.RESET_ALL}\n")
            return
        tarefas[ind_tarefa]["Descrição"] = nova_desc
        print(f"\n {Fore.GREEN} === Descrição atualizado com sucesso === \n")

    elif alterar == "3":
        nova_prioridade = input("\n-> Qual vai ser a nova prioridade?[Urgente/Alta/Media/Baixa]: ").title()
        if nova_prioridade not in prioridades:
            print(f"\n{Fore.RED}--ERRO: Escolha uma nova prioridade válida.{Style.RESET_ALL}\n")
            return
        if nova_prioridade == tarefas[ind_tarefa]["Prioridade"]:
            print(f"\n{Fore.RED}--ERRO: Escolha uma nova prioridade não a mesma.\n")
            return
        tarefas[ind_tarefa]["Prioridade"] = nova_prioridade
        print(f"\n {Fore.GREEN} === Prioridade atualizado com sucesso === \n")
    organizar_lista()

def verificar_urgencia():
    print(f"\n{Fore.YELLOW}=== Entrando na função de Verificar Urgencia [📒] === \n")
    '''
    Usando alguns blocos de condição, separamos as tarefas por prioridades, e então imprimimos ela junto com suas informações
    '''

    cont = 0
    print(f"\n {Fore.BLUE}=== Verificando Tarefas Urgente [❗] === \n")
    for i, v in enumerate(tarefas):
        if v['Prioridade'] == "Urgente":
            print(f"{i} | Nome da Tarefa: {Fore.GREEN}{v['Nome da tarefa']}{Style.RESET_ALL} - Descrição: {Fore.GREEN}{v['Descrição']}{Style.RESET_ALL} - Prioridade: {Fore.GREEN}{v['Prioridade']}{Style.RESET_ALL}")
        else:
            cont += 1
    if cont == len(tarefas):
        print(f"{Fore.GREEN}\n === Nao há tarefas Urgentes [❌] === \n")

    print(f"\n {Fore.BLUE}=== Verificando Tarefas de prioridade Alta [❗] === \n")
    cont = 0
    for i, v in enumerate(tarefas):
        if v['Prioridade'] == "Alta":
            print(f"{i} | Nome da Tarefa: {Fore.GREEN}{v['Nome da tarefa']}{Style.RESET_ALL} - Descrição: {Fore.GREEN}{v['Descrição']}{Style.RESET_ALL} - Prioridade: {Fore.GREEN}{v['Prioridade']}{Style.RESET_ALL}")
        else:
            cont += 1
    if cont == len(tarefas):
        print(f"\n {Fore.GREEN}=== Nao há tarefas de prioridade Alta [❌] === \n")

    print(f"\n {Fore.BLUE}=== Verificando Tarefas de prioridade Media[❗]  === \n")
    cont = 0
    for i, v in enumerate(tarefas):
        if v['Prioridade'] == "Media":
            print(f"{i} | Nome da Tarefa: {Fore.GREEN}{v['Nome da tarefa']}{Style.RESET_ALL} - Descrição: {Fore.GREEN}{v['Descrição']}{Style.RESET_ALL} - Prioridade: {Fore.GREEN}{v['Prioridade']}{Style.RESET_ALL}")
        else:
            cont += 1
    if cont == len(tarefas):
        print(f"\n {Fore.GREEN}=== Nao há tarefas de prioridade Media [❌] === \n")

    print(f"\n {Fore.BLUE}=== Verificando Tarefas de prioridade Baixa [❗] === \n")
    cont = 0
    for i, v in enumerate(tarefas):
        if v['Prioridade'] == "Baixa":
            print(f"{i} | Nome da Tarefa: {Fore.GREEN}{v['Nome da tarefa']}{Style.RESET_ALL} - Descrição: {Fore.GREEN}{v['Descrição']}{Style.RESET_ALL} - Prioridade: {Fore.GREEN}{v['Prioridade']}{Style.RESET_ALL}")
        else:
            cont += 1
    if cont == len(tarefas):
        print(f"\n {Fore.GREEN}=== Nao há tarefas de prioridade baixa [❌] === \n")

def relatorio():
    '''
    A função relatório usa um bloco de condição if para verificar se a lista está vazia, se estiver, ele retorna um erro, se não estiver, ele usa um bloco de repetição
    for para iterar sobre os itens de tarefa, retornando suas informações e seu indice
    '''

    print(f"\n {Fore.YELLOW}=== Entrando na função de relatório [📒] === \n")
    if not tarefas:
        print(f"{Fore.RED}--ERRO: Lista está vazia [❗]")
        return

    print("======================")
    for indice, tarefa in enumerate(tarefas):
        print(f"N° da tarefa: {indice} | Tarefa: {tarefa['Nome da tarefa']} - Descrição: {tarefa['Descrição']} - Origem: {tarefa['Origem']} - Status: {tarefa['Status']}")
    print("======================")

def ver_arquivadas():
    '''
    A função tarefas_arquivadas usa um bloco de condição if para verificar se a lista está vazia, se estiver, ele retorna um erro, se não estiver, ele usa um bloco de repetição
    for para iterar sobre os itens arquivados, retornando suas informações e seu indice
    '''

    print(f"\n {Fore.YELLOW}=== Entrando na função Tarefas Arquivadas [📒] === \n")
    if not tarefas:
        print(f"{Fore.RED}--ERRO: Lista está vazia [❗]")
        return

    print("======================")
    for indice, tarefa in enumerate(tarefas_arquivadas):
        print(f"N° da tarefa: {indice} | Tarefa: {tarefa['Nome da tarefa']} - Descrição: {tarefa['Descrição']} - Origem: {tarefa['Origem']} - Status: {tarefa['Status']}")
    print("======================")

tarefas = carregar_json()
tarefas_arquivadas = carregar_json_arquivada()

while True:
    try:
        escolher_tarefa = input(f'''
{Fore.GREEN}Escolha uma tarefa [🔢]{Style.RESET_ALL}:

{Style.BRIGHT} {Fore.GREEN}
1. Criar tarefa.
2. Verificar Urgência.
3. Atualizar Tarefa. 
4. Concluir tarefa.
5. Excluir tarefa.
6. Relatório.
7. Relatórios Arquivados.
8. Sair.
{Style.RESET_ALL}
                            
- > {Fore.GREEN}Sua escolha: {Style.RESET_ALL}''').title()
        if escolher_tarefa == "1":
            nome_tarefa = input("- > Digite o nome da tarefa: ").title()
            descricao = input("- > De uma descrição da tarefa: ").title()
            while True:
                prioridade = input("- > Qual a prioridade?[Urgente/Alta/Média/Baixa]: ").title()
                if prioridade not in prioridades:
                    print(f"\n{Fore.RED} === Escolha uma prioridade váida [❗]===\n")
                else:
                    break
            origem = input("- > Qual a origem da tarefa?: ").title()
            criar_tarefa(nome_tarefa, descricao, prioridade, origem)
        
        elif escolher_tarefa == "2":
            verificar_urgencia()
        
        elif escolher_tarefa == "3":
            id = procurar_tarefa()
            alterar_tarefa(id)
        
        elif escolher_tarefa == "4":
            concluir_tarefa()
        
        elif escolher_tarefa == "5":
            ...
        
        elif escolher_tarefa == "6":
            relatorio()

        elif escolher_tarefa == "7":
            ver_arquivadas()
        
        elif escolher_tarefa == "8":
            if not tarefas and not tarefas_arquivadas:
                print(f"{Fore.RED}=== Finalizando ===")
                break
            elif tarefas and tarefas_arquivadas:
                salvar_json()
                salvar_json_arquivados()
                print(f"{Fore.RED}=== Finalizando ===")
                break
            elif tarefas:
                salvar_json()
                print(f"{Fore.RED}=== Finalizando ===")
                break
            elif tarefas_arquivadas:
                salvar_json_arquivados()
                print(f"{Fore.RED}=== Finalizando ===")
                break

        elif escolher_tarefa == "Teste":
            for i in tarefas:
                print(i )
        else:
            print(f"\n{Fore.RED}=== Escolha uma opção válida === \n")
    except Exception as e:
        print(f"\n-- {Fore.RED}ERRO: Ocorreu um erro inesperado: {e} [❗]\n")