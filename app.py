from flask import Flask, render_template, request, url_for, redirect
from flask_paginate import Pagination, get_page_parameter
from database import Database
from models import Todo
from datetime import datetime

app = Flask("PyRavenDB_Todo")
POSTS_PER_PAGE = 10
context = None


def run_app(debug=False):
    global context
    app.config["DATABASE_URLS"] = ["http://localhost:8080"]
    app.config["DATABASE_NAME"] = "todo"
    app.config["DEBUG"] = debug

    context = app.app_context()
    Database.create_database(context)
    app.run()


def get_store():
    return Database.get_store(context)


@app.route('/')
def index():
    with get_store().open_session() as session:
        page = request.args.get(get_page_parameter(), type=int, default=1)

        todos, stats = list(session.query(object_type=Todo, with_statistics=True).order_by(
            "done").order_by_descending("complete_date").order_by_descending("pub_date").take(POSTS_PER_PAGE).skip(
            (page - 1) * POSTS_PER_PAGE))
        incomplete_total_result = stats['TotalResults']

        pagination = Pagination(page=page, total=incomplete_total_result, record_name='todos')
        return render_template('index.html', todos=todos, pagination=pagination)


@app.route('/completed')
def completed_items():
    with get_store().open_session() as session:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        completed, stats = list(session.query(object_type=Todo, with_statistics=True).order_by_descending(
            "complete_date").where(done=True).take(POSTS_PER_PAGE).skip((page - 1) * POSTS_PER_PAGE))
        complete_total_result = stats['TotalResults']

        pagination = Pagination(page=page, total=complete_total_result, record_name='completed todos')
        return render_template('completed.html', completed_items=completed, pagination=pagination)


@app.route('/uncompleted')
def uncompleted():
    with get_store().open_session() as session:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        uncompleted, stats = list(session.query(object_type=Todo, with_statistics=True).order_by_descending(
            "pub_date").where(done=False).take(POSTS_PER_PAGE).skip((page - 1) * POSTS_PER_PAGE))
        incomplete_total_result = stats['TotalResults']

        pagination = Pagination(page=page, total=incomplete_total_result, record_name='uncompleted todos')
        return render_template('uncompleted.html', uncompleted=uncompleted, pagination=pagination)


@app.route('/new', methods=['POST'])
def create():
    with get_store().open_session() as session:
        title = request.form['title']
        text = request.form['text']
        session.store(Todo(title=title, text=text))
        session.save_changes()
        return redirect(url_for('index'))


@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@app.route('/complete')
def complete():
    id = request.args.get('id')
    with get_store().open_session() as session:
        todo = session.load(id)
        todo.done = True
        todo.complete_date = datetime.utcnow()
        session.save_changes()
        return redirect(url_for('index'))


@app.route('/incomplete')
def incomplete():
    id = request.args.get('id')
    with get_store().open_session() as session:
        todo = session.load(id)
        todo.done = False
        todo.complete_date = None
        session.save_changes()
        return redirect(url_for('index'))


@app.route('/todos', methods=['POST'])
def update():
    r = request
    id = request.args.get('id')
    with get_store().open_session() as session:
        todo = session.load(id)
        todo.title = request.form['title']
        todo.text = request.form['text']
        session.save_changes()
        return redirect(url_for('index'))


@app.route('/todos', methods=['GET'])
def view():
    id = request.args.get('id')
    with get_store().open_session() as session:
        todo = session.load(id)
        return render_template('view.html', todo=todo)


@app.route('/delete')
def delete():
    id = request.args.get('id')
    with get_store().open_session() as session:
        session.delete(id)
        session.save_changes()
        return redirect(url_for('index'))


if __name__ == "__main__":
    run_app(debug=False)
