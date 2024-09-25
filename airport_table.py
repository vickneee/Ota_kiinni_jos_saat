from db_functions import get_db_connection

#fetch 21 airports from the database
def get_airports():
    airports = {}
    icao_codes=('EFHK','ENGM','EGLL',
                'LFPG','LEMD','EDDB',
                'LIRF','LPPT','EIDW',
                'LOWW','LGAV','EBBR',
                'ESSA','EPWA','LHBP',
                'LROP','LKPR','LYBE',
                'BIKF','LBSF','UKBB')
    sql = f"select airport.ident, airport.name, country.name, airport.latitude_deg, airport.longitude_deg from airport inner join country on airport.iso_country = country.iso_country where ident in {icao_codes}"
    conn=get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        airports[row[0]] = {"name": row[1], "country": row[2], "latitude": row[3], "longitude": row[4]}

    return airports


#function to print the airports
def print_airports(airports):
    for i in range(1,22):
        icao = list(airports.keys())[i-1]
        print(f"{i}. {airports[icao]['country']} : {airports[icao]['name']}")






