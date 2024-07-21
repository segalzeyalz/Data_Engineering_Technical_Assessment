### Queries

#### 1. How many objects of a specific type were detected by a specific vehicle in a given time range?
Example query:
To count the number of 'pedestrians' detected by the vehicle with ID 'ebab5f787798416fb2b8afc1340d7a4e' between '2022-06-05T21:00:00Z' and '2022-06-05T22:00:00Z', use the following query:
```sql
SELECT COUNT(*) AS object_count
FROM objects_detection
WHERE vehicle_id = 'ebab5f787798416fb2b8afc1340d7a4e'
AND object_type = 'pedestrians'
AND detection_time BETWEEN '2022-06-05T21:00:00Z' AND '2022-06-05T22:00:00Z';
```
![img_1.png](img_1.png)

#### 2. What is the latest status of a specific vehicle?
Example query:
To get the latest status of the vehicle with ID 'ebab5f787798416fb2b8afc1340d7a4e', use the following query:
```sql
SELECT status
FROM vehicles_status
WHERE vehicle_id = 'ebab5f787798416fb2b8afc1340d7a4e'
ORDER BY report_time DESC
LIMIT 1;
```
![img_2.png](img_2.png)

#### 3.  How many vehicles are currently in "accident" status?
Example query:
To count the number of vehicles that are currently in "accident" status, use the following query:
```sql
SELECT COUNT(DISTINCT vehicle_id) AS accident_vehicle_count
FROM vehicles_status
WHERE status = 'accident';
```
![img_3.png](img_3.png)

#### 4. How many vehicles are in "parking" status at any given time?
Example query:
To count the number of vehicles that are in "parking" status at any given time, use the following query:
```sql
SELECT COUNT(DISTINCT vehicle_id) AS parking_vehicle_count
FROM vehicles_status
WHERE status = 'parking';
```
![img_4.png](img_4.png)

#### 5. How many objects of a specific type were detected by all vehicles in a given time range?
Example query:
To count the number of 'cars' detected by all vehicles between '2022-06-05T21:00:00Z' and '2022-06-05T22:00:00Z', use the following query:
```sql
SELECT COUNT(*) AS object_count
FROM objects_detection
WHERE object_type = 'cars'
AND detection_time BETWEEN '2022-06-05T21:00:00Z' AND '2022-06-05T22:00:00Z';
```
![img_5.png](img_5.png)
#### 6. What is the distribution of object types detected by all vehicles on a specific day?
Example query:
To get the distribution of object types detected by all vehicles on '2022-06-05', use the following query:
```sql
SELECT object_type, COUNT(*) AS object_count
FROM objects_detection
WHERE DATE(detection_time) = 'specific_date'
GROUP BY object_type;
```
![img_6.png](img_6.png)

#### 7. How many vehicles reported detecting objects of a specific type on a given day?
```sql
SELECT COUNT(DISTINCT vehicle_id) AS vehicle_count
WHERE object_type = 'specific_object_type'
AND DATE(detection_time) = 'specific_date';
```
![img_7.png](img_7.png)
