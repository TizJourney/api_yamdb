import csv, sqlite3

name_csv = ''   # название файла csv
name_model = '' # название модели
name_app = ''   # название приложения, в котором будут созданы модели

headers = [] # объявление заголовка таблицы

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

# --эта часть кода для проверки работы-- 
# (при созданных моделях не использовать!)
with open(f'data/{name_csv}.csv', 'r', encoding='utf8') as read_csv:
    dr = csv.DictReader(read_csv)
    headers = dr.fieldnames
cur.execute(f"CREATE TABLE {name_app}_{name_model} {tuple(headers)};")
# --------------------------------------

with open(f'data/{name_csv}.csv', 'r', encoding='utf8') as read_csv:
    # csv.DictReader использует первую строку в файле для header
    # запятая - разделитель по умолчанию
    dr = csv.DictReader(read_csv)
    headers = dr.fieldnames
    to_db = []
    for i in dr:
        row = []
        for key_i in headers:
            row.append(i[key_i])
        to_db.append(row)

count_headers = len(headers) # количество столбцов
str_q = '?, ' * (count_headers - 1) + '?'

cur.executemany(
    f"INSERT INTO {name_app}_{name_model} {tuple(headers)} VALUES ({str_q});",
    to_db
)

con.commit()
con.close()
