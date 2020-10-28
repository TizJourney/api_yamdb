#! python
# coding: utf-8

# Первая строчка на называется shebang. Погулите, что это.
# Вторая строчка выставляет в кодировку кода скрипта в utf-8 
# но в python 3 кодировка по умолчанию и так utf-8, поэтому в этом скрипте
# эта строчка бессмысленна. Но в старых скриптах для python 2 она постоянно
# встречается

import argparse
import csv
import sqlite3
import sys

BASE_DEFAULT_PATH = './data'

# конфиг отображения таблиц базы данных в csv файлы
# название для таблицы можно подсмотреть так: python manage.py inspectdb
TABLE_CONFIG = {
    'api_yamdbuser': 'users',
    'api_title': 'titles',
    'api_review': 'review',
    'api_comment': 'comments',
}

def prepare_db_data(filename):
    with open(filename, 'r', encoding='utf8') as read_csv:
        # csv.DictReader использует первую строку в файле для header
        # запятая - разделитель по умолчанию
        dr = csv.DictReader(read_csv)

        # строим соответствие имён в данных и модели
        # и фильтруем по поляем, которые хотим использовать
        database_fields = dr.fieldnames
        database_data = []
        for row in dr:
            database_data.append(
                [
                    row[row_key] for row_key in database_fields
                ]
            )
    return database_fields, database_data


def main(options):
    cur = None

    if not options.dummy:
        con = sqlite3.connect(options.database)
        cur = con.cursor()
    else:
        print(f'Открываем базу {options.database}')
    
    for key, filename in TABLE_CONFIG.items():
        print(f'Запуск скрипта для {key}')
        full_path = f'{options.data}/{filename}.csv'
        headers, data = prepare_db_data(full_path)
        str_q =  ','.join('?' * len(headers))
        
        # добавляем запись(INSERT) или пропускаем(IGNORE), если она уже есть в базе данных
        command = f'INSERT OR IGNORE INTO {key} {tuple(headers)} VALUES ({str_q})'
        if not options.dummy:
            cur.executemany(command, data)
        else:
            # поддержка режима холостого запуска
            # вместо запуска команд просто печатаем их на экран            
            print(command)
            for item in data:
                print(item)

    if not options.dummy:
        con.commit()
        con.close()
    else:
        print(f'Закрываем базу')

def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description='Скрипт для заливки данных в тестовую базу данных из csv файлов')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--dummy', help='Режим холостого запуска', action='store_true')
    parser.add_argument(
        '--database', help='Путь до базы данных для заливки данных. По умолчанию: db.sqlite3', default='db.sqlite3')
    parser.add_argument(
        '-d', '--data', help=f'Путь до данных с файлами. По умолчанию {BASE_DEFAULT_PATH}', default=BASE_DEFAULT_PATH)


    return parser.parse_args()

if __name__ == "__main__":
    options = parse_arguments(sys.argv)
    main(options)
