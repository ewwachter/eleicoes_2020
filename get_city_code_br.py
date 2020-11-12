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
	mun_uf = "?"
	for UF in data['abr']:
		# print(UF['cd'])
		for mun in UF['mu']:
			try: 
				if mun['nm'] == mun_name:
					mun_code = mun['cd']
					mun_uf = UF['cd']
			except:
				print("-")
				# print(mun['nm'])

	return mun_code,mun_uf


#defines
COD_ELEICAO="426"
BASE_URL="https://resultados.tse.jus.br/oficial/ele2020/divulgacao/oficial/"+COD_ELEICAO+"/"

URL_MUN = BASE_URL+"config/mun-e"+"{:06d}".format(int(COD_ELEICAO))+"-cm.json"
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



print(URL_MUN)

res_cd, res_uf = get_mun_code(URL_MUN,mun_name)
print(mun_name,"-",res_uf)
print("código:",res_cd)


