import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)

from thrift.db import get_db
from thrift.auth import login_required

bp = Blueprint('features', __name__, url_prefix='/features')

@bp.route('/expenditure', methods=('GET', 'POST'))
@login_required
def expenditure():
	if request.method == 'POST':
		message = None
		error = None
		dated = request.form['date']
		name = request.form['name']
		category = request.form['category']
		totalAmount = request.form['totalAmount']
		by = g.user['username']
		items = request.form['itemList']
		items = items[:-1] #removing that last comma
		if items == "":
			error = "No items entered."
		if error is None:
			db = get_db()
			db.execute(
				"""
					INSERT INTO expenditure
					(spent_date, spent_by, category, amount, items, inserted_by)
					VALUES (?,?,?,?,?,?)
				""",
				(dated, name, category, totalAmount, items, by))

			db.commit()
			message = "Data inserted!"

			flash(message)
			return redirect(url_for('home.index'))
		if error is not None:
			flash(error)
	return render_template('features/expenditure.html')

@bp.route('/income', methods=('GET','POST'))
@login_required
def income():
	if request.method == 'POST':
		message = None
		dated = request.form['date']
		name = request.form['name']
		source = request.form['source']
		amount = request.form['amount']
		remarks = request.form['remarks']
		by = g.user['username']

		db = get_db()
		db.execute(
			"""
				INSERT INTO income
				(added_date, source, inserted_by, received_by, amount, remarks)
				VALUES (?,?,?,?,?,?)
			""",
			(dated, source, by, name, amount, remarks))
		db.commit()
		message = "Data inserted!"

		if message is not None:
			flash(message)
			return redirect(url_for('home.index'))

	return render_template('features/income.html')


@bp.route('/raise_request', methods=('GET', 'POST'))
@login_required
def raise_request():
    if request.method == 'POST':
        item = request.form['item_name']
        remarks =  request.form['remarks']
        category = request.form['category']
        requested_by = g.user['username']

        db = get_db()
        db.execute(
            """
                INSERT INTO request
                (item, category, remarks, requested_by)
                VALUES(?,?,?,?)
            """,
            (item, category, remarks, requested_by)
            )
        db.commit()
        message ="Request Raised!"
        if message is not None:
            flash(message)
            return redirect(url_for('features.raise_request'))

    return render_template('features/raise_request.html')

@bp.route('/manage_request', methods = ('GET', 'POST'))
@login_required
def manage_request():
    if request.method =='POST':
    	category = request.form['category']
    	item_name = request.form['item_name']
    	dated = request.form['date']
    	amount = request.form['iAmount']
    	name = g.user['username']
    	del_id = request.form['item_id']

    	db = get_db()
    	db.execute(
				"""
				INSERT INTO expenditure
					(spent_date, spent_by, category, amount, items, inserted_by)
				VALUES (?,?,?,?,?,?)
				""",
				(dated, name, category, amount, item_name, name))
    	db.commit()
    	db = get_db()
    	db.execute('DELETE FROM request WHERE id = ?', (del_id,))
    	db.commit()
    	return redirect(request.referrer)
    return render_template('features/raise_request.html')

@bp.route('/display_data', methods=('GET','POST'))
@login_required
def display_data():
	if request.method == 'GET':
		service = request.args.get('service')
		db = get_db()
		message = None
		error = None
		data = ''
		data2 = ''
		data3 = ''
		bal = ''
		query = ''
		query2 = ''
		query3 = ''
		if service == 'balance-enquiry':
			bal = str(fetchBalance())
			tableFor = 'Balance Enquiry'

		elif service == 'exp':
			query = """
				SELECT id, spent_date, category, items, amount,
				 spent_by, inserted_by
				 FROM expenditure ORDER BY(id) DESC LIMIT 30
				"""
			tableFor = 'Expenditures'

		elif service == 'current-requests':
			query = """
				SELECT id, item, remarks, category, requested_by, 
					datetime(request_date||"-05:30") as local_time 
				 FROM request ORDER BY(id) DESC
				"""
			tableFor = 'Current Requests'

		elif service == 'income':
			query = """
				SELECT id, added_date, source, amount, received_by,
				inserted_by, remarks
				FROM income ORDER BY(id) DESC LIMIT 30
				"""
			tableFor = 'Incomes'

		elif service == 'user-list':
			query = "SELECT id, username FROM user ORDER BY(id) DESC"
			tableFor = 'Users List'

		elif service == 'insights':
		    query = """
		    SELECT spent_by, count(*), sum(amount)
		    FROM expenditure
		    GROUP BY spent_by
		    ORDER BY (count(*))
		    DESC
		    """
		    query2 = """
		    SELECT received_by, count(*), sum(amount)
		    FROM income
		    GROUP BY received_by
		    ORDER BY (count(*))
		    DESC
		    """
		    query3 = """
		    SELECT category, count(*), sum(amount)
		    FROM expenditure
		    GROUP BY category
		    ORDER BY (sum(amount))
		    DESC
		    """

		    tableFor = 'Insights'

		if service != 'balance-enquiry':
			data = db.execute(query).fetchall()
			if service == 'insights':
			    data2 = db.execute(query2).fetchall()
			    data3 = db.execute(query3).fetchall()
			db.commit()

		return render_template('features/display_data.html',
			 data = data, data2 = data2, data3 = data3,
			 bal = bal, tableFor = tableFor)

		if message is not None:
			flash(message)
		if error is not None:
			flash(error)

	return render_template('features/display_data.html')

def fetchBalance():
	db = get_db()
	totalExp = db.execute("SELECT COALESCE(SUM(amount),0) FROM expenditure").fetchone()
	db.commit()
	totalIncome = db.execute("SELECT COALESCE(SUM(amount),0) FROM income").fetchone()
	db.commit()
	avlblBalance = totalIncome[0] - totalExp[0]
	return avlblBalance


@bp.route('/lpg_update', methods=('GET','POST'))
@login_required
def lpg_update():
	query =  ''
	data = ''
	message = ''

	query = """
			SELECT id, from_date, to_date, inserted_by, remarks 
			FROM lpg 
			ORDER BY(id) DESC
			"""
	db = get_db()
	data = db.execute(query).fetchall()
	db.commit()
	
	if request.method == 'POST':
		old_to_date = request.form['to_date']
		remarks = request.form['remarks']
		inserted_by = g.user['username']
		
		new_from_date = old_to_date

		db = get_db()
		db.execute("""
			UPDATE lpg 
			SET to_date = ? 
			WHERE id = (SELECT MAX(id) FROM lpg)
			""", (old_to_date,))

		db.commit()

		db.execute("""
					INSERT INTO lpg 
					(from_date, inserted_by, remarks) 
					VALUES(?,?,?)""",
					(new_from_date, inserted_by, remarks))
		db.commit()
		message = "Data inserted!"

		if message is not None:
			flash(message)
		return redirect(url_for('home.index'))

	return render_template('features/update_lpg_data.html', data = data)