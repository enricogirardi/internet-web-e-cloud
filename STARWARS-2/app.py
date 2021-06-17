import os
import sqlite3 as sql
from flask import Flask, render_template, current_app, g, request, flash, redirect, url_for, session, abort
from flask_paginate import get_page_args, Pagination
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
app.secret_key = '242432fsf32rdfwqasw3eDDEDE'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = './static/assets/img/foto'

# Menu in alto
vocidimenu = [{'caption': 'Home', 'href': 'home'},
              {'caption': 'News', 'href': 'notizie'},
              {'caption': 'Events', 'href': 'eventi'},
              {'caption': 'Admin', 'href': 'login'}]


@app.route('/')
@app.route('/theforcewillbewithyou')
def theforcewillbewithyou():
    contenuto = {'title': 'the force will be with you', 'content': 'ciao questa è la home', 'navigation': vocidimenu}
    return render_template('theforcewillbewithyou.html', **contenuto)


# Home Page
@app.route('/home')
def home():
    # Database
    con = sql.connect("starwars.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from notizie ORDER BY id DESC LIMIT 9")
    rows = cur.fetchall()
    con.close()
    # Parametri da inviare al template
    contenuto = {'title': 'Star Wars', 'navigation': vocidimenu}
    return render_template('home.html', **contenuto, rows=rows)


######### NOTIZIE

# Singola Notizia
@app.route('/notizia/<int:id>')
def notizia(id):
    # Database
    con = sql.connect("starwars.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from notizie where id= ?", [id])
    rows = cur.fetchall()
    con.close()
    # Parametri da inviare al template
    contenuto = {'title': 'Notizia', 'navigation': vocidimenu}
    return render_template('notizia.html', **contenuto, rows=rows)


# Tutte le notizie con paginazione
@app.route('/notizie')
def notizie():
    # Database
    g.cur.execute("select count(*) from notizie")
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args(
        page_parameter="p", per_page_parameter="pp", pp=6
    )
    if per_page:
        sql = "select * from notizie  order by id DESC limit {}, {}".format(
            offset, per_page
        )
    else:
        sql = "select * from notizie order by id DESC"

    # Parametri da inviare al template
    contenuto = {'title': 'Notizie', 'navigation': vocidimenu}
    g.cur.execute(sql)
    notizie = g.cur.fetchall()
    pagination = get_pagination(
        p=page,
        pp=per_page,
        total=total,
        record_name="notizie",
        format_total=True,
        format_number=True,
        page_parameter="p",
        per_page_parameter="pp",
    )
    return render_template(
        "notiziep.html",
        rows=notizie,
        **contenuto,
        pagination=pagination,
    )


# Notizie di AREA TEMATICA
@app.route('/notizie/<area>')
def notizie_area(area):
    # Database
    con = sql.connect("starwars.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from notizie  where area= ? ORDER BY id DESC", [area])
    rows = cur.fetchall()
    # con.close()
    # Parametri da inviare al template
    contenuto = {'title': 'Area Notizie', 'navigation': vocidimenu}
    return render_template('notizie.html', **contenuto, rows=rows)


######### EVENTI

# Singolo Evento
@app.route('/evento/<int:id>')
def evento(id):
    # Database
    con = sql.connect("starwars.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from eventi where id= ?", [id])
    rows = cur.fetchall()
    con.close()
    # Parametri da inviare al template
    contenuto = {'title': 'Evento', 'navigation': vocidimenu}
    return render_template('evento.html', **contenuto, rows=rows)


# Eventi di AREA TEMATICA
@app.route('/eventi/<area>')
def eventi_area(area):
    # Database
    con = sql.connect("starwars.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from eventi where area= ? ORDER BY id DESC", [area])
    rows = cur.fetchall()
    con.close()
    # Parametri da inviare al template
    contenuto = {'title': 'Area Eventi', 'navigation': vocidimenu}
    return render_template('eventi.html', **contenuto, rows=rows)


# Tutti gli eventi con paginazione
@app.route('/eventi')
def eventi():
    # Database
    g.cur.execute("select count(*) from eventi")
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args(
        page_parameter="p", per_page_parameter="pp", pp=6
    )
    if per_page:
        sql = "select * from eventi  order by id DESC limit {}, {}".format(
            offset, per_page
        )
    else:
        sql = "select * from eventi order by id DESC"

    # Parametri da inviare al template
    contenuto = {'title': 'Eventi', 'navigation': vocidimenu}
    g.cur.execute(sql)
    eventi = g.cur.fetchall()
    pagination = get_pagination(
        p=page,
        pp=per_page,
        total=total,
        record_name="eventi",
        format_total=True,
        format_number=True,
        page_parameter="p",
        per_page_parameter="pp",
    )
    return render_template(
        "eventip.html",
        rows=eventi,
        **contenuto,
        pagination=pagination,
    )


##### PAGINAZIONE
def get_css_framework():
    return current_app.config.get("CSS_FRAMEWORK", "bootstrap4")


def get_link_size():
    return current_app.config.get("LINK_SIZE", "sm")


def get_alignment():
    return current_app.config.get("LINK_ALIGNMENT", "")


def show_single_page_or_not():
    return current_app.config.get("SHOW_SINGLE_PAGE", False)


def get_pagination(**kwargs):
    kwargs.setdefault("record_name", "records")
    return Pagination(
        css_framework=get_css_framework(),
        link_size=get_link_size(),
        alignment=get_alignment(),
        show_single_page=show_single_page_or_not(),
        **kwargs
    )


@app.before_request
def before_request():
    g.conn = sql.connect("starwars.sqlite")
    g.conn.row_factory = sql.Row
    g.cur = g.conn.cursor()


@app.teardown_request
def teardown(error):
    if hasattr(g, "conn"):
        g.conn.close()


######### AUTENTICAZIONE

@app.route("/login/", methods=["GET", "POST"])
def login():
    contenuto = {'title': 'Login', 'navigation': vocidimenu}
    loggato = False

    if session.get('logged_in'):
        if session['logged_in'] == True:
            loggato = True

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

            sql = "select * from utenti where username='{}'".format(
                username
            )
            g.cur.execute(sql)
            user = g.cur.fetchall()
            # estrazione e stampa password da utente
            # print(user[0][2])
            if user:
                pass_utente = user[0][2]

                # tool di GENERAZIONE DI UNA PASSWORD sha256
                # hash = generate_password_hash('password', 'sha256')
                # print(hash)
                # controllo = check_password_hash(pass_utente, password)
                # print(controllo)

                if user and check_password_hash(pass_utente, password):
                    session[username] = True
                    return redirect(url_for("login", username=username))
                else:
                    flash("Invalid username or password 2.")
            else:
                flash("Invalid username or password 3.")

    return render_template("login.html", **contenuto, loggato=loggato)


@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("successfully logged out.")
    return redirect(url_for('login'))


######### AMMINISTRAZIONE


@app.route("/admin-eventi/")
def admin_eventi():
    username = session.get('username')

    # Database
    g.cur.execute("select count(*) from eventi")
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args(
        page_parameter="p", per_page_parameter="pp", pp=6
    )
    if per_page:
        sql = "select * from eventi  order by id DESC limit {}, {}".format(
            offset, per_page
        )
    else:
        sql = "select * from eventi order by id DESC"

    # Parametri da inviare al template
    contenuto = {'title': 'Amministrazione Eventi', 'navigation': vocidimenu}
    g.cur.execute(sql)
    eventi = g.cur.fetchall()
    pagination = get_pagination(
        p=page,
        pp=per_page,
        total=total,
        record_name="eventi",
        format_total=True,
        format_number=True,
        page_parameter="p",
        per_page_parameter="pp",
    )
    return render_template(
        "admin.html",
        rows=eventi,
        **contenuto,
        pagination=pagination,
        username=username,
        tipologia='Eventi',
        link='evento',
        link2='evento_id'
    )


@app.route("/admin-notizie/")
def admin_notizie():
    username = session.get('username')

    # Database
    g.cur.execute("select count(*) from notizie")
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args(
        page_parameter="p", per_page_parameter="pp", pp=6
    )
    if per_page:
        sql = "select * from notizie  order by id DESC limit {}, {}".format(
            offset, per_page
        )
    else:
        sql = "select * from notizie order by id DESC"

    # Parametri da inviare al template
    contenuto = {'title': 'Amministrazione Notizie', 'navigation': vocidimenu}
    g.cur.execute(sql)
    notizie = g.cur.fetchall()
    pagination = get_pagination(
        p=page,
        pp=per_page,
        total=total,
        record_name="notizie",
        format_total=True,
        format_number=True,
        page_parameter="p",
        per_page_parameter="pp",
    )
    return render_template(
        "admin.html",
        rows=notizie,
        **contenuto,
        pagination=pagination,
        username=username,
        tipologia='Notizie',
        link='notizia',
        link2='notizia_id'
    )


######### AMMINISTRAZIONE - ARTICOLI
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/nuovo/<tipologia>", methods=["GET", "POST"])
def nuovo(tipologia):
    if request.method == "POST":
        username = session.get('username')

        if session.get('username'):
            if session['username'] == True:
                val_titolo = request.form.get('titolo')
                val_area = request.form.get('area')
                val_descrizione = request.form.get('descrizione')

                # caricamento immagine
                immagine = request.files.get('immagine')
                if immagine and allowed_file(immagine.filename):
                    filename = secure_filename(immagine.filename)
                    immagine.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    val_immagine = immagine.filename
                else:
                    val_immagine = 'default.jpg'

                # Inserimento dato in database OK FUNZIONANTE
                if tipologia == 'evento':
                    val_luogo = request.form.get('luogo')
                    con = sql.connect("starwars.sqlite")
                    cur = con.cursor()
                    cur.execute("SELECT id FROM eventi ORDER BY id DESC LIMIT 1")
                    ultimoid = cur.fetchone()[0]
                    ultimoid = int(ultimoid) + 1
                    sql_v = "insert into eventi(id,titolo,descrizione,immagine,area,luogo) values ('%s','%s','%s','%s','%s','%s')" % (
                        ultimoid, val_titolo, val_descrizione, val_immagine, val_area, val_luogo)
                    cur.execute(sql_v)
                    con.commit()
                    con.close()
                    flash('INSERIMENTO EVENTO AVVENUTO CORRETTAMENTE')
                    return redirect(url_for("login", username=username))

                if tipologia == 'notizia':
                    con = sql.connect("starwars.sqlite")
                    cur = con.cursor()
                    # la funzione last_insert_rowid() non funziona bene, cerco l'id manualmnete e lo incremento
                    cur.execute("SELECT id FROM notizie ORDER BY id DESC LIMIT 1")
                    ultimoid = cur.fetchone()[0]
                    ultimoid = int(ultimoid) + 1
                    # flash(str(ultimoid))
                    sql_v = "insert into notizie(id,titolo,descrizione,immagine,area) values ('%s','%s','%s','%s','%s')" % (
                        ultimoid, val_titolo, val_descrizione, val_immagine, val_area)
                    cur.execute(sql_v)
                    con.commit()
                    con.close()
                    flash('INSERIMENTO NOTIZIA AVVENUTO CORRETTAMENTE')
                    return redirect(url_for("login", username=username))

    contenuto = {'title': 'Nuovo Contenuto', 'navigation': vocidimenu}
    return render_template(
        "nuovo.html",
        **contenuto,
        tipologia=tipologia
    )


@app.route("/cancella-notizia/<id>", methods=["GET", "POST"])
def cancella_notizia(id):
    if session.get('username'):
        if session['username'] == True:
            username = session.get('username')

            # Cancella riga dal database
            con = sql.connect("starwars.sqlite")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("delete from notizie where id= ? ", [id])
            con.commit()
            con.close()
            flash('NOTIZIA CANCELLATA CORRETTAMENTE')
            return redirect(url_for("login", username=username))


@app.route("/cancella-evento/<id>", methods=["GET", "POST"])
def cancella_evento(id):
    if session.get('username'):
        if session['username'] == True:
            username = session.get('username')

            # Cancella riga dal database
            con = sql.connect("starwars.sqlite")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("delete from eventi where id= ? ", [id])
            con.commit()
            con.close()
            flash('EVENTO CANCELLATO CORRETTAMENTE')
            return redirect(url_for("login", username=username))


@app.route("/edit/<tipologia>/<id>", methods=["GET", "POST"])
def edit(tipologia, id):
    # Database
    con = sql.connect("starwars.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    if tipologia == 'notizia':
        cur.execute("select * from notizie where id= ?", [id])
    if tipologia == 'evento':
        cur.execute("select * from eventi where id= ?", [id])
    rows = cur.fetchall()
    con.close()

    if request.method == "POST":
        username = session.get('username')
        if session.get('username'):
            if session['username'] == True:
                val_titolo = request.form.get('titolo')
                val_area = request.form.get('area')
                val_descrizione = request.form.get('descrizione')
                val_immagine = request.form.get('immagine')

                # caricamento immagine
                immaginenuova = request.files.get('immaginenuova')
                if immaginenuova.filename and allowed_file(immaginenuova.filename):
                    filename = secure_filename(immaginenuova.filename)
                    immaginenuova.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    val_immagine = immaginenuova.filename

                # Inserimento dato in database
                if tipologia == 'evento':
                    val_luogo = request.form.get('luogo')
                    con = sql.connect("starwars.sqlite")
                    cur = con.cursor()
                    sql_v = "update  eventi set titolo='%s' ,descrizione='%s',immagine='%s',area='%s',luogo='%s' where id='%s'" % (
                        val_titolo, val_descrizione, val_immagine, val_area, val_luogo, id)
                    cur.execute(sql_v)
                    con.commit()
                    con.close()
                    flash('MODIFICA EVENTO AVVENUTA CORRETTAMENTE')
                    return redirect(url_for("login", username=username))

                if tipologia == 'notizia':
                    con = sql.connect("starwars.sqlite")
                    cur = con.cursor()
                    sql_v = "update  notizie set titolo='%s' ,descrizione='%s',immagine='%s',area='%s' where id='%s'" % (
                        val_titolo, val_descrizione, val_immagine, val_area, id)
                    cur.execute(sql_v)
                    con.commit()
                    con.close()
                    flash('MODIFICA NOTIZIA AVVENUTA CORRETTAMENTE')
                    return redirect(url_for("login", username=username))

    # Parametri da inviare al template
    contenuto = {'title': 'Nuovo Contenuto', 'navigation': vocidimenu}
    return render_template(
        "edit.html",
        **contenuto,
        rows=rows,
        tipologia=tipologia, id=id
    )


########## 404
@app.errorhandler(404)
def page_not_found(e):
    contenuto = {'title': 'Ti sei perso?', 'navigation': vocidimenu}
    return render_template('404.html', **contenuto), 404


########## APP RUN
if __name__ == '__main__':
    app.run(debug=True)

# TODO:   SISTEMA TEMPLATE + MOBILE
