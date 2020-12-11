from flask_restful import Resource
from http import HTTPStatus
from flask import request

from models.sale import Sale, sale_list


class SaleListResource(Resource):

    def get(self):

        data = []

        for sale in sale_list:
            if sale.is_publish is True:
                data.append(sale.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        sale = Sale(name=data['name'],
                    description=data['description'],
                    date_of_sale=data[' date_of_sale'],
                    sale_amount=data['sale_amount'],
                    who_sold=data['who_sold'])

        sale_list.append(sale)

        return sale.data, HTTPStatus.CREATED


class SaleResource(Resource):

    def get(self, sale_id):
        sale = next((sale for sale in sale_list if sale.id == sale_id and sale.is_publish == True), None)

        if sale is None:
            return {'message': 'sale not found'}, HTTPStatus.NOT_FOUND

        return sale.data, HTTPStatus.OK

    def put(self, sale_id):
        data = request.get_json()

        sale = next((sale for sale in sale_list if sale.id == sale_id), None)

        if sale is None:
            return {'message': 'sale not found'}, HTTPStatus.NOT_FOUND

        sale.name = data['name']
        sale.description = data['description']
        sale.date_of_sale = data['date_of_sale']
        sale.sale_amount = data['sale_amount']
        sale.who_sold = data['who_sold']

        return sale.data, HTTPStatus.OK

    def delete(self, sale_id):
        sale = next((sale for sale in sale_list if sale.id == sale_id), None)

        if sale is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        sale_list.remove(sale)

        return {}, HTTPStatus.NO_CONTENT


class SalePublishResource(Resource):

    def put(self, sale_id):
        sale = next((sale for sale in sale_list if sale.id == sale_id), None)

        if sale is None:
            return {'message': 'sale not found'}, HTTPStatus.NOT_FOUND

        sale.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, sale_id):
        sale = next((sale for sale in sale_list if sale.id == sale_id), None)

        if sale is None:
            return {'message': 'sale not found'}, HTTPStatus.NOT_FOUND

        sale.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
