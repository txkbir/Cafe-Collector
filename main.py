from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from pprint import pprint
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(label="Cafe Name", validators=[DataRequired(message="Add a cafe name")])
    location = StringField(label="Location on Google Maps", validators=[DataRequired("Add a URL"), URL(message="Invaild URL")])
    open_time = StringField(label="Opening Time (e.g. 9AM)", validators=[DataRequired(message="Add the opening time")])
    close_time = StringField(label="Closing Time (e.g. 7:30PM)", validators=[DataRequired(message="Add the closing time")])
    coffee = SelectField(label="Coffee Rating", choices=["☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"], validators=[DataRequired()])
    wifi = SelectField(label="Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    sockets = SelectField(label="Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField(label="Submit")


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST" and form.validate_on_submit(): 
        cafe = form.cafe.data
        location = form.location.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        coffee = form.coffee.data
        wifi = form.wifi.data
        sockets = form.sockets.data

        new_row = [cafe, location, open_time, close_time, coffee, wifi, sockets]

        with open("cafe-data.csv", mode='a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(new_row)

        with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            list_of_rows = [row for row in csv_data]

        return render_template("cafes.html", cafes=list_of_rows)
    
    else:
        return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows: list[list] = [row for row in csv_data]
    
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
