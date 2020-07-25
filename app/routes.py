from flask import render_template
from flask import request
from app import app
import psycopg2

pg_conn = psycopg2.connect("dbname='qnswfixs' user='qnswfixs' host='kandula.db.elephantsql.com' password='A82HCdQ9xDVrhHyDxxE_BHBGnx_WIeKB'")
pg_cur = pg_conn.cursor()

country_comparison_query = """
select
string_agg('{{"name":"' || countries_and_territories || '",data:[' || (
select string_agg({0}_total::text,',') from
(select * from reports_cumulative
where countries_and_territories = c.countries_and_territories
and date_rep >= c.first_case
order by date_rep
) x
)::text || ']}}', ',')
from
countries c
where countries_and_territories in (
	select countries_and_territories from
	(
select distinct  on (countries_and_territories) countries_and_territories, {0}_total
from reports_cumulative
order by countries_and_territories, {0}_total desc
) x order by {0}_total desc
	limit 10
)
"""

bubbles_query = """
select
string_agg('[' || m1.value::text || ',' || m2.value::text || ',' ||
(
 SELECT {0}_total FROM reports_cumulative r
 WHERE r.countries_and_territories = m1.countries_and_territories
 ORDER BY date_rep DESC
 LIMIT 1
)::text || ']', ',')
from country_metrics m1
inner join country_metrics m2 using (countries_and_territories)
where 
m1.metric = 'pop_data' and
m2.metric = 'aged_70_older'
"""

continents_query = """
select string_agg('{{name:''' || continent_exp || ''',data:[' ||
(
select string_agg('{{name:''' || countries_and_territories || ''',value:' ||
	(
		select {0}_total::text
		from reports_cumulative r
		where r.countries_and_territories = c.countries_and_territories
		order by date_rep desc
		limit 1
	)
	 || '}}', ',')
from countries c
where con.continent_exp = c.continent_exp
)
|| ']}}', ',')
from continents con
"""

count_query = """
select sum(max)::text
from (
select max({0}_total) max
from reports_cumulative
group by countries_and_territories
) x
"""


@app.route('/')
@app.route('/index')
def index():
    chart_type = "cases"

    selected_type = request.args.get("type")
    if selected_type:
        chart_type = selected_type

    pg_cur.execute(country_comparison_query.format(chart_type))
    row1 = pg_cur.fetchone()

    pg_cur.execute(bubbles_query.format(chart_type))
    row2 = pg_cur.fetchone()

    pg_cur.execute(continents_query.format(chart_type))
    row3 = pg_cur.fetchone()

    pg_cur.execute(count_query.format(chart_type))
    row4 = pg_cur.fetchone()

    return render_template("index.html", country=row1[0], bubble=row2[0], continent=row3[0], count=row4[0], type=chart_type.title())
