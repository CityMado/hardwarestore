tool_list = []


def get_last_id():
    if tool_list:
        last_tool = tool_list[-1]
    else:
        return 1
    return last_tool.id + 1


class Tool:

    def __init__(self, name, inventory, placement, price, ):
        self.id = get_last_id()
        self.name = name
        self.inventory = inventory
        self.location = location
        self.price = price
        self.is_publish = False

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name, #name of the tool
            'inventory': self.inventory, #how many is in the inventory
            'location': self.location, #location in the warehouse
            'price': self.price #price of the tool
        }
