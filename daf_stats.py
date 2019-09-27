

def get_number_of_bikes_registered_in_total(conn):
    cur = conn.cursor()
    stmt = """
    SELECT brand, count(*) as number_of_bikes_registered
    FROM bike
    GROUP BY brand
    ORDER BY number_of_bikes_registered DESC;
    """
    cur.execute(stmt)
    data = serialize_number_of_bikes_registered_in_total(cur.fetchall())
    cur.close()
    conn.commit()
    return data


def serialize_number_of_bikes_registered_in_total(data):
    result = {}
    results = []
    for brand_data in data:
        record =  {}
        record["brand"] = brand_data[0]
        record["number_of_bikes_registered_in_daf"] = brand_data[1]
        results.append(record)
    result["stats"] = results
    return results

def get_number_of_bikes_in_depot(conn):
    cur = conn.cursor()
    stmt = """
    SELECT brand, count(*) as number_of_bikes, EXTRACT(epoch from avg(in_depot_duration)) / (3600*24) as average_days_in_depot
    FROM bike
    JOIN
    (SELECT bike_id, (NOW() - timestamp) as in_depot_duration
    FROM events
    WHERE event_id IN (select max(event_id) as max_event_id from events group by bike_id)
    AND event_type = 'check_in_depot') as bikes_in_depot
    ON bike.bike_id = bikes_in_depot.bike_id
    GROUP BY brand
    ORDER BY number_of_bikes DESC;
    """
    cur.execute(stmt)
    data = serialize_number_of_bikes_in_depot(cur.fetchall())
    conn.commit()
    cur.close()
    return data

def serialize_number_of_bikes_in_depot(data):
    result = {}
    results = []
    for brand_data in data:
        record =  {}
        record["brand"] = brand_data[0]
        record["number_of_bikes_registered_in_daf"] = brand_data[1]
        record["current_average_parking_duration"] = brand_data[2]
        results.append(record)
    result["stats"] = results
    return results

def get_stats_checkx(conn):
    cur = conn.cursor()
    stmt = """
    SELECT day::date, coalesce(number_of_checkins, 0) as number_of_checkins,
    coalesce(number_of_checkouts, 0) as number_of_checkouts
    FROM generate_series((NOW() + '-30 days')::date, NOW()::date, interval '1 day' day) day
    LEFT JOIN
    (SELECT timestamp::date as date, count(*) as number_of_checkins
    FROM events
    WHERE event_type = 'check_in_depot'
    GROUP BY timestamp::date
    ORDER BY date) as q1
    ON day = q1.date
    LEFT JOIN
    (SELECT timestamp::date as date, count(*) as number_of_checkouts
    FROM events
    WHERE event_type = 'check_out_depot'
    GROUP BY timestamp::date
    ORDER BY date) as q2
    ON day = q2.date;
    """
    cur.execute(stmt)
    data = serialize_stats_checkx(cur.fetchall())
    conn.commit()
    cur.close()
    return data

def serialize_stats_checkx(data):
    result = {}
    results = []
    for brand_data in data:
        record =  {}
        record["date"] = brand_data[0].strftime("%Y-%m-%d")
        record["number_of_check_ins"] = brand_data[1]
        record["number_of_check_outs"] = brand_data[2]
        results.append(record)
    result["stats"] = results
    return results

def get_stats_stored_longer_then(conn):
    cur = conn.cursor()
    stmt = """
   
    """
    cur.execute(stmt)
    data = serialize_stats_checkx(cur.fetchall())
    cur.close()
    return data




