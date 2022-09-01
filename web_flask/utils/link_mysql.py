import pymysql

def load_context(level):
    host = "betterdatabase.cyooqkxaxvqu.us-east-1.rds.amazonaws.com"
    username = "admin"
    password = "jung0204"
    port = 3306
    database = "better"

    db = pymysql.connect(
                        host=host, 
                        port=port, 
                        user=username, passwd=password, 
                        db=database, charset='utf8'
                        )


    sql = f"select context, question, answer, context_blank_sentence, context_black_answer, title FROM level_{level}_book ORDER BY RAND() LIMIT 1;"
    sql_2 = "SELECT count(*) from level_1_book"
    with db:
        with db.cursor() as cur:
            cur.execute(sql)
            result_sql = cur.fetchall()[0]

    # random으로 3개 추출!
    result_sql       

    return result_sql
