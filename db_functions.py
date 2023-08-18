import sqlite3
import itertools
import datetime


#! ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ
def is_in_database(user_id):
    """Checks if user already in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT COUNT(id) 
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()[0][0]
    
    cursor.close()
    database.close()

    return users


def add_user(user_id, username):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''
        INSERT INTO users (user_id, username, products, receive, review, history)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, '[]', '[]', '[]', '[]',))
    
    database.commit()
    cursor.close()
    database.close()


def drop_settings(user_id):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET input=?, input_data=?, products=?, receive=?, review=?, smiles=?
                    WHERE user_id=?
                    ''', (False, None, '[]', '[]', '[]', None, user_id,))

    database.commit()
    cursor.close()
    database.close()


def get_users_field_info(user_id, field):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    info = cursor.execute(f'''SELECT {field}
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()[0][0]
    
    cursor.close()
    database.close

    return info


def update_users_field(user_id, field, value):
    database = sqlite3.connect("db.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET {field}=?
                    WHERE user_id=?
                    ''', (value, user_id,))

    database.commit()
    cursor.close()
    database.close()


def select_user_info(user_id):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    info = cursor.execute(f'''SELECT *
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()[0]
    
    cursor.close()
    database.close()

    return info


def select_again_eligible_users(products):
    database = sqlite3.connect("db.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = database.cursor()

    time_filter = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    request = ''

    for product in products:
        request += f'''history NOT LIKE "%'{product[1]}'%" OR '''
    
    request = '(' + request.rstrip(' OR ') + ')'

    ids = cursor.execute(f'''SELECT user_id 
                            FROM users 
                            WHERE products=? AND receive=? AND review=? AND 
                            eligible=? AND smiles IS ? AND last_participate<? AND
                            {request}
                            ''', ('[]', '[]', '[]', False, None, time_filter,)).fetchall()
                            
    cursor.close()
    database.close()

    if ids:
        ids = list(itertools.chain.from_iterable(ids))

    return ids


#! ДЛЯ РАБОТЫ С ТОВАРАМИ
def is_product_in_database(product):
    """Checks if user already in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT COUNT(id) 
                            FROM products
                            WHERE product=?
                            ''', (product,)).fetchall()[0][0]
    
    cursor.close()
    database.close()

    return users


def drop_active_products():
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute('UPDATE products SET active=?', (False,))
        
    database.commit()
    cursor.close()
    database.close()


def activate_product(product):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute('UPDATE products SET active=? WHERE product=?', (True, product,))
        
    database.commit()
    cursor.close()
    database.close()


def add_product(product):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''
        INSERT INTO products (product, photo)
        VALUES (?, ?)
        ''', (product[0], product[1],))
        
    database.commit()
    cursor.close()
    database.close()


def select_active_products():
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    products = cursor.execute(f'''SELECT id, product 
                            FROM products
                            WHERE active=?
                            ORDER BY id
                            ''', (True,)).fetchall()
    
    cursor.close()
    database.close()

    return products


def select_products_photos(product):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    photo = cursor.execute(f'''SELECT photo
                            FROM products
                            WHERE product=?
                            ''', (product,)).fetchall()[0][0]
    
    cursor.close()
    database.close()

    return photo


#! ДЛЯ РАБОТЫ С ТЕКСТОМ
def update_text(name, text):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE texts
                    SET text=?
                    WHERE name=?
                    ''', (text, name,))

    database.commit()
    cursor.close()
    database.close()


def get_text(name):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    text = cursor.execute(f'''SELECT text
                            FROM texts
                            WHERE name=?
                            ''', (name,)).fetchall()[0][0]
    
    cursor.close()
    database.close

    return text
