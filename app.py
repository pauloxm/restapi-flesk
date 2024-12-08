from flask import Flask, request, jsonify
from flask import request
# Importa as bibliotecas Resource e API
from flask_restful import Resource, Api
import mariadb
import json

app = Flask(__name__)
# Comando abaixo cria API com flask Restful
api = Api(app)

# Parametros de conexão com o banco de dados
config = {
    'host': 'mariadb',
    'port': 3306,
    'user': 'root',
    'password': 'admin',
    'database': 'flask'
}

@app.route('/api/people', methods=['GET','POST'])
def index():
   # Conecta com o MariaDB
   conn = mariadb.connect(**config)
   # Cria o cursor de conexão
   cur = conn.cursor()

   json_data = []

   if request.method == 'GET':
    sql = "SELECT * FROM tasks ORDER BY id DESC"
    cur.execute(sql)
    row_headers=[x[0] for x in cur.description]
    for result in cur:
        json_data.append(dict(zip(row_headers,result)))

   if request.method == 'POST':
       data = request.get_json()
       tarefa = (data['description'], data['completed'])
       sql = "INSERT INTO tasks (description, completed) VALUES (%s, %s)"
       cur.execute(sql, tarefa)
       conn.commit()
       json_data = { 'success': True }

   # Retorna JSON com a saida
   return json.dumps(json_data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")