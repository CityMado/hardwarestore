from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from flask_restful import Resource
from http import HTTPStatus

from models.tool import Tool


class ToolListResource(Resource):

    def get(self):

        tools = Tool.get_all_published()

        data = []

        for tool in tools:
            data.append(tool.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()

        current_worker = get_jwt_identity()

        tool = Tool(tool_name=json_data['tool_name'],
                    inventory=json_data['inventory'],
                    location=json_data['location'],
                    price=json_data['price'],
                    worker_id=current_worker)

        tool.save()

        return tool.data(), HTTPStatus.CREATED


class ToolResource(Resource):

    @jwt_optional
    def get(self, tool_id):

        tool = Tool.get_by_id(tool_id=tool_id)

        if tool is None:
            return {'message': 'Tool not found'}, HTTPStatus.NOT_FOUND

        current_worker = get_jwt_identity()

        if tool.is_publish == False and tool.worker_id != current_worker:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return tool.data(), HTTPStatus.OK

    @jwt_required
    def put(self, tool_id):

        json_data = request.get_json()

        tool = Tool.get_by_id(tool_id=tool_id)

        if tool is None:
            return {'message': 'Tool not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != tool.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        tool.tool_name = json_data['tool_name']
        tool.inventory = json_data['inventory']
        tool.location = json_data['location']
        tool.price = json_data['price']

        tool.save()

        return tool.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, sale_id):

        tool = Tool.get_by_id(sale_id=sale_id)

        if tool is None:
            return {'message': 'Tool not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != tool.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        tool.delete()

        return {}, HTTPStatus.NO_CONTENT



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
