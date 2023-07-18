from flask import Flask, render_template, request,redirect

app = Flask(__name__)  

items =[]

@app.route('/')
def checklist():
    return render_template('checklist.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    item =request.form['item']
    items.append(item) #append the new item to the list but not yet stored in the database
    return redirect('/')

#update functionality endpoint
@app.route('/edit/<int:item_id>', methods=['GET','POST'])
def edit_item(item_id):
    item = items[item_id]  # retrieve the item based on its id

    if request.method == 'POST':
        new_item = request.form['item']
        items[item_id-1] = new_item
        return redirect('/')

    return render_template('edit.html', item=item, item_id=item_id)


#delete
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    del items[item_id-1]
    return redirect('/')


   