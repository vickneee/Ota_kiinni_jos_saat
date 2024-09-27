from db_functions import get_db_connection, db_query

# Tarkistetaan sijaitseeko rikollinen ja etsivä samalla lentokentällä.
# Kysely kokeilee onko type 0 eli rikollisella
# ja type 1 eli etsivällä sama arvo location sarakkeessa
def game_over():
    sql= f"""
        select location
        from player
        where type = 0
        intersect
        select location
        from player
        where type = 1
        """
    result = db_query(sql)
    # Palautetaan True, jos rikollinen ja etsivä sijaitsevat samalla lentokentällä
    # Muuten False, peli jatkuu
    if result:
        return True
    return False
