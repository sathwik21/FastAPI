from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import psycopg2.extras

hostname = "localhost"
database = "demo"
username = "postgres"
pwd = "delta"
port_id = 5432
# conn = None
# cur = None
#the above variables are used to close the connection when tried in try cath method

app = FastAPI()

# Request Schemas
class Freelancer(BaseModel):
    name: str
    price: int

class FreelancerUpdate(BaseModel):
    name: str
    new_name: str

conn = psycopg2.connect(
	host = hostname,
	dbname = database,
	user = username,
	password = pwd,
	port = port_id)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

create_script = '''CREATE TABLE IF NOT EXISTS employee(
                        name varchar(255) NOT NULL,
                        price int)'''
cur.execute(create_script)

@app.get('/')
def index():
    cur.execute('SELECT * FROM EMPLOYEE')
    return cur.fetchall()


@app.post('/create')
def create_new_freelancer(freelancer:Freelancer):
    insert_script = 'INSERT INTO employee(name, price) VALUES(%s,%s)'
    insert_value = (freelancer.name,freelancer.price)
    cur.execute(insert_script, insert_value)
    conn.commit()
    return f"User {freelancer.name} created"

@app.post('/update')
def update_new_freelancer(freelancer_update:FreelancerUpdate):
    update_script = 'UPDATE employee SET name = %s WHERE name = %s'
    cur.execute(update_script, (freelancer_update.new_name,freelancer_update.name))
    conn.commit()
    return f"User {freelancer_update.name} is updated to {freelancer_update.new_name}"


@app.delete('/freelancer/{name}')
def delete_freelancer(name: str):
    delete_script = 'DELETE FROM employee WHERE name = %s'
    delete_record = (name,)
    cur.execute(delete_script,delete_record)
    conn.commit()
    return f"User {name} deleted"























# cur.close()
# conn.close()