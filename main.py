import pandas as pd
import numpy as np
import db_manager
import converter
import sys

def run_mode(args):
    if len(args) == 0:
        return 'local'
    elif args[0] == 'deploy':
        return 'deploy'
    else:
        return 'local'


def db_mode(args):
    if run_mode(args) == 'deploy':
        return 'property_deploy'
    else:
        return 'property'


def excel_mode(args):
    if run_mode(args) == 'deploy':
        return 'datas_deploy'
    else:
        return 'datas'


if __name__ == '__main__':
    argument = sys.argv
    del argument[0]			# 첫번째 인자는 main.py 즉 실행시킨 파일명이 되기 때문에 지운다
    print('Argument : {}'.format(argument))
    script_mode = db_mode(argument)
    excel_file_name = excel_mode(argument)

    df = pd.read_excel(f"./{excel_file_name}.xlsx", engine="openpyxl")
    musical_np = df.values
    musical_list = list(musical_np)
    musical_datas = []
    musical_pks_list = []
    for i, musical in enumerate(musical_list):
        converted_data = converter.convert_dataframe(musical, i)
        if converted_data['is_invalid'] is True:
            musical_pks_list.append(None)
            continue
        else:
            musical_pks_list.append(converted_data['data']['musical_pk'])
        insert_data = converted_data['data']
        # print(insert_data)
        musical_datas.append(insert_data)
    print(len(musical_datas))
    print(type(musical_datas))

    df['musical_id'] = musical_pks_list
    musical_np_tmp = df.values
    musical_list_tmp = list(musical_np_tmp)

    df.to_excel("datas.xlsx", index=False, engine="openpyxl")

    db_manager.insert_to_musical(musical_datas, run_mode=script_mode)
