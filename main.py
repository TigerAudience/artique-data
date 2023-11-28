import pandas as pd
import numpy as np
import db_manager
import converter
import sys


def run_mode(args):
    if len(args) == 0:
        return 'property'
    elif args[0] == 'deploy':
        return 'property_deploy'
    else:
        return 'property'


if __name__ == '__main__':
    argument = sys.argv
    del argument[0]			# 첫번째 인자는 main.py 즉 실행시킨 파일명이 되기 때문에 지운다
    print('Argument : {}'.format(argument))
    script_mode = run_mode(argument)

    df = pd.read_excel("./datas.xlsx", engine="openpyxl")
    musical_np = df.values
    musical_list = list(musical_np)
    musical_datas = []
    for musical in musical_list:
        converted_data = converter.convert_dataframe(musical)
        if converted_data['is_invalid'] is True:
            continue
        insert_data = converted_data['data']
        # print(insert_data)
        musical_datas.append(insert_data)
    print(len(musical_datas))
    print(type(musical_datas))

    db_manager.insert_to_musical(musical_datas, run_mode=script_mode)
