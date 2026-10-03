import os
import time
import psycopg2

host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME', 'postgres')
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD')

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    sslmode='require'
)

cur = conn.cursor()

query = '''
SELECT product_id, SUM(amount)
FROM sales
GROUP BY product_id
ORDER BY SUM(amount) DESC;
'''

print('Generating reporting workload...')

try:
    while True:
        for _ in range(100):
            cur.execute(query)
            cur.fetchall()

        conn.commit()
        print('Reporting queries executed')
        time.sleep(1)

except KeyboardInterrupt:
    print('Load test stopped.')

finally:
    cur.close()
    conn.close()