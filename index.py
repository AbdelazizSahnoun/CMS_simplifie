from sqlite3.dbapi2 import Error
from flask import Flask, flash, redirect, url_for, abort
from flask import render_template
from flask import g
from database import Database
from flask import request
import logging
import datetime


app = Flask(__name__, static_url_path="", static_folder="static")
app.config['SECRET_KEY'] = 'SECRETKEY'
format_log = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                    format=format_log)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route("/")
def index():
    today = datetime.date.today()
    try:
        articles = get_db().get_article_by_date(today)
        return render_template('index.html', articles=articles)
    except Error as e:
        abort(503, description=e)


@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        try:
            searchterm = request.form['searchterm']
            results = get_db().get_article_by_searchterm(searchterm)
            if not results:
                return render_template('search_results_aucun.html',
                                       searchterm=searchterm)
            return render_template('search_results.html', results=results)
        except Error as e:
            abort(503, description=e)
    else:
        return "405 Method Not Allowed", 405


@app.route('/articles/<article_id>')
def articles(article_id):
    try:
        article = get_db().get_articles_by_id(article_id)
    except Error as e:
        abort(503, description=e)
    if not article:
        abort(404, description="L'article n'existe pas")
    return render_template('article.html', article=article)


@app.route("/admin")
def admin():
    try:
        articles = get_db().get_articles_by_all()
    except Error as e:
        abort(503, description=e)
    return render_template('admin.html', articles=articles)


@app.route("/admin/modifier_articles/<article_id>")
def admin_modifier_articles(article_id):
    try:
        article = get_db().get_articles_by_id(article_id)
    except Error as e:
        abort(503, description=e)
    if not article:
        abort(404, description="L'article n'existe pas")
    return render_template('admin_modifier_articles.html', article=article)


msg_erreur_admin_modification = '''
Formulaire invalide,veuillez entrer un titre valide et un paragraphe valide,
seuls les champs titre et paragraphe sont modifables.
'''


@app.route("/admin/modifier_articles/<article_id>/post_article",
           methods=['POST'])
def admin_modifier_articles_post(article_id):

    if request.method == "POST":
        try:
            article = get_db().get_articles_by_id(article_id)
            if not article:
                abort(404, description="L'article n'existe pas")
            if(
                request.form['titre'] == "" or len(request.form['titre']) > 100
                or request.form['paragraphe'] == ""
                or len(request.form['paragraphe']) > 500
                or request.form['identifiant'] != article[0][2]
                or request.form['auteur'] != article[0][3]
                or request.form['date_publication'] != article[0][4]
            ):
                flash(msg_erreur_admin_modification)
                return render_template('admin_modifier_articles.html',
                                       article=article)
        except Error as e:
            abort(503, description=e)
        else:
            get_db().update_article_title(article_id, request.form['titre'])
            get_db().update_article_paragraphe(
                article_id, request.form['paragraphe'])
            return redirect(url_for('admin_modifier_articles_success',
                                    article_id=article_id))

    else:
        return "405 Method Not Allowed", 405


@app.route("/admin/modifier_articles/success_modifier/<article_id>")
def admin_modifier_articles_success(article_id):
    try:
        article = get_db().get_articles_by_id(article_id)
    except Error as e:
        abort(503, description=e)
    if not article:
        abort(404, description="L'article n'existe pas")
    return render_template('success_modification.html', article=article)


msg_erreur_admin_nouveau = '''
Formulaire invalide,
veuillez entrer les informations valides en suivant les messages d\'erreurs
'''


@app.route("/admin-nouveau")
def admin_nouveau():
    return render_template('admin_nouveau.html')


@app.route("/admin-nouveau/ajout/", methods=['POST'])
def admin_nouveau_ajout():

    titre = request.form['titre']
    identifiant = request.form['identifiant']
    auteur = request.form['auteur']
    date_publication = request.form['date_publication']
    paragraphe = request.form['paragraphe']

    if request.method == "POST":
        if(
           titre == "" or len(titre) > 100 or
           identifiant == "" or len(identifiant) > 50 or
           auteur == "" or len(auteur) > 100 or
           not validerDate(date_publication)
           or paragraphe == ""
           or len(paragraphe) > 500
           ):
            flash(msg_erreur_admin_nouveau)
            return render_template('admin_nouveau.html')
        else:
            try:
                id = get_db().get_last_article_id()[0][0]
                id += 1
                get_db().add_new_article(str(id), titre, identifiant,
                                         auteur, date_publication, paragraphe)
            except Error as e:
                abort(503, description=e)
            return redirect(url_for('admin_ajout_success', article_id=id))

    else:
        return "405 Method Not Allowed", 405


@app.route("/admin-nouveau/ajout/success_ajout/<article_id>")
def admin_ajout_success(article_id):
    try:
        article = get_db().get_articles_by_id(article_id)
    except Error as e:
        abort(503, description=e)
    if not article:
        abort(404, description="L'article n'existe pas")
    return render_template('success_ajout.html', article=article)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', erreur=e), 404


@app.errorhandler(503)
def service_unavailable(e):
    return render_template('503.html'), 503


def validerDate(date_publication):

    date_format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(date_publication, date_format)
    except ValueError:
        return False
    return True
