from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus
from flask import request

from models.sale import Sale


class SaleListResource(Resource):

    def get(self):

        sales = Sale.get_all_published()

        data = []

        for sale in sales:
            data.append(sale.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()

        current_worker = get_jwt_identity()

        sale = Sale(name=json_data['name'],
                    description=json_data['description'],
                    date_of_sale=json_data['date_of_sale'],
                    sale_amount=json_data['sale_amount'],
                    who_sold=json_data['who_sold'],
                    worker_id=current_worker)

        sale.save()

        return sale.data(), HTTPStatus.CREATED


class SaleResource(Resource):

    @jwt_optional
    def get(self, sale_id):

        sale = Sale.get_by_id(sale_id=sale_id)

        if sale is None:
            return {'message': 'Sale not found'}, HTTPStatus.NOT_FOUND

        current_worker = get_jwt_identity()

        if sale.is_publish == False and sale.worker_id != current_worker:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return sale.data(), HTTPStatus.OK

    @jwt_required
    def put(self, sale_id):

        json_data = request.get_json()

        sale = Sale.get_by_id(sale_id=sale_id)

        if sale is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != sale.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        sale.name = json_data['name']
        sale.description = json_data['description']
        sale.date_of_sale = json_data['date_of_sale']
        sale.sale_amount = json_data['sale_amount']
        sale.who_sold = json_data['who_sold']

        sale.save()

        return sale.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, sale_id):

        sale = Sale.get_by_id(sale_id=sale_id)

        if sale is None:
            return {'message': 'Sale not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != sale.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        sale.delete()

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
