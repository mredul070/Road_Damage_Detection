import os 
import json

json_dir = ('E:/road_damage_detection/dataset/annotated/checked/all_jsons/set_2')
print(json_dir)
jsons = os.listdir(json_dir)
data = {}
print(jsons)
for js in jsons:
    json_data = json.load(open(os.path.join(json_dir, js)))
    print(js.split('/')[-1], " json len : ", len(json_data))
    data.update(json_data)
print("Final json len : ", len(data))
with open(json_dir+'/merged.json', 'wb') as f:
    f.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))