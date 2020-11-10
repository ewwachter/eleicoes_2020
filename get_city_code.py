import requests, json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse



def get_mun_code(url, mun_name):
	r = requests.get(url)
	data = r.json()
	# print(json.dumps(data, indent=4, sort_keys=True))	

	mun_code = "not found"
	for item in data['abr']:
		try: 
			if item['nmabr'] == mun_name:
				mun_code = item['cdabr']
		except:
			print("-")

	return mun_code


#defines
COD_ELEICAO="8334"
BASE_URL="https://resultados.tse.jus.br/publico/ele2020/divulgacao/simulado/"+COD_ELEICAO+"/"
#################

parser = argparse.ArgumentParser()
parser.add_argument('-uf', action='store',
                    dest='uf_code',
                    default='rs',
                    help='UF do município')
parser.add_argument('-n', action='store',
                    dest='mun_name',
                    default='rs',
                    help='nome do município')
args = parser.parse_args()
mun_name = args.mun_name
uf_code = args.uf_code



url_mun = BASE_URL+"dados/"+uf_code+"/"+uf_code+"-c0011-e00"+COD_ELEICAO+"-e.json"



print("código:",get_mun_code(url_mun,mun_name))


