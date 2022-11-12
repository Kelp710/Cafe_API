from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,Length, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe location", validators=[DataRequired(), URL()])
    open_hour = StringField("Open time", validators=[DataRequired()])
    close_hour = StringField("Close time", validators=[DataRequired()])
    coffee = SelectField("Coffee quality", choices=[("✘","✘"),("☕","☕"), ("☕☕",'☕☕'), ("☕☕☕",'☕☕☕'), ("☕☕☕☕",'☕☕☕☕'),("☕☕☕☕☕",'☕☕☕☕☕')],validators=[DataRequired()])
    wifi = SelectField("wifi strength", choices=[("✘","✘"),("💪","💪"), ("💪💪",'💪💪'), ("💪💪💪",'💪💪💪'), ("💪💪💪💪",'💪💪💪💪'),("💪💪💪💪💪",'💪💪💪💪💪')],validators=[DataRequired()])
    power = SelectField("Power", choices=[("✘","✘"),("🔌","🔌"), ("🔌🔌",'🔌🔌'), ("🔌🔌🔌",'🔌🔌🔌'), ("🔌🔌🔌🔌",'🔌🔌🔌🔌'),("🔌🔌🔌🔌🔌",'🔌🔌🔌🔌🔌')],validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open_hour time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        with open('cafe-data.csv', newline='', encoding="utf-8", mode="a") as csv_file:
            cafe_name = str(form.cafe.data)
            location = str(form.location.data)
            open_hour = str(form.open_hour.data)
            close_hour = str(form.close_hour.data)
            coffee = str(form.coffee.data)
            wifi = str(form.wifi.data)
            power = str(form.power.data)
            csv_file.write(f'{cafe_name}')
            csv_file.write(f',"{location}"')
            csv_file.write(f',{open_hour},{close_hour},{coffee},{wifi},{power}\n')
        return redirect(url_for('cafes'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
