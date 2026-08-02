USE bus_data;

-- Top 10 most common run times
SELECT
    run_time,
    COUNT(*) AS total
FROM journey_pattern_links
GROUP BY run_time
ORDER BY total DESC
LIMIT 10;

-- Stops with the highest number of outgoing journeys
SELECT
    from_stop,
    COUNT(*) AS journeys
FROM journey_pattern_links
GROUP BY from_stop
ORDER BY journeys DESC
LIMIT 10;

-- Number of unique bus stops
SELECT
    COUNT(DISTINCT from_stop) AS unique_stops
FROM journey_pattern_links;

-- Count missing activities
SELECT
    COUNT(*) AS missing_activity
FROM journey_pattern_links
WHERE from_activity IS NULL;

-- Top route links by journey frequency
SELECT
    route_link_ref,
    COUNT(*) AS total_journeys
FROM journey_pattern_links
GROUP BY route_link_ref
ORDER BY total_journeys DESC
LIMIT 10;