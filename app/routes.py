from flask import render_template
from flask import request
from app import app
import psycopg2
import sys
import os

pg_conn = None
try:
    pg_conn = psycopg2.connect(
        dbname = os.getenv("DBNAME"),
        user = os.getenv("DBUSER"),
        host = os.getenv("DBHOST"),
        password = os.getenv("DBPASS")
    )
except:
    pg_conn = None
if pg_conn == None:
    sys.exit(1)
pg_cur = pg_conn.cursor()
pg_conn.autocommit = True

country_comparison_query = """
SELECT string_agg(
    '{{"name":"' || countries_and_territories || '",data:[' ||
    (
        SELECT string_agg({0}_total::text, ',')
        FROM (
            SELECT *
            FROM reports
            WHERE countries_and_territories = c.countries_and_territories
              AND date_rep >= c.first_case
              AND date_rep < '2020-{1}-01'
            ORDER BY date_rep
        ) x
    )::text || ']}}', ',')
FROM countries c
WHERE countries_and_territories IN (
  SELECT countries_and_territories
  FROM reports
  WHERE date_rep < '2020-{1}-01'
  GROUP BY countries_and_territories
  ORDER BY SUM({0}) DESC
  LIMIT 25
)
"""

bubbles_query = """
SELECT string_agg('[' || m1.value::text || ',' || m2.value::text || ',' ||
       (
        SELECT {0}_total
        FROM reports r
        WHERE r.countries_and_territories = m1.countries_and_territories
          AND date_rep < '2020-{1}-01'
        ORDER BY date_rep DESC
        LIMIT 1
       )::text || ']', ',')
FROM country_metrics m1
INNER JOIN country_metrics m2 USING (countries_and_territories)
WHERE m1.metric = 'pop_data'
  AND m2.metric = 'aged_70_older'
"""

continents_query = """
SELECT string_agg('{{name:''' || continent_exp || ''',data:[' ||
       (
        SELECT string_agg('{{name:''' || countries_and_territories || ''',value:' ||
               (
                SELECT {0}_total::text
                FROM reports r
                WHERE r.countries_and_territories = c.countries_and_territories
                  AND date_rep < '2020-{1}-01'
                ORDER BY date_rep DESC
                LIMIT 1
               ) || '}}', ',')
        FROM countries c
        WHERE cont.continent_exp = c.continent_exp
       ) || ']}}', ',')
FROM continents cont
"""

gdp_query = """
SELECT '{{countries:[''' || string_agg(a.countries_and_territories::text, ''',''') || '''],' ||
       'gdps:[' || string_agg(a.value::text, ',') || '],' ||
       'rates:[' || string_agg(((
           SELECT max({0}_total)
           FROM reports r
           WHERE r.countries_and_territories = a.countries_and_territories
             AND date_rep < '2020-{1}-01'
       )::numeric*1000000/b.value)::text, ',') || ']}}'
FROM public.country_metrics a
INNER JOIN public.country_metrics b USING (countries_and_territories)
WHERE a.metric = 'gdp_per_capita' 
  AND b.metric = 'pop_data'
  AND a.countries_and_territories IN 
(
  SELECT countries_and_territories
  FROM reports
  WHERE date_rep < '2020-{1}-01'
  GROUP BY countries_and_territories
  ORDER BY SUM({0}) DESC
  LIMIT 25
)
"""

count_query = """
SELECT sum(max)::text
FROM (
    SELECT max({0}_total) max
    FROM reports
    WHERE date_rep < '2020-{1}-01'
    GROUP BY countries_and_territories
) x
"""

@app.route('/')
@app.route('/index')
def index():
    chart_type = "cases"

    selected_type = request.args.get("type")
    if selected_type:
        chart_type = selected_type

    if not (chart_type in ["cases", "tests", "deaths"]):
        sys.exit(1)
	
    month_number = "07"

    selected_month = request.args.get("month")
    if selected_month:
        month_number = selected_month

    month_text = "June"
    if month_number == "06":
        month_text = "May"
    elif month_number == "05":
        month_text = "April"
    elif month_number == "04":
        month_text = "March"
    elif month_number == "03":
        month_text = "February"

    if not (month_number in ["03", "04", "05", "06", "07"]):
        sys.exit(1)
	
    try:
        pg_cur.execute(country_comparison_query.format(chart_type, month_number))
    except:
        sys.exit(1)
    row1 = pg_cur.fetchone()

    try:
        pg_cur.execute(bubbles_query.format(chart_type, month_number))
    except:
        sys.exit(1)
    row2 = pg_cur.fetchone()

    try:
        pg_cur.execute(continents_query.format(chart_type, month_number))
    except:
        sys.exit(1)
    row3 = pg_cur.fetchone()

    try:
        pg_cur.execute(gdp_query.format(chart_type, month_number))
    except:
        sys.exit(1)
    row4 = pg_cur.fetchone()

    try:
        pg_cur.execute(count_query.format(chart_type, month_number))
    except:
        sys.exit(1)
    row5 = pg_cur.fetchone()

    return render_template(
	    "index.html",
	    country=row1[0],
	    bubble=row2[0],
	    continent=row3[0],
	    gdp=row4[0],
	    count=row5[0],
	    type=chart_type,
	    month=month_number,
	    mtext=month_text
    )
