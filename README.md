# Banco de Tarefas 📚

Este é um sistema simples de gerenciamento de tarefas de linha de comando (CLI) desenvolvido em Python, com foco na persistência de dados e em uma interface de usuário colorida.

## 🛠️ Ferramentas Utilizadas

Neste projeto, foram utilizadas as seguintes ferramentas:

* ### Python
    O projeto foi inteiramente desenvolvido em Python, uma linguagem de programação moderna e poderosa, aplicando conceitos de modularidade com o uso de funções para organizar o código.

* ### 1. Biblioteca `OS`
    Esta biblioteca nativa do Python foi utilizada com duas finalidades principais:
    1.  Limpar a tela do terminal (`os.system('cls')`) para uma interface mais limpa.
    2.  Verificar a existência do arquivo de dados (`os.path.exists()`) antes de tentar carregá-lo.

* ### 2. Biblioteca `json`
    Para garantir a persistência dos dados (fazer com que as tarefas não desapareçam ao fechar o programa), esta biblioteca nativa foi usada para:
    1.  **Salvar:** Converter a lista de tarefas (uma lista de dicionários Python) em um arquivo no formato JSON (`tarefas.json`).
    2.  **Carregar:** Ler o arquivo `tarefas.json` no início da execução e convertê-lo de volta para uma lista Python.

* ### 3. Biblioteca `colorama`
    Esta biblioteca (não nativa) foi adicionada para melhorar a experiência do usuário. Sua função é puramente visual, adicionando cores e estilos ao texto do terminal, facilitando a distinção entre menus, mensagens de sucesso e alertas de erro.
    * *Para instalar: `pip install colorama`*

---
