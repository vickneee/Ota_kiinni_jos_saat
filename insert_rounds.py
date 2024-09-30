from db_functions import db_update

# Lisätään yksi kierros round columniin
def insert_round():
    sql= """
        UPDATE game
        SET round = round +1
        """
    db_update(sql)