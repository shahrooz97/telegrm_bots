import mysql.connector 




def setup_db(host='remotemysql.com', user='dBny7aHPwr', password='B6KY87R1k0', database='dBny7aHPwr'):
    sql = """
                CREATE TABLE IF NOT EXISTS bot_users 
                (user_name CHAR(100),
                id INT PRIMARY KEY )
          """

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cur = conn.cursor()
        cur.execute(sql)
        cur.execute('SELECT VERSION()')
        data = cur.fetchall()
        print('connected db verseion: %s'%(data))
        cur.execute(sql)
    except Exception as e:
        print(e)
    conn.commit()
 
#make query to the  db and return all info
def get_db(where=None):
    conn = mysql.connector.connect(host='remotemysql.com', user='dBny7aHPwr', password='B6KY87R1k0', database='dBny7aHPwr')
    if not where:
        sql = """
            SELECT * FROM bot_users
        """
    else:
        sql = """
            SELECT * FROM bot_users
        """
        sql = sql + " WHERE id = {}".format(where)

    cur = conn.cursor()
    cur.execute(sql)
    return [items for items in cur.fetchall()] 

#return all chat_ids 
def get_chat_ids(where=None):
    conn = mysql.connector.connect(host='remotemysql.com', user='dBny7aHPwr', password='B6KY87R1k0', database='dBny7aHPwr')
    if not where:
        sql = """
            SELECT chat_id FROM bot_users
        """
    else:
        sql = """
            SELECT chat_id FROM bot_users
        """
        sql = sql + " WHERE id = {}".format(where)

    cur = conn.cursor()
    cur.execute(sql)
    return [items for items in cur.fetchall()] 


#return all user ids 
def get_user_ids(where=None):
    conn = mysql.connector.connect(host='remotemysql.com', user='dBny7aHPwr', password='B6KY87R1k0', database='dBny7aHPwr')
    if not where:
        sql = """
            SELECT id FROM bot_users
        """
    else:
        sql = """
            SELECT id FROM bot_users
        """
        sql = sql + " WHERE id = {}".format(where)

    cur = conn.cursor()
    cur.execute(sql)
    return [items for items in cur.fetchall()] 


def insert_to_db(values):
    conn = mysql.connector.connect(host='remotemysql.com', user='dBny7aHPwr', password='B6KY87R1k0', database='dBny7aHPwr')
    sql = "INSERT INTO bot_users (id, chat_id) VALUES (%s, %s)"
    cur = conn.cursor()
    try:
        cur.execute(sql, values)
    except Exception as e:
        print(e)
        #conn.close()
        #return e.args
    conn.commit()
    #conn.close()


def del_from_db(where):
    conn = mysql.connector.connect(host='remotemysql.com', user='dBny7aHPwr', password='B6KY87R1k0', database='dBny7aHPwr')
    sql = "DELETE FROM bot_users WHERE id = {}".format(where)
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
        #conn.close()
        #return e.args
    conn.commit()
 


