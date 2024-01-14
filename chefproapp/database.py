import pymysql
from werkzeug.security import generate_password_hash,check_password_hash
import uuid

def unique_id():
    return str(uuid.uuid4()).replace("-","")

def db():
    conn = pymysql.connect(host="localhost",user="root",password="Sami@7760365935",database="chefprodb")
    return conn

def register(fullname,username,emailid,country,birthdate,password):
    with db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO users(userid,fullname,username,emailid,country,birthdate,password) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (unique_id(),fullname,username,emailid,country,birthdate,generate_password_hash(password)))
        conn.commit()

def login(email,password):
    with db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE emailid = %s",(email,))
        data = cur.fetchone()
    if data and check_password_hash(data[6],password):
        return data
    else:
        return False
    
def userinfo (id):
    with db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE userid = %s",(id,))
        data = cur.fetchone()
    if data:
        return data
    else:
        return False
    
def foodrecipes(user=None):
    query = "SELECT * FROM recipes"
    params = None

    if user:
        query += " WHERE recipeby = %s"
        params = (user,)

    with db() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        data = cur.fetchall()

    return data

def addrecipes(title,steps,image,recipeby,ingredients):
    params = (unique_id(),title,steps,image,recipeby,ingredients)
    with db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO recipes(recipeid,title,steps,image,recipeby,ingredients) VALUES (%s,%s,%s,%s,%s,%s)",params)
        conn.commit()

def recipe_info(id):
    params = (id,)
    with db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipes WHERE recipeid = %s",(params))
        data = cur.fetchone()
    if data:
        return data
    else:
        return False
    
def userinfo(userid):
    params = (userid,)
    with db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE userid = %s",(params))
        data = cur.fetchone()
    if data:
        return data
    else:
        return False
    
def deleterecipe(id):
    with db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM ratings WHERE recipe =%s",(id,))
        cur.execute("DELETE FROM recipes WHERE recipeid = %s",(id,))
        conn.commit()

def editinfo(fullname,username,emailid,country,birthdate,userid):
    try:
        params = (fullname,username,emailid,country,birthdate,userid)
        with db() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET fullname = %s,username = %s,emailid = %s,country = %s,birthdate=%s WHERE userid = %s",params)
            conn.commit()
        return True
    except pymysql.IntegrityError:
        return False
    except:
        return False
    
def comments(recipeid):
    with db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ratings WHERE recipe = %s",(recipeid,))
        comment_list = cur.fetchall()
    if comment_list:
        return comment_list
    else:
        return False
    
def rate_recipe(stars,comment,recipe,commentor):
    try:
        params = (f'{commentor}{recipe}',stars,comment,recipe,commentor)
        with db() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO ratings(id,stars,comment,recipe,commentor) VALUES (%s,%s,%s,%s,%s)",params)
            conn.commit()
        return 'new'
    except:
        commentid = f'{commentor}{recipe}'
        params = (stars,comment,commentid)
        with db() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE ratings SET stars=%s,comment=%s WHERE id = %s",params)
            conn.commit()
        return 'old'
    