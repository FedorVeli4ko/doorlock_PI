import bottle
import os
import sqlite3
import random
import string
import qrcode
import time


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return (result_str)


# Конфигурационные значения.
save_path = '/home/pipa/Desktop/backend'
save_file_path = save_path + '/files/'
path_to_db = '/home/pipa/Desktop/backend/database.db'

# Application object
app = bottle.Bottle()


# Static files such as images or CSS files are not served automatically.
# You have to add a route and a callback to control
# which files get served and where to find them:

@app.route('/css/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root=save_path + '/css')


@app.route('/js/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root=save_path + '/js')


@app.route('/fonts/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root=save_path + '/fonts')


@app.route('/images/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root=save_path + '/images')


# Стартовая страница
@app.route('/')
@app.route('/index')
def do_start_page():
    return bottle.template('/home/pipa/Desktop/backend/index.tpl')

# Работа с персоналиями
@app.route('/staff')
def do_staff_page():
    conn = sqlite3.connect(path_to_db)
    pl = conn.execute('''SELECT * FROM users''')
    ll = pl.fetchall()

    return bottle.template('/home/pipa/Desktop/backend/staff.tpl', plist=ll)

# Обработка формы
@app.post('/staff')
def do_staff_form():
    # Получить данные из формы
    name = bottle.request.forms.get('staff_name')
    surname = bottle.request.forms.get('staff_surname')
    cls = bottle.request.forms.get('staff_class')
    tch = bottle.request.forms.get('is_teacher')
    if tch == 'yes':
        cls = 'УЧИТЕЛЬ'
    # Подключиться к базе, взять список id для генерации уникального
    conn = sqlite3.connect(path_to_db)
    pl = conn.execute('''SELECT userID FROM users''')
    ll = pl.fetchall()  # userID list
    while (new_id := get_random_string(10)) in ll:
        pass
    # Генерация картинки кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(new_id)
    qr.make(fit=True)
    # Сохранение на диск
    image_name = new_id + '.jpg'
    image_path = save_path + '/images/' + image_name
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(image_path, "JPEG")
    # Запись в базу
    conn.execute('''INSERT INTO users VALUES(?, ?, ?, ?)''', (new_id, name, surname, cls))
    conn.commit()

    # Для отрисовки списка
    pl = conn.execute('''SELECT * FROM users''')
    ll = list(reversed(pl.fetchall()))

    conn.close()

    return bottle.template('/home/pipa/Desktop/backend/staff.tpl', plist=ll)

# Просмотр находящихся в кабинете
@app.route('/viewstaff')
def do_viewstaff_page():
    conn = sqlite3.connect(path_to_db)
    pl = conn.execute('''SELECT * FROM orders''')
    ll = list(reversed(pl.fetchall()))
    data = []
    ids = set()
    for item in ll:
        # для каждого уникального id выбираем одну единственную строку - последний вход
        if item[0] not in ids:
            ids.add(item[0])
            # проверить, что проход был за последнее время и отобрать только за 45 мин
            current_time = time.localtime(time.time())
            current_stamp = current_time.tm_hour * 60 + current_time.tm_min
            item_time = item[5].split(':')
            item_stamp = int(item_time[0]) * 60 + int(item_time[1])
            if current_stamp - item_stamp <= 45:
                data.append(item)

    return bottle.template('/home/pipa/Desktop/backend/viewstaff.tpl', plist=data)

# Run application
app.run(host='0.0.0.0', port=8088, debug=True)
