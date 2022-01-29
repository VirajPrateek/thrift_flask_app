import functools
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
)

from thrift.db import get_db

bp = Blueprint('tracking', __name__, url_prefix='/tracker')

@bp.route('/', methods=('GET', 'POST'))
def track():
    track_category = 'None'
    if request.method == 'POST':
        track_category = request.form['track_category']

        incomeData = getIncomeData(track_category)
        expData = getExpenditureData(track_category)

        allData = incomeData[0] + expData[0]

        sortedAllData = sorted(allData, key=lambda d: datetime.strptime(d[0], "%Y-%m-%d"), reverse = True)
        # https://stackoverflow.com/a/62732262/7696053

        return render_template('features/tracking/track.html'
        , track_category = track_category
        , allData = sortedAllData
        , totalIncome = incomeData[1] 
        , totalExp = expData[1]
        )

    return render_template('features/tracking/track.html')

def getIncomeData(category):
    db = get_db()
    incomeData = db.execute("""
                    SELECT added_date, received_by, amount 
                    FROM income 
                    WHERE source = ?
                    ORDER BY added_date DESC
                    LIMIT 15""",(category,)).fetchall()

    totaIncomeForFixedPurpose = db.execute("""
                SELECT COALESCE(SUM(amount),0) 
                FROM income WHERE source = ?
                """, (category,)).fetchone()

    db.commit()

    return [incomeData, str(totaIncomeForFixedPurpose[0])]

def getExpenditureData(category):
    db = get_db()
    expData = db.execute("""
                    SELECT spent_date, spent_by, items, amount 
                    FROM expenditure 
                    WHERE category = ?
                    ORDER BY spent_date DESC
                    LIMIT 15""",(category,)).fetchall()

    totalExpForFixedPurpose = db.execute("""
                SELECT COALESCE(SUM(amount),0) 
                FROM expenditure WHERE category = ?
                """, (category,)).fetchone()
    db.commit()

    return [expData, str(totalExpForFixedPurpose[0])]
