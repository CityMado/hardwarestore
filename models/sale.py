from extensions import db

sale_list = []


def get_last_id():
    if sale_list:
        last_sale = sale_list[-1]
    else:
        return 1
    return last_sale.id + 1


class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    date_of_sale = db.Column(db.Integer)
    sale_amount = db.Column(db.Integer)
    who_sold = db.Column(db.String(1000))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))