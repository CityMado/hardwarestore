from extensions import db


class Tool(db.Model):
    __tablename__ = 'tool'

    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(200))
    inventory = db.Column(db.Integer)
    location = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    worker_id = db.Column(db.Integer(), db.ForeignKey("worker.id"))

    def data(self):
        return {
            'id': self.id,
            'tool_name': self.tool_name,
            'inventory': self.inventory,
            'location': self.location,
            'price': self.price,
            'worker_id': self.worker_id
        }

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_publish=True).all()

    @classmethod
    def get_by_id(cls, tool_id):
        return cls.query.filter_by(id=tool_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

