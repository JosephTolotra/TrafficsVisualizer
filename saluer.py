from cloudpickle import load
from tensorflow.keras.models import model_from_json 
import pandas as pd
import tensorflow as tf
import numpy as np

def  predict(df):
	col_transfer = ['ts','td','sa','sp','da','dp','pr','ibyt','ipkt','flg','Label']
	contains_no_matching_flows = (df == 'No matching flows').any().any()	
	if df.empty:
		print('TRue')
		df_final = pd.DataFrame(columns=col_transfer)
	elif contains_no_matching_flows:
		print('No matching flows')
		df_final = pd.DataFrame(columns=col_transfer)
	else:
		#Import process
		process = load(open('/home/ornella/modele/processing.pkl','rb'))

		# load json and create model
		json_file = open('/home/ornella/modele/model.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		model = model_from_json(loaded_model_json)

		# load weights into new model
		model.load_weights('/home/ornella/modele/model.weights.h5')
		print("Loaded model from disk")	
	
		#Copy dataframe	
		#df_final = df.copy()
	
		#Get columns needed
		columns_needed = ['sa', 'sp', 'da', 'dp', 'pr','ibyt',  'ipkt','flg','td', 'ts']
		df = df[columns_needed]
		print(df)

		columns = ['IPV4_SRC_ADDR', 'L4_SRC_PORT', 'IPV4_DST_ADDR', 'L4_DST_PORT',\
 		'PROTOCOL', 'IN_BYTES',  'IN_PKTS',  'TCP_FLAGS','FLOW_DURATION_MILLISECONDS','ts']
		df.columns = columns
		#df = pd.DataFrame(df, columns=columns)

		#Change value of tcp flags and protocol
		df['TCP_FLAGS'] = df['TCP_FLAGS'].replace('...A....',0)
	
		df['PROTOCOL'] = df['PROTOCOL'].replace('ICMP',1)
		df['PROTOCOL'] = df['PROTOCOL'].replace('UDP',17)
		df['PROTOCOL'] = df['PROTOCOL'].replace('TCP',16)


		#Adress source
		df[['IPV4_SRC_ADDR_network1','IPV4_SRC_ADDR_network2','IPV4_SRC_ADDR_hote1',\
		'IPV4_SRC_ADDR_hote2']]=df['IPV4_SRC_ADDR'].str.split('.', expand=True)
		df = process['target_encoding_src_network1'].merge(df, on='IPV4_SRC_ADDR_network1')
		df = process['target_encoding_src_network2'].merge(df, on='IPV4_SRC_ADDR_network2')
		df = process['target_encoding_src_hote1'].merge(df, on='IPV4_SRC_ADDR_hote1')
		df = process['target_encoding_src_hote2'].merge(df, on='IPV4_SRC_ADDR_hote2')

		#Destinaton adress
		df[['IPV4_DST_ADDR_network1','IPV4_DST_ADDR_network2','IPV4_DST_ADDR_hote1',\
		'IPV4_DST_ADDR_hote2']]= df['IPV4_DST_ADDR'].str.split('.', expand=True)
		df = process['target_encoding_dst_network1'].merge(df, on='IPV4_DST_ADDR_network1')
		df = process['target_encoding_dst_network2'].merge(df, on='IPV4_DST_ADDR_network2')
		df = process['target_encoding_dst_hote1'].merge(df, on='IPV4_DST_ADDR_hote1')
		df = process['target_encoding_dst_hote2'].merge(df, on='IPV4_DST_ADDR_hote2')

		#Deal with src port address
		df = process['target_encoding_l4_src_port'].merge(df, on='L4_SRC_PORT')

		#Deal with dst port address
		df = process['target_encoding_l4_dst_port'].merge(df, on='L4_DST_PORT')

		#Deal with protocol
		df= process['target_encoding_protocol'].merge(df, on='PROTOCOL')

		#Deal with tcp_flags
		df= process['target_encoding_tcp_flags'].merge(df, on='TCP_FLAGS')
	
		#Copy dataframe 
		df_final = df.copy()
		df_final = df[columns]
		df_final.columns = ['sa', 'sp', 'da', 'dp', 'pr','ibyt',  'ipkt','flg','td', 'ts']

		#Drop col
		drop_col = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR',  'TCP_FLAGS', 'PROTOCOL', 
		'L4_DST_PORT', 'L4_SRC_PORT', 'IPV4_DST_ADDR_hote2','IPV4_DST_ADDR_hote1','IPV4_DST_ADDR_network2',
		'IPV4_DST_ADDR_network1', 'IPV4_SRC_ADDR_hote2','IPV4_SRC_ADDR_hote1', 'IPV4_SRC_ADDR_network2',
		'IPV4_SRC_ADDR_network1','ts']
		df = df.drop(columns=drop_col)

		#Standard scaler
		df_scaled = process['stdScaler'].transform(df)

		#Prediction
		reconstruction_result = model.predict(df_scaled)
		loss = tf.keras.losses.mae(reconstruction_result, df_scaled)

		threshold = process['threshold']
		outliers = loss > threshold

		#print(df_final[columns_needed])

        	#Insert value 0 or 1 to column of 'Label' of df_final to return 
		for index, element in enumerate(outliers):
			a = element.numpy().any().astype(int)
			df_final.loc[index,'Label'] = a
	
		#col_transfer = ['ts','td','sa','sp','da','dp','pr','ibyt','ipkt','flg','Label']	
		
		#Mettre à jour liste_packets.csv
		df_liste_packet_csv = pd.read_csv('liste_packets.csv')
		df_liste_packets_a_jour = pd.concat([df_liste_packet_csv,df_final[col_transfer]], ignore_index=True)

		#Enregistrer le nouveau fichier liste_packets.csv
		df_liste_packets_a_jour.to_csv('liste_packets.csv', index=False)
	
	return df_final[col_transfer]

#values = [['192.168.60.100', 65, '192.168.40.2', 357,  6, 10, 10, 0, 15360], 
#          ['192.168.60.2', 65, '192.168.40.2', 357,  6, 10, 10, 0, 15360],
#         ['192.168.50.2', 65, '192.168.40.2', 357,  6, 10, 10, 0, 15360],
#         ['192.168.50.100', 65, '192.168.60.100', 357,  6, 10, 10, 0, 15360]]

#columns = ['IPV4_SRC_ADDR', 'L4_SRC_PORT', 'IPV4_DST_ADDR', 'L4_DST_PORT',\
#    'PROTOCOL', 'IN_BYTES',  'IN_PKTS',  'TCP_FLAGS','FLOW_DURATION_MILLISECONDS']


#df = pd.DataFrame(values, columns=columns)
#df = pd.read_csv('test_csv.csv')
#print(predict(df))
