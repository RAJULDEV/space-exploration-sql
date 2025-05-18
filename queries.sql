-- Query 1: List Missions with Agency Names
SELECT 
    m.name AS mission_name,
    a.name AS agency_name,
    m.launch_date,
    m.destination,
    m.mission_type,
    m.success,
    m.cost
FROM missions m
JOIN agencies a ON m.agency_id = a.agency_id
ORDER BY m.launch_date
LIMIT 20;

-- Query 2: Count Missions by Agency
SELECT 
    a.name AS agency_name,
    COUNT(m.mission_id) AS mission_count
FROM agencies a
JOIN missions m ON a.agency_id = m.agency_id
GROUP BY a.name
ORDER BY mission_count DESC
LIMIT 10;

-- Query 3: Calculate Success Rates by Agency
SELECT 
    a.name AS agency_name,
    COUNT(m.mission_id) AS total_missions,
    SUM(CASE WHEN m.success THEN 1 ELSE 0 END) AS successful_missions,
    ROUND(SUM(CASE WHEN m.success THEN 1 ELSE 0 END) * 100.0 / COUNT(m.mission_id), 2) AS success_rate
FROM agencies a
JOIN missions m ON m.agency_id = a.agency_id
GROUP BY a.name
HAVING total_missions > 10
ORDER BY success_rate DESC;

-- Query 4: Missions by Decade
SELECT 
    FLOOR(YEAR(launch_date) / 10) * 10 AS decade,
    COUNT(mission_id) AS mission_count
FROM missions
GROUP BY decade
ORDER BY decade;