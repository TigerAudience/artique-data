import pandas as pd
import numpy as np


def convert_dataframe(musical, idx):
    for idx, data in enumerate(musical):
        if isinstance(data, pd._libs.tslibs.nattype.NaTType):
            musical[idx] = None
        elif isinstance(data, float) and np.isnan(data):
            musical[idx] = None
    insert_data = {'genre': '뮤지컬', 'name': musical[1]}
    is_already_exist = musical[2]
    insert_data['musical_status'] = musical[3]
    insert_data['plot'] = musical[4]
    insert_data['begin_date'] = musical[5]
    insert_data['end_date'] = musical[6]
    insert_data['casting'] = musical[7]
    insert_data['place_name'] = musical[8]
    insert_data['poster_url'] = musical[10]
    insert_data['origin_idx'] = idx

    is_invalid = validation(insert_data, is_already_exist)

    result = {
        'is_invalid': is_invalid,
        'data': insert_data
    }
    return result


def validation(info, is_already_exist):
    res = False
    if is_already_exist is None or is_already_exist is True:
        return True
    elif info['begin_date'] is None:
        res = True
    elif info['end_date'] is None:
        res = True
    elif info['name'] is None:
        res = True
    return res
