# My First Server

Django + DRF

## Task #1
### if need data only for colors that exist in birds table
```sql
DELETE FROM bird_colors_info;
INSERT INTO bird_colors_info (color, count) SELECT color, COUNT(*) FROM birds GROUP BY color;
```

### for all colors from enum
```sql
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
```

## Task #2

```sql
DELETE FROM birds_stat;
INSERT INTO birds_stat (body_length_mean, body_length_median, body_length_mode, wingspan_mean, wingspan_median, wingspan_mode)
SELECT 
	(SELECT AVG(body_length) FROM birds), 
	(SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY body_length) FROM birds),
	(SELECT ARRAY(SELECT MODE() WITHIN GROUP (ORDER BY body_length) AS modal_value FROM birds)),
	(SELECT AVG(wingspan) FROM birds), 
	(SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY wingspan) FROM birds),
	(SELECT ARRAY(SELECT MODE() WITHIN GROUP (ORDER BY wingspan) AS modal_value FROM birds));

```

## Task #3
### Start
1. Start ostadnick/birds-db docker container from task
2. Start \venv\Scripts\activate.bat to activate venv or start PyCharm
3. Run command from project root folder in venv or Pycharm terminal:

```bash
python manage.py runserver 8080
```

### Unit tests
To run unit tests, you need to comment the following code:

file **birds/models.py**:
```python
    class Meta:
        managed = False
        db_table = 'birds'
```
and run tests using command:
```bash
python manage.py test
```

P.S. Also GET by name, PUT and DELETE APIs were created. It's just for me :)