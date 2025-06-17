from database.DB_connect import DBConnect
from model.director import Director


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodes(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
from imdb_0408.movies_directors md , imdb_0408.movies m , imdb_0408.directors d 
where m.id = md.movie_id 
and m.`year` = %s
and md.director_id = d.id """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(Director(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAttoriDirectors(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select  r.actor_id as aid, md.director_id as did
from imdb_0408.movies_directors md , imdb_0408.roles r , imdb_0408.movies m 
where r.movie_id = md.movie_id 
and m.id = r.movie_id 
and m.`year` = %s
 """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append((row['aid'], row['did']))

        cursor.close()
        conn.close()
        return result
