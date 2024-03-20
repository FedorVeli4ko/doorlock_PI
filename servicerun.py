import time
import cv2
import sqlite3
import syslog
import RPi.GPIO as GPIO

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)  #GPIO numbers instead of board numbers

DOOR_RELAY_GPIO = 17
GPIO.setup(DOOR_RELAY_GPIO, GPIO.OUT)



# import os

# mypath = os.getcwd()
# dbpath = mypath + '/database.db'
# /root/database.db
# syslog.syslog('Opening database ' + dbpath)

# con = sqlite3.connect(dbpath)
con = sqlite3.connect("/home/pipa/Desktop/backend/database.db")
cur = con.cursor()
syslog.syslog('Opening database...')

# cur.execute("CREATE TABLE IF NOT EXISTS users(userID, name, surname, class)")
# cur.execute("""
#  INSERT INTO users VALUES
#  ('00001', 'Fedor', 'Velichko', '10F'),
#  ('00010', 'Sergey', 'Tselishev', 'TEACHER')
# """)

# cur.execute("""CREATE TABLE IF NOT EXISTS orders(
#      orderid TEXT,
#      date TEXT,
#      time TEXT);
#  """)
# con.commit()
def noliki(x):
    if str(x) == '1':
        x = '01'
    if str(x) == '2':
        x = '02'
    if str(x) == '3':
        x = '03'
    if str(x) == '4':
        x = '04'
    if str(x) == '5':
        x = '05'
    if str(x) == '6':
        x = '06'
    if str(x) == '7':
        x = '07'
    if str(x) == '8':
        x = '08'
    if str(x) == '9':
        x = '09'
    if str(x) == '0':
        x = '00'
    return(x)
    

    

def decode():
    
    door_lock = 'DOOR CLOSED'
    GPIO.output(DOOR_RELAY_GPIO, GPIO.LOW)
#     if GPIO.output(DOOR_RELAY_GPIO) == GPIO.LOW:
#         door_lock = 'DOOR CLOSED'
#     else:
#         door_lock = 'DOOR OPENED'
#         GPIO.output(DOOR_RELAY_GPIO, GPIO.HIGH)
    
    
    
    # doortime = 0
    lastID = '.'
    cap = cv2.VideoCapture(0)
    
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        
        data, bbox, _ = detector.detectAndDecode(img)
        
        # t = time.time()
        # if doortime and (t - doortime) > 10:
            # GPIO.output(DOOR_RELAY_GPIO, GPIO.LOW)
            # door_lock = 'DOOR CLOSED'
            # syslog.syslog('DOOR AUTOMATICLY CLOSED')
            # doortime = 0

        if data:
            # print("[+] QR Code detected, data:", data)
            datatime = time.time()
            cur.execute("SELECT userID FROM users WHERE userID = ?", [str(data)])
            syslog.syslog('QR DETECTED!!!')
        




            if cur.fetchone() is not None:

                if lastID != data:

                    user_id = data
                    cur.execute("SELECT name FROM users WHERE userid = ?", [str(data)])
                    ordername0 = cur.fetchone()
                    cur.execute("SELECT surname FROM users WHERE userid = ?", [str(data)])
                    ordersurname0 = cur.fetchone()
                    # family = str(ordersurname)[2:-3]
                    # print(family)
                    cur.execute("SELECT class FROM users WHERE userid = ?", [str(data)])
                    orderclass0 = cur.fetchone()
                    ordername = str(ordername0)[2:-3]
                    ordersurname = str(ordersurname0)[2:-3]
                    orderclass = str(orderclass0)[2:-3]
                    result = time.localtime(time.time())
                    curtime = noliki(str(result.tm_hour)) + ':' + noliki(str(result.tm_min)) + ':' + noliki(str(result.tm_sec))
                    curdate = noliki(str(result.tm_mday)) + '/' + noliki(str(result.tm_mon)) + '/' + noliki(str(result.tm_year))
                    
                    # syslog.syslog(syslog.LOG_DEBUG, data)
                    # syslog.syslog(syslog.LOG_DEBUG, curdate)
                    # syslog.syslog(syslog.LOG_DEBUG, curtime)
                    # syslog.syslog(syslog.LOG_DEBUG,'SUCCESS')
                    if str(orderclass) == 'УЧИТЕЛЬ':
                            
                        if door_lock == 'DOOR CLOSED':
                            GPIO.output(DOOR_RELAY_GPIO, GPIO.HIGH)
                            door_lock = 'DOOR OPENED'
                            doortime = time.time()
                            syslog.syslog('DOOR OPENED')
                            values = [user_id, str(ordername), str(ordersurname), str(orderclass), curdate, curtime]
                            cur.execute("INSERT OR IGNORE INTO orders(orderid, order_name, order_surname, order_class, date, time) VALUES(?, ?, ?, ?, ?, ?)", values)
                            con.commit()
                            dbtime = time.time()
                            finish_tchr = 'Teacher with ID ' + data + ' is entered in database, ' + door_lock + ' | ' + curdate + ' ' + curtime
                        
                    
                        else:
                            GPIO.output(DOOR_RELAY_GPIO, GPIO.LOW)
                            door_lock = 'DOOR CLOSED'
                            syslog.syslog('DOOR CLOSED')
                            # values = [user_id, str(ordername), str(ordersurname), str(orderclass), curdate, curtime]
                            # cur.execute("INSERT OR IGNORE INTO orders(orderid, order_name, order_surname, order_class, date, time) VALUES(?, ?, ?, ?, ?, ?)", values)
                            # con.commit()
                            # dbtime = time.time()
                            finish_tchr = 'Teacher with ID ' + data + '  ' + door_lock + ' | ' + curdate + ' ' + curtime
                            lastID = data
                            
                        syslog.syslog(syslog.LOG_DEBUG, finish_tchr)
                    else:
                        if door_lock == 'DOOR OPENED':
                            values = [user_id, str(ordername), str(ordersurname), str(orderclass), curdate, curtime]
                            cur.execute("INSERT OR IGNORE INTO orders(orderid, order_name, order_surname, order_class, date, time) VALUES(?, ?, ?, ?, ?, ?)", values)
                            con.commit()
                            dbtime = time.time()
                            finish_us = 'User with ID ' + data + ' is entered in database | ' + curdate + ' ' + curtime
                        else:
                            finish_us = 'ACCES DENIED to user with ID ' + data + '  | ' + curdate + ' ' + curtime
                        syslog.syslog(syslog.LOG_DEBUG, finish_us)
                    lastID = data

                        
                else:
                    if datatime - dbtime > 10:
                        user_id = data
                        cur.execute("SELECT name FROM users WHERE userid = ?", [str(data)])
                        ordername0 = cur.fetchone()
                        cur.execute("SELECT surname FROM users WHERE userid = ?", [str(data)])
                        ordersurname0 = cur.fetchone()
                        cur.execute("SELECT class FROM users WHERE userid = ?", [str(data)])
                        orderclass0 = cur.fetchone()
                        ordername = str(ordername0)[2:-3]
                        ordersurname = str(ordersurname0)[2:-3]
                        orderclass = str(orderclass0)[2:-3]
                        result = time.localtime(time.time())
                        curtime = noliki(str(result.tm_hour)) + ':' + noliki(str(result.tm_min)) + ':' + noliki(str(result.tm_sec))
                        curdate = noliki(str(result.tm_mday)) + '/' + noliki(str(result.tm_mon)) + '/' + noliki(str(result.tm_year))
                        values = [user_id, str(ordername), str(ordersurname), str(orderclass), curdate, curtime]
                        cur.execute("INSERT OR IGNORE INTO orders(orderid, order_name, order_surname, order_class, date, time) VALUES(?, ?, ?, ?, ?, ?)", values)
                        con.commit()
                        dbtime = time.time()
                        finish_us = 'User with ID ' + data + ' is entered in database | ' + curdate + ' ' + curtime
                        # syslog.syslog(syslog.LOG_DEBUG, data)
                        # syslog.syslog(syslog.LOG_DEBUG, curdate)
                        # syslog.syslog(syslog.LOG_DEBUG, curtime)
                        # syslog.syslog(syslog.LOG_DEBUG,'SUCCESS')
                        if str(orderclass) == 'УЧИТЕЛЬ':
                            
                            if door_lock == 'DOOR CLOSED':
                                GPIO.output(DOOR_RELAY_GPIO, GPIO.HIGH)
                                door_lock = 'DOOR OPENED'
                                doortime = time.time()
                                syslog.syslog('DOOR OPENED')
                                values = [user_id, str(ordername), str(ordersurname), str(orderclass), curdate, curtime]
                                cur.execute("INSERT OR IGNORE INTO orders(orderid, order_name, order_surname, order_class, date, time) VALUES(?, ?, ?, ?, ?, ?)", values)
                                con.commit()
                                dbtime = time.time()
                                finish_tchr = 'Teacher with ID ' + data + ' is entered in database, ' + door_lock + ' | ' + curdate + ' ' + curtime
                            
                        
                            else:
                                GPIO.output(DOOR_RELAY_GPIO, GPIO.LOW)
                                door_lock = 'DOOR CLOSED'
                                syslog.syslog('DOOR CLOSED')
                                # values = [user_id, str(ordername), str(ordersurname), str(orderclass), curdate, curtime]
                                # cur.execute("INSERT OR IGNORE INTO orders(orderid, order_name, order_surname, order_class, date, time) VALUES(?, ?, ?, ?, ?, ?)", values)
                                # con.commit()
                                # dbtime = time.time()
                                finish_tchr = 'Teacher with ID ' + data + '  ' + door_lock + ' | ' + curdate + ' ' + curtime
                                
                                
                            syslog.syslog(syslog.LOG_DEBUG, finish_tchr)
                        else:
                            if door_lock == 'DOOR OPENED':
                                values = [user_id, str(ordername), str(ordersurname), str(orderclass), curdate, curtime]
                                cur.execute("INSERT OR IGNORE INTO orders(orderid, order_name, order_surname, order_class, date, time) VALUES(?, ?, ?, ?, ?, ?)", values)
                                con.commit()
                                dbtime = time.time()
                                finish_us = 'User with ID ' + data + ' is entered in database | ' + curdate + ' ' + curtime
                            else:
                                finish_us = 'ACCES DENIED to user with ID ' + data + '  | ' + curdate + ' ' + curtime
                            syslog.syslog(syslog.LOG_DEBUG, finish_us)
                    lastID = data
        del data
        time.sleep(0.1)




        
        # cv2.imshow("QR reader", img)
        # if cv2.waitKey(1) == ord("q"):
            # break
    # cap.release()
    # cv2.destroyAllWindows()
while True:
    try:
        decode()
    except Exception as error:
        syslog.syslog(error)
        pass
