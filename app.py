import os
from flask import Flask
from flask import render_template
import psycopg2

pg_conn = psycopg2.connect("dbname='qnswfixs' user='qnswfixs' host='kandula.db.elephantsql.com' password='A82HCdQ9xDVrhHyDxxE_BHBGnx_WIeKB'")
pg_cur = pg_conn.cursor()
pg_conn.autocommit = True

query_string = """
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

app = Flask(__name__)

@app.route("/")
def covid19():
    pg_cur.execute(query_string)
    row = pg_cur.fetchone()

    return render_template('index.html', data=row[0])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
