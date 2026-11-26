from flask import Flask, render_template,request
import sqlite3
import re
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

@app.route("/")
def print_first_text():
    return 'начальная страница!!!'

@app.route("/samples")
def show_samples():
    db = sqlite3.connect('novabiom.db')
    c = db.cursor()
    c.execute('SELECT serial_number,client_name,status FROM samples')
    data = c.fetchall()
    db.commit()
    db.close()

    return data


@app.route("/samples/new",methods=["GET", "POST"])
def create_sample():
    text_error_serial_number = ''
    text_error_client_name = ''
    serial_number = ''
    client_name = ''
    if request.method == "POST":

        #серийный номер. Обработка
        serial_number = request.form.get("serial_number").strip()
        if len(serial_number)>64 or len(serial_number)<1:
            text_error_serial_number = "Поле неправильной длины! Должно быть от 1 до 64 включительно"
        elif  re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", serial_number):
            serial_number = serial_number.upper()
            print(serial_number)
        else:
            text_error_serial_number = """Номер не подходит по критериям. Должно 
            начинаться с латинским букв и содержать цифпы с латинскими буквами"""

        #имя клиента. Обработка
        client_name = request.form.get("client_name").strip()
        if len(client_name)<1 or len(client_name)>200:
            text_error_client_name = "Поле неправильной длины! Должно быть от 1 до 200 включительно"

        if len(text_error_client_name+text_error_serial_number) == 0:
            moscow_time = timezone(timedelta(hours=3))
            now = datetime.now(moscow_time).isoformat(timespec="seconds")
            print("Можно сохранять в БД")

            db = sqlite3.connect('novabiom.db')
            c = db.cursor()

            c.execute("""
            INSERT INTO samples (serial_number,client_name, status, created_at,status_changed_at)
            VALUES (?,?,?,?,?) ON CONFLICT(serial_number) DO NOTHING""", 
            (serial_number,client_name,"issued",now,now)
            )

            if c.rowcount == 0:
                text_error_serial_number = 'Номер уже есть в базе! Нельзя добавить. Попобуйте новый'
            else:
                c.execute ("""
                INSERT INTO status_events (sample_id , to_status, created_at)
                VALUES (?,?,?)""", (c.lastrowid, "issued",now))

            db.commit()
            db.close()
            


    return render_template("samples_new.html",text_error_1=text_error_serial_number,
                           text_error_2 = text_error_client_name,saved_serial_number = 
                           serial_number,saved_client_name =client_name)


@app.route("/samples/<int:id>",)
def show_card_samle(id):
    db = sqlite3.connect('novabiom.db')
    c = db.cursor()

    c.execute("""
    SELECT serial_number, client_name, status 
    FROM samples
    WHERE id = ?""", (id,))
    row = c.fetchone()
    db.close()

    if row is None:
        return render_template("sample_card.html", text_error = 'номера нет в базе. ' \
                               'Невозможно показать данные'),404
    else:
        return render_template("sample_card.html",serial_number = row[0] , client_name = row[1],
                                status = row[2] )

if __name__ == "__main__":
    app.run()
