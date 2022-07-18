# 🕵️ Monitor Presidenciáveis Telegram

Bot do Telegram - Para a captura de dados dos canais no Telegram dos Presidenciáveis

## 📝 Estrutura dos Dados

![image](https://user-images.githubusercontent.com/6977257/178580578-ced33dda-6617-4633-b268-8ec87fbf64c4.png)

Para as tabelas **telegram_entities** e **telegram_messages** possuímos 'copia' como **\*\_changes**

### Colunas

Sendo as colunas comuns para ambas:

- **attr_name:** Indicando o nome de qual coluna foi modificada na tabela
- **old_value:** O valor anterior
- **new_value:** O Valor atual
- **date:** Data de modificação

## 🏃 Como Executar

### Primeira Configuração

- Execute o comando `pip install -r requirements.txt` para instalar as dependências;
- Adicione as informações do banco de dados no `config.json`;
- Troque a variavel `"env": "dev"` para `"env": "prod"` no arquivo `config.json` caso esteja em produção;
- Execute o comando `python run_configuration.py` para fazer o upload do banco de dados.

### Capturar/Atualizar os canais monitorados

- Execute o comando `python get_groups.py` para registrar/atualizar novos canais no banco de dados.
- Execute o comando `python get_new_messages.py` para registrar/atualizar novas mensagens no banco de dados.
- Execute o comando `python send.py` para mandar os dados para o Telegram/Twitter.
