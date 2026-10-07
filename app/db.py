import os, mysql.connector
from dotenv import load_dotenv
load_dotenv()
CFG=dict(host=os.getenv('DB_HOST','127.0.0.1'),port=int(os.getenv('DB_PORT','3306')),user=os.getenv('DB_USER','root'),password=os.getenv('DB_PASSWORD',''),database=os.getenv('DB_NAME','enterprise_ai_worker'))
def q(sql,p=()):
 c=mysql.connector.connect(**CFG);cur=c.cursor(dictionary=True);cur.execute(sql,p);r=cur.fetchall();cur.close();c.close();return r
def health():
 try:q('SELECT 1');return {'ok':True}
 except Exception as e:return {'ok':False,'error':str(e)}
