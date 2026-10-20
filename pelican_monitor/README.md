# Monitorador de Licitações - PNCP (Pelican)

Este projeto é um script em Python desenvolvido para monitorar as licitações públicas brasileiras cadastradas no [Portal Nacional de Contratações Públicas (PNCP)](https://pncp.gov.br/) que mencionem os seguintes termos:
- `pelican`
- `peli case`
- `maleta estanque pelican`

A aplicação consulta as licitações publicadas no dia e notifica novos resultados por meio do Telegram. Ele é configurado para rodar a cada 2 horas de forma automatizada usando **GitHub Actions**, salvando o estado das notificações no arquivo `processed_ids.json` e comitando essas alterações de volta ao repositório para evitar notificações repetidas.

## Estrutura do Projeto

- `monitor.py`: O script principal da aplicação que realiza as consultas na API, filtra os resultados da data corrente e notifica via Telegram.
- `requirements.txt`: Arquivo que define as dependências necessárias da aplicação.
- `processed_ids.json`: Arquivo gerado dinamicamente para armazenar os IDs dos editais já notificados.
- `../.github/workflows/pelican_monitor.yml`: O fluxo do GitHub Actions que roda o script periodicamente.

## Configuração do Telegram e GitHub Secrets

Para que as notificações do Telegram funcionem, você precisa criar um bot no Telegram, capturar as credenciais dele e configurá-las no seu repositório do GitHub (onde este projeto foi clonado).

### 1. Criar um Bot no Telegram

1. No aplicativo Telegram, procure por `@BotFather`.
2. Mande o comando `/newbot` e siga as instruções para criar um novo bot.
3. Ao finalizar, o BotFather enviará uma mensagem contendo o seu **Token**. Ele se parecerá com algo do tipo: `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ`. Guarde esse Token.
4. Para obter o seu **Chat ID** (o identificador do seu usuário ou grupo que vai receber os alertas):
   - Mande um 'Olá' para o seu bot pelo aplicativo.
   - Acesse no navegador: `https://api.telegram.org/bot<SEU_TOKEN_AQUI>/getUpdates`
   - O resultado será um JSON. Procure por `"chat":{"id": <SEU_CHAT_ID>...`. Esse número (ex: `987654321` ou `-123456789`) é o seu Chat ID.

### 2. Configurar as Secrets no GitHub

1. Vá até o seu repositório no GitHub.
2. Acesse **Settings** > **Secrets and variables** > **Actions**.
3. Clique em **New repository secret**.
4. Crie os seguintes Secrets:
   - **Nome:** `TELEGRAM_BOT_TOKEN`
     - **Valor:** O Token gerado pelo BotFather (ex: `123456789:ABCDEF...`).
   - **Nome:** `TELEGRAM_CHAT_ID`
     - **Valor:** O ID numérico do seu chat ou grupo (ex: `987654321`).

### Opcional: Como Executar Localmente

Se você deseja rodar a ferramenta em sua própria máquina, certifique-se de exportar as variáveis de ambiente antes de executar:

```bash
# Instale as dependências
pip install -r requirements.txt

# Configure o ambiente
export TELEGRAM_BOT_TOKEN="seu_token_aqui"
export TELEGRAM_CHAT_ID="seu_chat_id_aqui"

# Execute o bot
python monitor.py
```
