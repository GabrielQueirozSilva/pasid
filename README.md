O projeto feito foi estruturado da seguinte maneira, nele existem inicialmente 2 pastas e 2 arquivos, os arquivos são o docker-compose para a crontrução inicial do projeto e o readme que explica seu funcionamento, na questão das pastas existe a pasta graficos que armazena os resultados obtivos a partir do experimento feito e a pasta src que contem a estrutura geral do projeto, a pasta src é dividida em 5 pastas internas, cada uma com um dockerfile para a estruturação do conteiner, um requeriments.txt que guarda os requerimentos necessarios para seu funcionamento e um .py que é o código python do código. As pastas internas do srv são 2 load_balancer que servem para o balanceamento do conteiner, os serviços que fazem as requesições e o source que serve para as partes dos experimentos.

Para o funcionamento correto do projeto primeiro se deve navegar ate a parte inicial e executar o comando:
 docker-build --no-cache

Apos isso é feito o uso do comando
docker compse up para o código rodar

E por fim para pegar o grafico usei isso depois do source funcionar no código:
docker cp source:/app/graficos ./graficos
