
import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:

            self.connection = sqlite3.connect('db/article.db')

        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_articles_by_all(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article")
        articles = cursor.fetchall()
        return articles

    def get_articles_by_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where id=?", (id,))
        articles = cursor.fetchall()
        return articles

    def get_article_by_date(self, date):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "select * from article where date_publication=?", (date,))
        articles = cursor.fetchall()
        return articles

    def get_article_by_searchterm(self, searchterm):

        searchterm = '%' + searchterm + '%'
        cursor = self.get_connection().cursor()
        cursor.execute(
            "select * from article where titre like ? or paragraphe like ?",
            (searchterm, searchterm))
        results = cursor.fetchall()
        return results

    def get_last_article_id(self):

        cursor = self.get_connection().cursor()
        cursor.execute("select * from article order by id desc limit 1")
        return cursor.fetchall()

    def update_article_title(self, id, titre):

        cursor = self.get_connection().cursor()
        cursor.execute("update article set titre=? where id=?", (titre, id))
        self.get_connection().commit()

    def update_article_paragraphe(self, id, paragraphe):

        cursor = self.get_connection().cursor()
        cursor.execute(
            "update article set paragraphe=? where id=?", (paragraphe, id))
        self.get_connection().commit()

    def add_new_article(self, id, titre, identifiant,
                        auteur, date_publication, paragraphe):
        cursor = self.get_connection().cursor()
        cursor.execute("insert into article values(?,?,?,?,?,?)",
                       (id, titre, identifiant, auteur,
                        date_publication, paragraphe))
        self.get_connection().commit()
