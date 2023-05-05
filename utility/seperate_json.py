import json
import os

all_json_path = 'E:/road_damage_detection/dataset/annotated/checked/all_jsons/phase_1_all_img.json'

root = 'E:/road_damage_detection/dataset/annotated/checked/phase_1_all_img'

data_types = ['train', 'val'] #, 'val']
jsons = json.load(open(all_json_path))
print(len(jsons))

for data_type in data_types:
	# print(data_type)
	
	new_json = {}
	json_path = root + '/' + data_type + '.json'
	files =[i.split('/')[-1] for i in os.listdir(root + '/' + data_type)]
	print(len(files))

	for key, value in jsons.items():
		if value['filename'] in files:
			new_json[key] = value
	print(data_type, ': ', len(new_json))
	# json.dump(new_json, open(json_path, 'w'))
	with open(json_path, 'wb') as f:
		f.write(json.dumps(new_json, ensure_ascii=False).encode('utf-8'))