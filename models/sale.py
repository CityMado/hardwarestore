from extensions import db


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

    worker_id = db.Column(db.Integer(), db.ForeignKey("worker.id"))

    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date_of_sale': self.date_of_sale,
            'sale_amount': self.sale_amount,
            'who_sold': self.who_sold,
            'worker_id': self.worker_id
        }

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_publish=True).all()

    @classmethod
    def get_by_id(cls, sale_id):
        return cls.query.filter_by(id=sale_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
