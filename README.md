# 🕵️ Monitor Presidenciáveis Telegram

Bot do Telegram - Para a captura de dados dos canais no Telegram dos Presidenciáveis

## 📝 Estrutura dos Dados

![image](https://user-images.githubusercontent.com/6977257/181994965-d5e923a1-aca9-4064-900d-69cce56c8eb8.png)


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

#### Para EC2

##### Versão com Selenium (Método Antigo de Screenshot)
- Instale o firefox `sudo amazon-linux-extras install firefox`

##### Versão com o Imgkit (Método Novo de Screenshot + Veloz)
- Execute o comando `sudo yum -y install wget`
- Depois baixe o pacote `wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm`
- Instale o pacote `sudo yum install ./wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm`

### Capturar/Atualizar os canais monitorados

- Execute o comando `python get_groups.py` para registrar/atualizar novos canais no banco de dados.
- Execute o comando `python get_new_messages.py` para registrar/atualizar novas mensagens no banco de dados.
- Execute o comando `python send.py` para mandar os dados para o Telegram/Twitter.
- Execute o comando `python trending.py` para enviar as postagens virais diarias para o Telegram/Twitter.


### Configuração do Crontab
```sh
# Todo dia a cada 2 horas
0 */2 * * * cd /home/ec2-user/bot-presidenciaveis-telegram && ./run_all.sh

# Todo dia as 23:00 Horas
00 23 * * * cd /home/ec2-user/bot-presidenciaveis-telegram && /usr/bin/python3 trending.py >> ~/bot-presidenciaveis-telegram/trending.py 2>&1
```

### Imagens
![image](https://user-images.githubusercontent.com/6977257/179576428-fa9799c6-e776-4d1f-b321-6eaa00cfb529.png)
- Gerando uma imagem a partir da diferença do texto, sugestão @lagolucas, inspiração [nyt_diff](https://twitter.com/nyt_diff)
