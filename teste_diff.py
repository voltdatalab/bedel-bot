from simplediff import string_diff


change = []
change.append('message')
change.append('O Sérgio Arouca sempre me dizia que para que o povo hehehe brasileiro pudesse ter saúde, era preciso investir na promoção da qualidade de vida, garantindo acesso aos serviços de saúde, mas priorizando também o direito à alimentação de qualidade, moradia, transporte, renda, educação e lazer. Era preciso investir na prevenção de doenças com serviços de atenção básica, e organizar uma rede de saúde forte e acolhedora. E que jamais teríamos saúde se ela não fosse um direito universal e um dever do Estado garantido na Constituição.')
change.append('O Sérgio Arouca me dizia que hahahah para que o povo brasileiro pudesse ter saúde, era preciso investir na promoção da qualidade de vida, garantindo acesso aos serviços de saúde, mas priorizando também o direito à alimentação de qualidade, moradia, transporte, renda, educação e lazer. Era preciso investir na prevenção de doenças com serviços de atenção básica, e organizar uma rede de saúde forte e acolhedora. E que jamais teríamos saúde se ela não fosse um direito universal e um dever do Estado garantido na Constituição. :camera_with_flash: Ricardo Stuckert')

diff = None
if change[0] == 'message':
	diff = string_diff(change[1], change[2])



string_add = ' | '.join([' '.join(d[1]) for d in diff if d[0] == '+'])
string_del = ' | '.join([' '.join(d[1]) for d in diff if d[0] == '-'])
print(string_add)
print(string_del)
