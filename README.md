# eleicoes_2020
python para acompanhar resultados eleições 2020 via API do TSE.
Dados iniciais configurados para a simulação executada pelo TSE. Mais informações no link: https://www.tse.jus.br/eleicoes/eleicoes-2020/interessados-na-divulgacao-de-resultados

configuração para o simulado:
COD_ELEICAO="8334"
BASE_URL="https://resultados.tse.jus.br/publico/ele2020/divulgacao/simulado/"+COD_ELEICAO+"/"


# Como executar

- Primeiro descubra o código do município. Por exemplo, para procurar o código da cidade de Três de Maio:

python get_city_code_br.py -n "TRÊS DE MAIO"


 - Com o código da cidade, pegue os resultados para prefeito (exemplo cidade do Rio de Janeiro - RJ)

python get_results_plot.py -uf rj -m 60011


- Para os resultados para vereador (exemplo cidade do Rio de Janeiro - RJ)

python get_results_plot.py -uf rj -m 60011 -v
