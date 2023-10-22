import datetime
import os
import json


def preprocessing_exp_upload(files, data_store):
    try:
        filename = files[0].filename.split('/')[0] + '.json'
        items = []
        for file in files:
            fn = file.filename.replace('Predata', 'PreData').replace('Postdata', 'PostData').replace('Prozess', 'Process')
            items.append(fn.split('/'))
        
        data_by_second_element = {}

        for item in items:
            key = item[1] 
            if key in data_by_second_element:
                data_by_second_element[key].append(item)
            else:
                data_by_second_element[key] = [item]

        classified_data_by_third_element = {}
        for key, items in data_by_second_element.items():
            classified_data_by_third_element[key] = {} 
            for item in items:
                third_key = item[2]
                if third_key in classified_data_by_third_element[key]:
                    classified_data_by_third_element[key][third_key].append(item)
                else:
                    classified_data_by_third_element[key][third_key] = [item]
        
        for versuch_index in classified_data_by_third_element:
            for versuch_value in classified_data_by_third_element[versuch_index]:
                if versuch_value == 'PreData':
                    for ii, cc in enumerate(classified_data_by_third_element[versuch_index][versuch_value]):
                        classified_data_by_third_element[versuch_index][versuch_value][ii] = cc[3].rsplit('.', 1)[0]
                else:
                    data_by_tf_element = {}

                    for ii, cc in enumerate(classified_data_by_third_element[versuch_index][versuch_value]):
                        if cc[3] in data_by_tf_element:
                            data_by_tf_element[cc[3]].append(cc[4].rsplit('.', 1)[0])
                            data_by_tf_element[cc[3]] = list(set(data_by_tf_element[cc[3]]))
                        else:
                            data_by_tf_element[cc[3]] = [cc[4].rsplit('.', 1)[0]]
                    classified_data_by_third_element[versuch_index][versuch_value] = data_by_tf_element
        
        for versuch_index in classified_data_by_third_element:
            for versuch_value in classified_data_by_third_element[versuch_index]:
                if versuch_value != 'PreData':
                    if 'PreData' in classified_data_by_third_element[versuch_index]:
                        classified_data_by_third_element[versuch_index][versuch_value]['PreData'] = classified_data_by_third_element[versuch_index]['PreData']
        contents = {}
        for i, versuch_index in enumerate(classified_data_by_third_element):
            if 'PreData' in classified_data_by_third_element[versuch_index]:
                del classified_data_by_third_element[versuch_index]['PreData']
            probe = {}
            for ii, sample_index in enumerate(classified_data_by_third_element[versuch_index]):
                classified_data_by_third_element[versuch_index][sample_index]['Sample ID'] = sample_index
                probe[f'Probe {ii+1}'] = classified_data_by_third_element[versuch_index][sample_index]
            classified_data_by_third_element[versuch_index] = probe
            classified_data_by_third_element[versuch_index]['Versuche ID'] = versuch_index
            contents[f'Versuch {i+1}'] = classified_data_by_third_element[versuch_index]
        
        for versuch in contents:
            for probe in contents[versuch]:
                for detail in contents[versuch][probe]:
                    if detail == 'Process' or detail == 'CPA':
                        contents[versuch][probe][detail] = contents[versuch][probe][detail][0]
        
        for versuch_id, versuch_data in contents.items():
            for probe_id, probe_data in versuch_data.items():
                for task in ['CPA', 'Process']:
                    if task in probe_data:
                        probe_data[f"{task} ID"] = probe_data.pop(task)
                for task in ['PreData', 'PostData']:
                    if task in probe_data:
                        probe_data[f"{task} ID"] = sorted(probe_data.pop(task))

        with open(f'{data_store}/Experiment/{filename}', 'wb') as f:
            f.write(json.dumps(contents).encode('utf-8'))

        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON GENERATE EXP DATA: {filename} \n")
        return {'file_name': filename, 'result': 'success', 'neo4j': 'waiting'}


    except Exception as e:
        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON GENERATE EXP DATA: {filename}: {e} \n")
        return {'file_name': filename, 'result': 'error', 'neo4j': 'undo'}
