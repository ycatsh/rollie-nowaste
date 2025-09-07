from rollie import app, db
from rollie.seed import init_data


with app.app_context():
    db.create_all()
    init_data()

if __name__ == '__main__':
    app.run(debug=True)