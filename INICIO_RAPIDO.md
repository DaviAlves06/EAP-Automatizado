# 🚀 Início Rápido - Extração de Blocos EAP

## Para Usuários Windows

### Passo 1: Baixar o Projeto
- Baixe o arquivo ZIP do projeto
- Extraia o arquivo ZIP em uma pasta no seu computador

### Passo 2: Executar
- Abra a pasta onde você extraiu o projeto
- **Procure pelo arquivo `EXECUTE PARA ABRIR.bat`** (o nome deixa claro o que fazer!)
- **Clique duas vezes** no arquivo `EXECUTE PARA ABRIR.bat`
- Aguarde alguns segundos enquanto as dependências são instaladas automaticamente
- O navegador abrirá automaticamente em `http://localhost:5000`

> ⚠️ **IMPORTANTE:** O arquivo que você deve executar se chama **`EXECUTE PARA ABRIR.bat`** - o nome foi escolhido para deixar bem claro!

### Passo 3: Usar
- Arraste seu arquivo XML do MS Project para a área indicada
- (Opcional) Digite um nome para o Excel
- Clique em "Processar Arquivo"
- Baixe o Excel gerado!

## Para Usuários Linux/Mac

### Passo 1: Baixar o Projeto
- Baixe todos os arquivos do projeto para uma pasta

### Passo 2: Executar
- Abra o terminal na pasta do projeto
- Execute: `chmod +x iniciar.sh && ./iniciar.sh`
- Acesse `http://localhost:5000` no navegador

## ⚠️ Requisitos

- **Python 3.8 ou superior** instalado
  - Windows: Baixe de https://www.python.org/downloads/
  - Certifique-se de marcar "Add Python to PATH" durante a instalação
  - Linux/Mac: Geralmente já vem instalado

## ❓ Problemas?

### Python não encontrado
- Instale o Python de https://www.python.org/downloads/
- Durante a instalação, marque "Add Python to PATH"

### Erro ao instalar dependências
- Execute manualmente: `pip install flask openpyxl`

### Porta 5000 já em uso
- Feche outros programas que possam estar usando a porta 5000
- Ou altere a porta no arquivo `web_frontend.py` (última linha)

## 📝 Notas

- ✅ **Sem limites de tamanho** quando rodando localmente
- ✅ **Funciona offline** após a primeira instalação
- ✅ **Não precisa de internet** para processar arquivos
- ✅ **Totalmente gratuito** e open source

