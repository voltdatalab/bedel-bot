cd ~/bot-presidenciaveis-telegram &&
echo "Atualizando Grupos" &&
/usr/bin/python3 get_groups.py >> ~/bot-presidenciaveis-telegram/get_groups.log 2>&1 &&
echo "Atualizando Mensagens" &&
/usr/bin/python3 get_new_messages.py >> ~/bot-presidenciaveis-telegram/get_new_messages.log 2>&1 &&
echo "Enviando Coisas" &&
/usr/bin/python3 send.py >> ~/bot-presidenciaveis-telegram/send.log 2>&1 &&