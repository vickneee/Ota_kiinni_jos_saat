from db_functions import db_query

# Haetaan kannasta rikollisen viimeisin lokaatio, sekä lentolippu
# Kysely hakee taulun viimeiseimpänä lisätyt tiedot
def get_criminal_movements():
    sql = f"""
    SELECT location, ticket_type
    FROM past_movement
    JOIN player ON past_movement.player_id = player.id
    WHERE player.type = 0
    ORDER BY past_movement.rowid DESC
    LIMIT 1
    """
    criminal_movement=db_query(sql)
    return criminal_movement