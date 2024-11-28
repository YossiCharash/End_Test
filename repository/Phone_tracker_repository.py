



class PhoneTrackerRepository:
    def __init__(self,driver):
        self.driver = driver


    def create_phone_tracker(self,phone):
        with self.driver.session() as session:
            query = """
                MERGE (from:Device {account_id: $from_id, name: $from_name, brand: $from_brand, model: $from_model,latitude: $from_latitude, longitude:$from_longitude, altitude_meters:$from_altitude_meters, accuracy_meters:$from_accuracy_meters})
                MERGE (to:Device {account_id: $to_id, name: $to_name, brand: $to_brand, model: $to_model,latitude: $to_latitude, longitude:$to_longitude, altitude_meters:$to_altitude_meters, accuracy_meters:$to_accuracy_meters})
                CREATE (from)-[t:CONNECTED  {
                    details_id: $details_id,
                    method: $method,
                    bluetooth_version: $bluetooth_version,
                    signal_strength_dbm: $signal_strength_dbm,
                    distance_meters: $distance_meters,
                    duration_seconds: $duration_seconds,
                    timestamp: datetime($timestamp)
                }]->(to)
                RETURN t.details_id as details_id
            """

            result = session.run(query, {
                'from_id': phone["devices"][0]['id'],
                'from_name': phone["devices"][0]['name'],
                'from_brand': phone["devices"][0]['brand'],
                'from_model': phone["devices"][0]['model'],
                "from_latitude": phone["devices"][0]['location']['latitude'],
                "from_longitude": phone["devices"][0]['location']['longitude'],
                "from_altitude_meters": phone["devices"][0]['location']['altitude_meters'],
                "from_accuracy_meters": phone["devices"][0]['location']['accuracy_meters'],

                'to_id': phone["devices"][1]['id'],
                'to_name': phone["devices"][1]['name'],
                'to_brand': phone["devices"][1]['brand'],
                'to_model': phone["devices"][1]['model'],
                "to_latitude": phone["devices"][1]['location']['latitude'],
                "to_longitude":phone["devices"][1]['location']['longitude'],
                "to_altitude_meters": phone["devices"][1]['location']['altitude_meters'],
                "to_accuracy_meters": phone["devices"][1]['location']['accuracy_meters'],

                'details_id': f'{phone["interaction"]["from_device"]}{phone["interaction"]["to_device"]}',
                'method': phone['interaction']['method'],
                'bluetooth_version': phone['interaction']['bluetooth_version'],
                'signal_strength_dbm': phone['interaction']['signal_strength_dbm'],
                'distance_meters': phone['interaction']['distance_meters'],
                'duration_seconds': phone['interaction']['duration_seconds'],
                'timestamp': phone['interaction']['timestamp']
            })
            return result.single()['details_id']




    def get_num_phon_by_bluetooth(self):
        with self.driver.session() as session:
            result = session.run(
                """
                    MATCH (start:Device)
                    MATCH (end:Device)
                    WHERE start <> end
                    MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
                    WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
                    WITH path, length(path) as pathLength
                    ORDER BY pathLength DESC
                    LIMIT 1
                    RETURN length(path)
                    """
            )
            print(result)
            print(result.single())
            return result.single()['length']

