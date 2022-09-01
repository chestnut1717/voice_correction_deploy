import pymysql

# 사용자가 각 레벨을 선택했을 때, 해당 레벨에 맞는 context, question, answer 로드하는 함수
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

    # 랜덤으로 추출한다
    sql = f"select context, question, answer, context_blank_sentence, context_black_answer, title FROM level_{level}_book ORDER BY RAND() LIMIT 1;"
    sql_2 = "SELECT count(*) from level_1_book"
    with db:
        with db.cursor() as cur:
            cur.execute(sql)
            result_sql = cur.fetchall()[0]

    result_sql       

    return result_sql
