from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.tool import Tool, tool_list


class ToolListResource(Resource):

    def get(self):

        data = []

        for tool in tool_list:
            if tool.is_publish is True:
                data.append(tool.data)

            return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        tool = Tool(name=data['name'],
                    inventory=data['inventory'],
                    location=data['location'],
                    price=data['price'])

        tool_list.append(tool)

        return tool.data, HTTPStatus.CREATED


class ToolResource(Resource):

    def get(self, tool_id):
        tool = next((tool for tool in tool_list if tool.id == tool_id and tool.is_publish == True), None)

        if tool is None:
            return {'message': 'tool not found'}, HTTPStatus.NOT_FOUND

        return tool.data, HTTPStatus.OK

    def put(self, tool_id):
        data = request.get_json()

        tool = next(( tool for tool in tool_list if tool.id == tool_id), None)

        if tool is None:
            return {'message': 'tool not found'}, HTTPStatus.NOT_FOUND

        tool.name = data['name']
        tool.inventory = data['inventory']
        tool.location = data['location']
        tool.price = data['price']

        return tool.data, HTTPStatus.OK


class ToolPublishResource(Resource):

    def put(self, tool_id):
        tool = next((tool for tool in tool_list if tool.id == tool_id), None)

        if tool is None:
            return {'message': 'tool not found'}, HTTPStatus.NOT_FOUND

        tool.is_publish = True

        return {}, HTTPStatus.NOT_CONTENT

    def delete(self, tool_id):
        tool = next((tool for tool in tool_list if tool.id == tool_id), None)

        if tool is None:
            return {'message': 'tool not found'}, HTTPStatus.NOT_FOUND

        tool.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
