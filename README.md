# 📄 Extração de Dados do MS Project para Excel

Este script automatiza a leitura de tarefas de um arquivo do Microsoft Project (`.mpp`) e exporta dados específicos para uma planilha Excel.

## ✅ Requisitos

Antes de executar o script, você precisa:

1. **Windows com MS Project instalado**
2. **Python 3.6+**
3. Pacotes Python:
   - `pywin32`
   - `openpyxl`

Instale os pacotes com:

```bash
pip install pywin32 openpyxl
```

---

## 📁 Como usar

### 1. **Coloque seu arquivo `.mpp`**

Altere a linha abaixo no script para o caminho do seu arquivo `.mpp`:

```python
project_file = r"C:\CAMINHO\PARA\SEU\ARQUIVO.mpp"
```

> **Exemplo real** no script:
>
> ```python
> project_file = r"C:\Users\davvi\Downloads\EAP_00953_24_1A1 - BLOCOS - 30.05.2025 1 (1) (1) 1 (1).mpp"
> ```

### 2. **Altere o nome do arquivo Excel gerado**

No final do script, localize a seguinte linha:

```python
excel_path = r"C:\Users\davvi\OneDrive\Documentos\dados_extraidos953.xlsx"
```

Para mudar o **nome do arquivo Excel gerado** ou **onde ele será salvo**, substitua esse caminho.

#### ✔️ Exemplos:

- Para salvar com outro nome:

  ```python
  excel_path = r"C:\Users\davvi\OneDrive\Documentos\blocos_relatorio.xlsx"
  ```

- Para salvar em outra pasta:

  ```python
  excel_path = r"D:\Relatorios\saida_mpp.xlsx"
  ```

> ⚠️ **Importante**: A pasta deve existir. O script **não cria pastas automaticamente**.

---

## 📝 O que o script faz?

- Abre o arquivo `.mpp` no Microsoft Project via COM.
- Busca tarefas com nomes que contenham a palavra **"bloco"**.
- Para cada bloco, procura subtarefas com os termos:
  - "obra"
  - "projeto executivo"
  - "imobilização"
- Extrai datas de início e término dessas tarefas.
- Extrai o campo personalizado **Número1** (economias previstas).
- Exporta os dados para um arquivo Excel com a seguinte estrutura:

| Bloco | Nível | Início Obras | Término Obras | Início Projeto Executivo | ... | Qtd. Econo. Previstas |
| ----- | ----- | ------------ | ------------- | ------------------------ | --- | --------------------- |

---

## 👣 Passo a passo simples para executar usando o Jupyter Notebook no VSCode

1. **Instale o Python**
   - Acesse [https://www.python.org](https://www.python.org) e baixe a versão mais recente do Python para Windows.
   - Durante a instalação, marque a opção "Add Python to PATH".

2. **Instale o Visual Studio Code (VSCode)**
   - Acesse [https://code.visualstudio.com/](https://code.visualstudio.com/) e baixe o instalador.
   - Instale o VSCode normalmente.

3. **Instale a extensão Jupyter no VSCode**
   - Abra o VSCode.
   - Vá até a aba de extensões (ícone de quadrado no menu lateral esquerdo ou `Ctrl+Shift+X`).
   - Pesquise por "Jupyter" e clique em "Instalar".

4. **Crie ou abra um notebook `.ipynb`**
   - No VSCode, clique em `File > New File` e selecione o tipo **Jupyter Notebook** ou salve um novo arquivo com a extensão `.ipynb`.
   - Copie o conteúdo do script Python para dentro de uma ou mais células no notebook.

5. **Instale os pacotes necessários (se ainda não tiver feito)**
   - Em uma célula, rode o seguinte código:

     ```python
     !pip install pywin32 openpyxl
     ```

6. **Edite os caminhos do arquivo `.mpp` e do Excel**
   - Altere os valores das variáveis `project_file` e `excel_path` conforme explicado anteriormente.

7. **Execute as células do notebook**
   - Clique em "▶" à esquerda de cada célula para executar o código passo a passo.

8. **Pronto!**
   - O Excel será criado no local definido.
   - O Microsoft Project será aberto e fechado automaticamente.

---

## 🛑 Observações importantes

- O Microsoft Project **deve estar instalado e licenciado**.
- O script **abre o MS Project de forma invisível** e o fecha automaticamente.
- O campo **"Número1"** deve estar corretamente preenchido no MS Project para ser exportado.
