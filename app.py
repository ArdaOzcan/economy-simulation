import datetime

import wtforms
from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, SubmitField

import logger
from models import db, SellRequests, Transactions

app = Flask(__name__)
app.config.from_pyfile("config.py")

db.init_app(app=app)


class BuyForm(FlaskForm):
    name = StringField("name")
    item_id = IntegerField("item_id")
    max_price = IntegerField("max_price")
    amount = IntegerField("amount")
    submit = SubmitField("submit")


class SellForm(FlaskForm):
    name = StringField("name")
    item_id = IntegerField("item_id")
    price = IntegerField("price")
    amount = IntegerField("amount")


# Create tables
with app.app_context():
    db.create_all()
# Clear all tables
    # db.session.query(Transactions).delete()
    # db.session.query(SellRequests).delete()
    # db.session.commit()


def handle_sell(sell_form):
    db.session.add(SellRequests(seller_name=sell_form.name.data, item_id=sell_form.item_id.data,
                                price=sell_form.price.data, amount=sell_form.amount.data))
    db.session.commit()


def handle_buy(buy_form):
    wanted_amount = int(buy_form.amount.data)
    bought_amount = 0
    sell_requests = db.session.query(SellRequests) \
        .filter(SellRequests.item_id == buy_form.item_id.data, SellRequests.price <= buy_form.max_price.data) \
        .order_by(SellRequests.price.asc())

    for req in sell_requests:
        current_wanted = wanted_amount-bought_amount
        if current_wanted == 0:
            break

        date = datetime.datetime.now() + datetime.timedelta(days=4)
        if req.amount <= current_wanted:
            logger.info(
                f"{buy_form.name.data} bought {req.amount} of item {req.item_id} from the price of {req.price} from {req.seller_name}")

            db.session.add(Transactions(date=date,
                                        seller_name=req.seller_name,
                                        buyer_name=buy_form.name.data,
                                        item_id=req.item_id,
                                        price=req.price,
                                        amount=req.amount))
            bought_amount += req.amount
            req.amount = 0
            db.session.delete(req)
        else:
            req.amount -= current_wanted
            bought_amount += current_wanted
            logger.info(
                f"{buy_form.name.data} bought {current_wanted} of item {req.item_id} from the price of {req.price} from {req.seller_name}")

            db.session.add(Transactions(date=date,
                                        seller_name=req.seller_name,
                                        buyer_name=buy_form.name.data,
                                        item_id=req.item_id,
                                        price=req.price,
                                        amount=current_wanted))

    db.session.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sell-requests")
def sell_requests():
    return render_template("sell-requests.html",
                           s_requests=db.session.query(SellRequests)
                           .order_by(SellRequests.item_id.asc(),
                                     SellRequests.price.asc()))


@app.route("/history")
def history():
    return render_template("history.html", transactions=db.session.query(Transactions).all())


@app.route("/charts")
def charts():
    transactions = db.session.query(Transactions).filter(Transactions.item_id == 0).order_by(Transactions.date)
    labels = []
    data = []
    previous_day = transactions[0].date
    day_max = 0
    for t in transactions:
        if previous_day.day != t.date.day:
            # changed day
            data.append(day_max)
            labels.append(previous_day)
            day_max = 0

        if t.price > day_max:
            day_max = t.price

        previous_day = t.date

    if labels[-1] != t.date:
        data.append(day_max)
        labels.append(t.date)

    return render_template("charts.html", server_data=[labels, data])


@app.route("/buy", methods=['GET', 'POST'])
def buy():
    if request.method == 'POST':
        form = BuyForm(request.form, csrf_enabled=False)
        if form.validate():
            handle_buy(form)
        else:
            return Response("<b>400 Bad Request</b>", 400)

    return render_template("buy.html")


@app.route("/sell", methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        form = SellForm(request.form, csrf_enabled=False)
        if form.validate():
            handle_sell(form)
        else:
            return Response("<b>400 Bad Request</b>", 400)

    return render_template("sell.html")


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
