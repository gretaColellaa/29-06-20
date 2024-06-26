from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.direttore import Direttore


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodi(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
from directors d , movies_directors md , movies m
where d.id =md.director_id and md.movie_id =m.id 
and year =%s"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(Direttore(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.d1 as v1,t2.d2 as v2,count(distinct t1.a1) as peso
from (select md.director_id as d1, r.actor_id as a1
from roles r , movies_directors md, movies m 
where r.movie_id =m.id and r.movie_id =md.movie_id 
and  m.`year` =%s) as t1,
(select md.director_id as d2, r.actor_id as a2
from roles r , movies_directors md, movies m 
where r.movie_id =m.id and r.movie_id =md.movie_id 
and  m.`year` =%s) as t2
where t1.d1<t2.d2 and t1.a1=t2.a2
group by t1.d1,t2.d2"""

        cursor.execute(query,(anno,anno,))

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result
