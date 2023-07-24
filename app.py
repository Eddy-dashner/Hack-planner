from flask import Flask, render_template, request,redirect
import sqlite3
app = Flask(__name__)  

items =[]
db_path = 'checklist.db'

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS checklist
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)''')
    conn.commit()
    conn.close()

def get_items():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM checklist")
    items = c.fetchall()
    conn.close()
    return items

def add_item_to_db(item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO checklist (item) VALUES (?)", (item,))
    conn.commit()
    conn.close()

def update_item(item_id, new_item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE checklist SET item = ? WHERE id = ?", (new_item, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM checklist WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

@app.route('/')
def checklist():
    create_table()
    items =get_items()
    return render_template('checklist.html', items=items)

@app.route('/add', methods=['POST'])
def add_item_route():
    item = request.form['item']
    add_item_to_db(item)  # Call the renamed function
    return redirect('/')

#update functionality endpoint
@app.route('/edit/<int:item_id>', methods=['GET','POST'])
def edit_item(item_id):
    # item = items[item_id]  # retrieve the item based on its id

    if request.method == 'POST':
        new_item = request.form['item']
        update_item(item_id, new_item)
        return redirect('/')
    else:
        items = get_items()
        item= next((x[1]for x in items if x[0] == item_id), None)
        return render_template('edit.html', item=item, item_id=item_id)


#delete
@app.route('/delete/<int:item_id>')
def delete_item_route(item_id):
    delete_item(item_id)  # Call the appropriate function
    return redirect('/')


   