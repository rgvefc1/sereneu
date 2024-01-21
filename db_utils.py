import mysql.connector

# MySQL 연결 함수
def connect():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='0000',
            database='SERENEU'
        )
        return connection
    except mysql.connector.Error as error:
        print("Error: ", error)
        return None

# MySQL 연결 해제 함수
def disconnect(connection):
    if connection.is_connected():
        connection.close()

# SQL 쿼리 실행 함수
def execute_query(connection, sql, params=None):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            return result
    except mysql.connector.Error as error:
        print("Error: ", error)
        return None

# 추가 함수: 특정 쿼리를 실행하여 결과를 JSON 형식으로 반환
def execute_query_and_return_json(connection, sql):
    result = execute_query(connection, sql)
    if result:
        column_names = [column[0] for column in cursor.description]
        records = [dict(zip(column_names, row)) for row in result]
        return records
    else:
        return []
