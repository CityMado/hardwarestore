from extensions import db

tool_list = []


def get_last_id():
    if tool_list:
        last_tool = tool_list[-1]
    else:
        return 1
    return last_tool.id + 1


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