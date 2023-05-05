import pymysql


def connect_database():
    connection = pymysql.connect(host="116.63.14.146",
                                 port=3306,
                                 db="se2023",
                                 user="root",
                                 passwd="O2E-TH-1!",
                                 charset="utf8")
    cursor = connection.cursor()
    return connection, cursor


def close_database(connection, cursor):
    connection.close()
    cursor.close()


def get_all_entity(entity: str):
    connection, cursor = connect_database()

    instruction = "select * from " + entity

    try:
        cursor.execute(instruction)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("执行MySQL错误")
    result = cursor.fetchall()
    close_database(connection, cursor)
    return result


def update(entity: str, attribute: str, value: str, id: int):
    connection, cursor = connect_database()

    instruction = "update " + entity + " set " + attribute + "=" + '\"' + value + '\"' + " where id=" + str(id)

    try:
        cursor.execute(instruction)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("执行MySQL错误")
    close_database(connection, cursor)


def update_sci_vector(entity: str, vector: str, id: int):
    connection, cursor = connect_database()

    instruction = "update " + entity + " set vector_sci=" + vector + " where id=" + str(id)

    try:
        cursor.execute(instruction)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("执行MySQL错误")
    result = cursor.fetchall()
    close_database(connection, cursor)
    return result


def update_hit_vector(entity: str, vector: str, id: int):
    connection, cursor = connect_database()

    instruction = "update " + entity + " set vector_hit=" + vector + " where id=" + str(id)

    try:
        cursor.execute(instruction)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("执行MySQL错误")
    result = cursor.fetchall()
    close_database(connection, cursor)
    return result
