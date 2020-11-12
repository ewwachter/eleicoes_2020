import requests, json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse



def get_mun_name(url, cod_mun):
	r = requests.get(url)
	data = r.json()
	# print(json.dumps(data, indent=4, sort_keys=True))	

	mun_name = "not found"
	for UF in data['abr']:
		# print(UF['cd'])
		for mun in UF['mu']:
			try: 
				if int(mun['cd']) == cod_mun:
					mun_name = mun['nm']
					uf_name = UF['cd']
			except:
				print("-")

	return mun_name,uf_name


def get_data(url):
	r = requests.get(url)
	data = r.json()

	# print(json.dumps(data, indent=4, sort_keys=True))

	print("############################")
	print(data['dt'],data['ht'])
	last_update = data['dt'],data['ht']
	mun_name, uf = get_mun_name(URL_UF,int(data['cdabr']))
	print("código município: ",data['cdabr'])
	print("nome município: ",mun_name, "-", uf)
	mun_name = mun_name + " - " + uf

	print("----------------------------")
	if (data['tf'] == 's'):
		print("TOTALIZAÇÃO FINAL")
	else:
		print("totalização parcial")
	print("seções totalizadas",data['pst'],"% (",data['st'],"/",data['s'],")")
	# print("seções totalizadas",data['st'],"/",data['s'],")")
	print("----------------------------")

	result_sec = []
	my_dict={}
	my_dict['sec_totalizadas']=data['st']
	my_dict['sec']=data['s']
	my_dict['sec_perc']=data['pst']
	result_sec.append(my_dict)

	eleitorado = []
	my_dict={}
	my_dict['total_eleitores']=data['e']
	my_dict['eleitores_nao_apurados']=data['ena']
	my_dict['perc_eleitorado_apurado']=data['pea']
	my_dict['perc_comparecimento']=data['pc']
	print(my_dict)
	eleitorado.append(my_dict)

	result = []
	for item in data['cand']:
		my_dict={}
		# my_dict['nr_candidato']=item.get('n')

		if(item.get('e')=="s"):
			my_dict['nome_candidato']=item.get('nm')+"\nELEITO!"
		else:
			my_dict['nome_candidato']=item.get('nm')
		my_dict['percentual']=float (item.get('pvap').strip().replace(",", "."))
		my_dict['nr_votos']=item.get('vap')
		my_dict['eleito']=item.get('e')
		# print(my_dict)
		result.append(my_dict)

	result = sorted(result, key=lambda k: k['nr_votos'])

	print("brancos",data['vb']," - ",data['pvb'],"%")
	my_dict={}
	my_dict['nome_candidato']="brancos"
	my_dict['nr_votos']=data['vb']
	my_dict['percentual']=data['pvb']
	result.insert(0,my_dict)

	print("nulos",data['tvn']," - ",data['ptvn'],"%")
	my_dict={}
	my_dict['nome_candidato']="nulos"
	my_dict['nr_votos']=data['tvn']
	my_dict['percentual']=data['ptvn']
	result.insert(0,my_dict)
	for i in result:
		print(i.values())
	return result,result_sec,last_update,mun_name,eleitorado

def animate(i):

	result_candidatos,secoes,last_update,mun_name,eleitorado = get_data(URL_CIDADE)
	
	title = mun_name + "\n" + last_update[0] + " - " + last_update[1]
	plt.suptitle(title, fontsize=20)
	# fig.title(title, fontsize=20, ha='center')

	perc_cand = [ sub['percentual'] for sub in result_candidatos ]
	perc_cand = perc_cand[-15:]
	# print(perc_cand)

	votos_cand = [ sub['nr_votos'] for sub in result_candidatos ]
	votos_cand = votos_cand[-15:]
	# print(votos_cand)

	name_cand = [ sub['nome_candidato'] for sub in result_candidatos ]
	name_cand = name_cand[-15:]
	# print(name_cand)

	y_pos = np.arange(len(name_cand))
	# print(y_pos)
	axs[0].barh(y_pos, votos_cand, align='center',color="dodgerblue")
	axs[0].set_yticks(y_pos)
	try:
		axs[0].set_xlim(0,max(votos_cand)*1.2)
	except:
		pass
	axs[0].set_yticklabels(name_cand)
	total_eleitores = [ sub['total_eleitores'] for sub in eleitorado ]
	eleitores_nao_apurados = [ sub['eleitores_nao_apurados'] for sub in eleitorado ]
	perc_eleitorado_apurado = [ sub['perc_eleitorado_apurado'] for sub in eleitorado ]
	perc_comparecimento = [ sub['perc_comparecimento'] for sub in eleitorado ]
	axs[0].set_xlabel("Total Eleitores:"+str(total_eleitores[0])+
						"\nVotos Apurado:"+str(perc_eleitorado_apurado[0])+
						"%\nVotos Não Apurados:"+str(eleitores_nao_apurados[0])+
						"\nComparecimento:"+str(perc_comparecimento[0])+"%"
						 )

	i=0
	if(axs[0].texts == []):
		for perc in perc_cand:
			axs[0].text(votos_cand[i], i, (str(votos_cand[i])+"\n"+str(perc)+"%"), color='red', fontweight='bold')
			i=i+1
		txt_perc=axs[1].text(0,0,"", color='red', fontweight='bold', horizontalalignment='center')
	else:
		for tx in axs[0].texts:			
			tx.set_position((votos_cand[i], i))
			tx.set_text(str(str(votos_cand[i])+"\n"+str(perc_cand[i])+"%"))
			i=i+1

	#secoes

	totalizadas = [ sub['sec_totalizadas'] for sub in secoes ]
	sec = [ sub['sec'] for sub in secoes ]
	sec_perc = [ sub['sec_perc'] for sub in secoes ]
	print("sec_perc:",sec_perc)
	
	axs[1].bar("0", totalizadas, width=0.2, label='Seções Totalizadas')
	axs[1].bar("0", int(sec[0])-int(totalizadas[0]), width=0.2, bottom=totalizadas, color="lightgray")
	axs[1].get_xaxis().set_ticks([])
	try:
		axs[1].set_ylim(0,sec[0]*1.1)
	except:
		pass
	axs[1].set_xlabel("Seções Apuradas:"+str(totalizadas[0])+"\nTotal Seções:"+str(sec[0]))

	axs[1].texts[0].set_position((0, totalizadas[0]))
	axs[1].texts[0].set_text(sec_perc[0]+"%")

#defines
# COD_ELEICAO_SIM="8334"
# BASE_URL_SIM="https://resultados.tse.jus.br/publico/ele2020/divulgacao/simulado/"+COD_ELEICAO_SIM+"/"
# COD_ELEICAO=COD_ELEICAO_SIM
# BASE_URL=BASE_URL_SIM

COD_ELEICAO="426"
BASE_URL="https://resultados.tse.jus.br/oficial/ele2020/divulgacao/oficial/"+COD_ELEICAO+"/"

URL_UF = BASE_URL+"config/mun-e"+"{:06d}".format(int(COD_ELEICAO))+"-cm.json"
#################

parser = argparse.ArgumentParser()
parser.add_argument('-uf', action='store',
                    dest='uf_code',
                    default='rs',
                    help='UF do município')
parser.add_argument('-m', action='store',
                    dest='mun_code',
                    default='88013',
                    help='código do município')
parser.add_argument('-v', action='store_true',
                    dest='cargo',
					help='vereador ou prefeito')
args = parser.parse_args()

mun_code = args.mun_code
uf_code = args.uf_code
if(args.cargo):
	cargo="0013"
	print("vereador")
else:
	cargo="0011"
	print("prefeito")


print("URL_UF:",URL_UF)
URL_CIDADE = BASE_URL+"dados-simplificados/"+uf_code+"/"+uf_code+mun_code+"-c"+cargo+"-e"+"{:06d}".format(int(COD_ELEICAO))+"-r.json"
print("URL_CIDADE:",URL_CIDADE)


fig, axs = plt.subplots(1,2,gridspec_kw={'width_ratios': [6, 1]})

ani = animation.FuncAnimation(fig, animate, interval=60000)

fig.set_size_inches(10, 15, forward=True)

plt.show()