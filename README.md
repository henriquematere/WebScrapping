Automatizador de Busca de Odds na Bet365
Projeto pessoal para facilitar a análise de apostas esportivas

Criei esse robô para automatizar a busca por odds específicas no site da Bet365.

Ele faz o seguinte:

1. Acessa o site da Bet365 e lida com os popups iniciais
2. Navega até a seção de futebol automaticamente
3. Encontrar jogos específicos que eu quero analisar
4. Localizar as odds de mercados específicos (como Over 1.5 gols)


Fiz esse programa para integrar com um outro que já está funcionando, ele servirá para buscar as melhores odds de todas as casas esportivas para calcular possibilidade de arbitragem.


Usei Python com Selenium para:

1. Controlar um navegador automático
2. Esperar os elementos carregarem (com waits inteligentes)
3. Lidar com os desafios do site (como CAPTCHAs que exigem intervenção humana)

O principal problema encontrado foi o CAPTCHA que atrapalha a automação.

Foi um primeiro contato com web scraping em sites.

📝 Como usar
Instalar o Selenium

Configurar o jogo e odd que quer buscar

Rodar o script e resolver o CAPTCHA se aparecer

O robô faz o resto e mostra a odd encontrada
