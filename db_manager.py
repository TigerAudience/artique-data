import pymysql
import configparser


def insert_to_musical(musical_info_list, run_mode):
    config = configparser.ConfigParser()
    config.read(filenames=f'{run_mode}.ini')
    #config.read(filenames=f'property_deploy.ini')
    host = config['DATABASE']['HOST']
    user = config['DATABASE']['USER']
    password = config['DATABASE']['PASSWORD']
    db = config['DATABASE']['DB']
    conn = pymysql.connect(
        host=host, user=user, password=password, db=db
    )
    cursor = conn.cursor()

    query = f"INSERT INTO musical (id,begin_date,end_date,casting," \
            "genre,musical_status,name,place_name,poster_url,plot) " \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for musical_info in musical_info_list:
        pk_info = generate_pk_info(musical_info, cursor)
        '''
        pk = f"{musical_info['name']}@{musical_info['begin_date']}~{musical_info['end_date']}"
        select_pk_query = f"SELECT * FROM musical WHERE id='{pk}'"
        cursor.execute(select_pk_query)
        select_pk = cursor.fetchall()
        pk_info = {'pk': pk, 'is_exist': False}
        '''
        if pk_info['is_exist'] is True:
            continue
        data = [pk_info['pk'], musical_info['begin_date'], musical_info['end_date'], musical_info['casting'],
                musical_info['genre'], musical_info['musical_status'], musical_info['name'],
                musical_info['place_name'], musical_info['poster_url'], musical_info['plot']]
        try:
            cursor.execute(query, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f'예외가 발생했습니다. 예외 메세지 : {e}')
            exception_detail = {
                'message': e
            }


def generate_pk_info(musical_info, cursor):
    pk = musical_info['musical_pk']
    select_pk_query = f"SELECT * FROM musical WHERE id='{pk}'"
    cursor.execute(select_pk_query)
    select_pk = cursor.fetchall()
    result = {}
    if len(select_pk) != 0:
        result = {
            'is_exist': True,
            'pk': pk
        }
        return result
    result = {
        'is_exist': False,
        'pk': pk
    }
    return result
