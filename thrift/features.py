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
		dated = request.form['date']
		name = request.form['name']
		category = request.form['category']
		totalAmount = request.form['totalAmount']
		by = g.user['username']
		items = request.form['itemList']
		message = None
		message = "received data.. yet NOT  Inserted"

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
		
		if message is not None:
			flash(message)
			return redirect(url_for('home.index'))
		
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

		message = "Recieved data.. NOT yet inserted!"

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


@bp.route('/display_data', methods=('GET','POST'))
@login_required
def view():
	if request.method == 'POST':
		service = request.form['service']
		db = get_db()
		message = None

		if service == 'balance-enquiry':
			bal = str(fetchBalance())
			tableFor = 'Balance Enquiry'
			return render_template('features/display_data.html', 
				bal = bal, tableFor = tableFor)

		elif service == 'last-exp':
			data = db.execute("""
				SELECT id, spent_date, category, items, amount,
				 spent_by, inserted_by 
				 FROM expenditure
				 WHERE id=(
				 	SELECT MAX(id) FROM expenditure
				 	)
				""").fetchall()

			# message = 'Under construction..'+str(data[0][2])
			db.commit()
			tableFor = 'Last Expenditure'
			return render_template('features/display_data.html',
			 data = data, tableFor = tableFor)
		
		elif service == 'all-exp':
			data = db.execute("""
				SELECT id, spent_date, category, items, amount,
				 spent_by, inserted_by 
				 FROM expenditure ORDER BY(id) DESC
				""").fetchall()
			db.commit()
			tableFor = ' All Expenditure'
			return render_template('features/display_data.html',
			 data = data, tableFor = tableFor)

		elif service == 'last-income':
			data = db.execute("""
				SELECT id, added_date, source, amount, received_by, 
				inserted_by, remarks 
				 FROM income
				 WHERE id=(
				 	SELECT MAX(id) FROM income
				 	)
				""").fetchall()

			db.commit()
			tableFor = 'Last Income'
			return render_template('features/display_data.html',
			 data = data, tableFor = tableFor)

		elif service == 'all-income':
			data = db.execute("""
				SELECT id, added_date, source, amount, received_by, 
				inserted_by, remarks 
				FROM income ORDER BY(id) DESC
				""").fetchall()
			db.commit()
			tableFor = 'All Income'
			return render_template('features/display_data.html',
			 data = data, tableFor = tableFor)
		
		if message is not None:
			flash(message)

	return render_template('features/display_data.html')

def fetchBalance():
	db = get_db()
	totalExp = db.execute("SELECT SUM(amount) FROM expenditure").fetchone()
	db.commit()
	totalIncome = db.execute("SELECT SUM(amount) FROM income").fetchone()
	db.commit()
	avlblBalance = totalIncome[0] - totalExp[0]
	return avlblBalance
