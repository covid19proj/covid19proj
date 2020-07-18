import os
from flask import Flask
from flask import render_template
import psycopg2

pg_conn = psycopg2.connect("dbname='qnswfixs' user='qnswfixs' host='kandula.db.elephantsql.com' password='A82HCdQ9xDVrhHyDxxE_BHBGnx_WIeKB'")
pg_cur = pg_conn.cursor()

country_comparison_query = """
select
string_agg('{"name":"' || countries_and_territories || '",data:[' || (
select string_agg(cases_total::text,',') from
(select * from reports_cumulative
where countries_and_territories = c.countries_and_territories
and date_rep >= c.first_case
order by date_rep
) x
)::text || ']}', ',')
from
countries c
where countries_and_territories in (
	select countries_and_territories from
	(
select distinct  on (countries_and_territories) countries_and_territories, cases_total
from reports_cumulative
order by countries_and_territories, cases_total desc
) x order by cases_total desc
	limit 10
)
"""

bubbles_query = """
select
string_agg('[' || m1.value::text || ',' || m2.value::text || ',' ||
(
 SELECT deaths_total FROM reports_cumulative r
 WHERE r.countries_and_territories = m1.countries_and_territories
 ORDER BY date_rep DESC
 LIMIT 1
)::text || ']', ',')
from country_metrics m1
inner join country_metrics m2 using (countries_and_territories)
where 
m1.metric = 'gdp_per_capita' and
m2.metric = 'median_age' and
m1.countries_and_territories in (
select countries_and_territories from
(
select distinct on (countries_and_territories) countries_and_territories, deaths_total
from reports_cumulative
order by countries_and_territories, deaths_total desc
) x order by deaths_total desc
limit 25
)
"""

continents_query = """
select string_agg('{name:''' || continent_exp || ''',data:[' ||
(
select string_agg('{name:''' || countries_and_territories || ''',value:' ||
	(
		select deaths_total::text
		from reports_cumulative r
		where r.countries_and_territories = c.countries_and_territories
		order by date_rep desc
		limit 1
	)
	 || '}', ',')
from countries c
where con.continent_exp = c.continent_exp
)
|| ']}', ',')
from continents con
"""

app = Flask(__name__)

@app.route("/country_comparison")
def country_comparison():
    pg_cur.execute(country_comparison_query)
    row = pg_cur.fetchone()

    return render_template("country_comparison.html", data=row[0])

@app.route("/bubbles")
def bubbles():
    pg_cur.execute(bubbles_query)
    row = pg_cur.fetchone()

    return render_template('bubbles.html', data=row[0])

@app.route("/continents")
def continents():
    pg_cur.execute(continents_query)
    row = pg_cur.fetchone()

    return render_template('continents.html', data=row[0])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
