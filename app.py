from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Inicializa base de datos
def init_db():
    conn = sqlite3.connect('tareas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY, descripcion TEXT, completada BOOLEAN)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tareas.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tareas')
    tareas = c.fetchall()
    conn.close()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    descripcion = request.form['descripcion']
    conn = sqlite3.connect('tareas.db')
    c = conn.cursor()
    c.execute('INSERT INTO tareas (descripcion, completada) VALUES (?, ?)', (descripcion, False))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/completar/<int:id>')
def completar(id):
    conn = sqlite3.connect('tareas.db')
    c = conn.cursor()
    c.execute('UPDATE tareas SET completada = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = sqlite3.connect('tareas.db')
    c = conn.cursor()
    c.execute('DELETE FROM tareas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
