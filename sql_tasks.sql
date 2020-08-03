-- Task #1
-- 1)
DELETE FROM bird_colors_info;
INSERT INTO bird_colors_info (color, count) SELECT color, COUNT(*) FROM birds GROUP BY color;

-- 2)
DELETE FROM bird_colors_info;
INSERT INTO bird_colors_info (color, count)
SELECT c.color AS color, COUNT(name) FROM (
	SELECT 'black'::bird_color AS color UNION ALL
	SELECT 'white' UNION ALL
	SELECT 'black & white' UNION ALL
	SELECT 'grey' UNION ALL
	SELECT 'red' UNION ALL
	SELECT 'red & white') c LEFT JOIN
birds b 
USING(color)
GROUP BY color;


-- Task #2
DELETE FROM birds_stat;
INSERT INTO birds_stat (body_length_mean, body_length_median, body_length_mode, wingspan_mean, wingspan_median, wingspan_mode)
SELECT 
    (SELECT AVG(body_length) FROM birds), 
	 (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY body_length) FROM birds),
	 (SELECT ARRAY(SELECT MODE() WITHIN GROUP (ORDER BY body_length) AS modal_value FROM birds)),
	 (SELECT AVG(wingspan) FROM birds), 
	 (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY wingspan) FROM birds),
	 (SELECT ARRAY(SELECT MODE() WITHIN GROUP (ORDER BY wingspan) AS modal_value FROM birds));




