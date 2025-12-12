# 📄 Extração de Dados do MS Project para Excel

Aplicação web para automatizar a leitura de tarefas de um arquivo do Microsoft Project (`.mpp`) e exportar dados específicos para uma planilha Excel. A aplicação funciona através de uma interface web moderna que aceita arquivos XML exportados do MS Project.

## ✅ Requisitos

### Para uso local:
1. **Python 3.8+**
2. **Pacotes Python:**
   - `flask`
   - `openpyxl`

Instale os pacotes com:
```bash
pip install flask openpyxl
```

### Para exportar XML do MS Project:
- **Microsoft Project instalado** (para exportar o arquivo `.mpp` para XML)

---

## 🚀 Como usar a aplicação web

### Opção 1: Uso local

1. **Instale as dependências:**
   ```bash
   pip install flask openpyxl
   ```

2. **Execute a aplicação:**
   ```bash
   python web_frontend.py
   ```

3. **Acesse no navegador:**
   - Abra `http://localhost:5000`

4. **Use a interface:**
   - Arraste e solte o arquivo XML ou clique para selecionar
   - (Opcional) Digite um nome personalizado para o arquivo Excel
   - Clique em "Processar Arquivo"
   - Aguarde o processamento
   - Baixe o arquivo Excel gerado

### Opção 2: Uso na Vercel (compartilhamento fácil)

A aplicação está configurada para deploy na Vercel, permitindo compartilhamento fácil com outros usuários.

**Para fazer deploy:**
1. Faça push do código para um repositório GitHub
2. Conecte o repositório na Vercel
3. A Vercel detectará automaticamente a configuração e fará o deploy
4. Compartilhe o link da aplicação com sua equipe

---

## 📤 Como extrair XML do arquivo .mpp

Antes de usar a aplicação web, você precisa exportar seu arquivo `.mpp` para XML no Microsoft Project. Siga estes passos:

### Passo a passo para exportar XML:

1. **Abra o Microsoft Project**
   - Inicie o Microsoft Project
   - Abra o arquivo `.mpp` que deseja processar

2. **Acesse o menu de exportação:**
   - Clique em **Arquivo** (File) no menu superior
   - Selecione **Salvar Como** (Save As) ou **Exportar** (Export)

3. **Configure a exportação:**
   - Na janela de salvar, altere o tipo de arquivo para **XML** ou **XML Project** (dependendo da versão do MS Project)
   - Escolha um local para salvar o arquivo
   - Digite um nome para o arquivo (ex: `projeto_eap.xml`)
   - Clique em **Salvar** (Save)

4. **Confirme a exportação:**
   - Se aparecer alguma janela de confirmação, clique em **OK** ou **Salvar**
   - O arquivo XML será gerado no local escolhido

5. **Pronto!**
   - Agora você pode usar este arquivo XML na aplicação web

> 💡 **Dica:** O arquivo XML geralmente é muito menor que o `.mpp` e contém todas as informações necessárias para a extração.

---

## 📝 O que a aplicação faz?

A aplicação processa o arquivo XML exportado do MS Project e:

- ✅ Busca tarefas com nomes que contenham a palavra **"bloco"**
- ✅ Para cada bloco, procura subtarefas com os termos:
  - "obra"
  - "projeto executivo"
  - "imobilização"
- ✅ Extrai datas de início e término dessas tarefas
- ✅ Extrai o campo personalizado **Número1** (economias previstas)
- ✅ Exporta os dados para um arquivo Excel com a seguinte estrutura:

| Bloco | Nível | Início Obras | Término Obras | Início Projeto Executivo | Término Projeto Executivo | Início Imobilização | Término Imobilização | Início Bloco | Término Bloco | Qtd. Econo. Previstas |
| ----- | ----- | ------------ | ------------- | ------------------------ | ------------------------- | ------------------- | -------------------- | ------------ | ------------- | --------------------- |

---

## 🎯 Passo a passo completo de uso

### 1️⃣ Exportar XML do MS Project
1. Abra o arquivo `.mpp` no Microsoft Project
2. Vá em **Arquivo > Salvar Como**
3. Selecione o formato **XML** ou **XML Project**
4. Salve o arquivo (ex: `meu_projeto.xml`)

### 2️⃣ Acessar a aplicação
- **Local:** Abra `http://localhost:5000` no navegador
- **Vercel:** Acesse o link fornecido pela Vercel

### 3️⃣ Fazer upload do arquivo
1. Na página web, você verá uma área de "arrastar e soltar"
2. Arraste o arquivo XML para a área ou clique para selecionar
3. (Opcional) Digite um nome personalizado para o arquivo Excel no campo "Nome do Excel"
4. Clique em **"Processar Arquivo"**

### 4️⃣ Aguardar processamento
- A aplicação processará o arquivo
- Você verá uma mensagem mostrando a quantidade de blocos encontrados
- Exemplo: *"✅ Processamento concluído! Encontrados 15 blocos."*

### 5️⃣ Baixar o Excel
- Após o processamento, aparecerá um botão para baixar o arquivo Excel
- Clique em **"Download do Excel"**
- O arquivo será baixado com o nome especificado (ou um nome automático com timestamp)

---

## 🔧 Estrutura do projeto

```
EAP Automação/
├── web_frontend.py      # Aplicação Flask principal
├── api/
│   └── index.py         # Handler para Vercel
├── vercel.json          # Configuração do deploy Vercel
├── requirements.txt     # Dependências Python
├── app.py              # Script original (para referência)
└── README.md           # Este arquivo
```

---

## 🛑 Observações importantes

- ✅ A aplicação **não requer MS Project instalado** no servidor (apenas para exportar o XML)
- ✅ O arquivo XML deve ser exportado corretamente do MS Project
- ✅ O campo **"Número1"** deve estar preenchido no MS Project para aparecer no Excel
- ✅ A aplicação processa apenas arquivos `.xml` (não aceita `.mpp` diretamente)
- ✅ Arquivos temporários são limpos automaticamente após o processamento

---

## 🐛 Solução de problemas

### Erro: "Envie um arquivo XML exportado do MS Project"
- **Solução:** Certifique-se de que exportou o arquivo `.mpp` para XML no MS Project antes de fazer upload

### Erro: "Nenhum bloco encontrado"
- **Solução:** Verifique se as tarefas no MS Project contêm a palavra "bloco" no nome

### Erro no deploy da Vercel
- **Solução:** Verifique se o arquivo `vercel.json` está configurado corretamente e se todas as dependências estão no `requirements.txt`

---

## 📞 Suporte

Em caso de dúvidas ou problemas, entre em contato com:
- **Davi Alves CT895/24 - 1B1**

---

## 📄 Versão anterior (script local)

Se você preferir usar o script Python original que funciona diretamente com arquivos `.mpp` (requer MS Project instalado), consulte o arquivo `app.py` e siga as instruções comentadas no código.
