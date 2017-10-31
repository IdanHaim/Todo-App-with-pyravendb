from flask import Flask, render_template, request, url_for, redirect
from database import Database
from datetime import datetime
from models import Todo
import re

app = Flask(__name__)
db = Database()


@app.route('/')
def index():
    with db.document_store.open_session() as session:
        todos = list(session.query(object_type=Todo, nested_object_types={"pub_date": datetime},
                                   wait_for_non_stale_results=True).order_by_descending("pub_date"))

        incomplete = [todo for todo in todos if not todo.done]
        complete = [todo for todo in todos if todo.done]

        for todo in todos:
            todo.temp_id = re.match(pattern=r"todos\/(\d+)-", string=todo.Id, flags=re.IGNORECASE).group(1)
    return render_template('index.html', todos=todos, incomplete = incomplete, complete=complete)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        with db.document_store as store:
            with store.open_session() as session:
                title = request.form['title']
                text = request.form['text']
                session.store(Todo(title=title, text=text))
                session.save_changes()
        return redirect(url_for('index'))
    return render_template('new.html')


@app.route('/complete')
def complete():
    id = request.args.get('id')
    with db.document_store.open_session() as session:
        todo = session.load(key_or_keys=id, nested_object_types={"pub_date": datetime})
        todo.done = True
        session.save_changes()
    return redirect(url_for('index'))


@app.route('/todos/', methods=['GET', 'POST'])
def update():
    id = request.args.get('id')
    with db.document_store.open_session() as session:
        todo = session.load(id)
        if request.method == 'GET':
            return render_template('view.html', todo=todo)
        todo.title = request.form['title']
        todo.text = request.form['text']
        session.save_changes()
        return redirect(url_for('index'))


@app.route('/delete')
def delete():
    id = request.args.get('id')
    with db.document_store.open_session() as session:
        session.delete(id)
        session.save_changes()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
