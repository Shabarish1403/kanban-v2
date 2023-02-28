from flask_restful import Resource, fields, marshal_with, reqparse, marshal
from application.models import User, List, Card
from application.validation import NotFoundError, BusinessValidationError
from .database import db
from datetime import datetime as dt
import string, random
from pprint import pprint
import copy
from flask_security import auth_required
# from main import cache


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'active': fields.Boolean,
    'fs_uniquifier': fields.String,
}

user_parser = reqparse.RequestParser()
user_parser.add_argument('email')
user_parser.add_argument('name')
user_parser.add_argument('password')


class UserAPI(Resource):
    # @cache.cached(timeout=50, key_prefix='get_user_api')
    @auth_required('token')
    def get(self, email):
        user = User.query.filter_by(email=email).first()
        data = {}
        data['id'] = user.id
        data['name'] = user.name
        l_api = ListAPI()
        lists = l_api.get(user.id)
        data['lists'] = lists
        for (i,l) in enumerate(lists):
            c_api = CardAPI()
            cards = c_api.get(l['id'])
            data['lists'][i]['cards'] = cards
        return data
    
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        email = args.get('email',None)
        name = args.get('name',None)
        password = args.get('password',None)
        active = 1
        fs_uniquifier = ''.join(random.choices(string.ascii_letters,k=10))
        user = User(email=email, name=name, password=password, active=active, fs_uniquifier=fs_uniquifier)
        db.session.add(user)
        db.session.commit()
        return user, 201


toggle_parser = reqparse.RequestParser()
toggle_parser.add_argument('toggle')

class ToggleAPI(Resource):
    @auth_required('token')
    def put(self, card_id):
        args = toggle_parser.parse_args()
        toggle = args.get('toggle')

        card = Card.query.get(card_id)
        l = List.query.get(card.list_id)

        if toggle == '1':
            card.toggle = 1
            card.complete_date = dt.isoformat(dt.today())
        else:
            card.toggle = 0
            card.complete_date = 'Not completed'
        db.session.commit()
        return 201

class ExportAPI(Resource):
    @auth_required('token')
    def get(self, user_id, list_id):
        if list_id == 'null':
            user = User.query.get(user_id)
            lists = user.lists
            d = []
            for lst in lists:
                temp = {}
                flag = True
                temp['user_id'] = user_id
                temp['list_id'] = lst.id
                temp['list_name'] = lst.name
                temp['update_date'] = lst.update_date
                for card in lst.cards:
                    flag = False
                    temp['card_id'] = card.id
                    temp['card_name'] = card.name
                    temp['card_content'] = card.content
                    temp['card_deadline'] = card.deadline
                    temp['toggle'] = card.toggle
                    temp['card_create_date'] = card.create_date
                    temp['card_complete_date'] = card.complete_date
                    d.append(copy.deepcopy(temp))
                if flag:
                    d.append(temp)
        else:
            lst = List.query.get(list_id)
            d = []
            for card in lst.cards:
                temp = {}
                temp['user_id'] = user_id
                temp['list_id'] = list_id
                temp['list_name'] = lst.name
                temp['card_id'] = card.id
                temp['card_name'] = card.name
                temp['card_content'] = card.content
                temp['card_deadline'] = card.deadline
                temp['toggle'] = card.toggle
                temp['card_create_date'] = card.create_date
                temp['card_complete_date'] = card.complete_date
                d.append(temp)
        return d

list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'update_date': fields.String,
    'user_id': fields.Integer,
}

list_parser = reqparse.RequestParser()
list_parser.add_argument('name')

class ListAPI(Resource):
    @marshal_with(list_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            l = user.lists
            return l
        else:
            raise NotFoundError(status_code=404)

    @auth_required('token')
    @marshal_with(list_fields)
    def post(self, user_id):
        args = list_parser.parse_args()
        name = args.get('name', None)
        update_date = dt.isoformat(dt.now())

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='LIST001', error_message='List Name is required')

        l = List.query.filter_by(name=name,user_id=user_id).first()
        if l is not None:
            raise BusinessValidationError(status_code=400, error_code='LIST002', error_message='List Name already exists')
        
        l = List(name=name,update_date=update_date ,user_id = user_id)
        db.session.add(l)
        db.session.commit()
        return l, 201

    @auth_required('token')
    def delete(self, list_id):
        l = List.query.get(list_id)
        if l is None:
            raise NotFoundError(status_code=404)
        else:
            db.session.delete(l)
            db.session.commit()
            return "Successfully Deleted"

    @auth_required('token')
    @marshal_with(list_fields)
    def put(self, list_id):
        l = List.query.get(list_id)
        if l is None:
            raise NotFoundError(status_code=404)

        args = list_parser.parse_args()
        name = args.get('name', None)

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='LIST001', error_message='List Name is required')

        new = List.query.filter_by(name=name,user_id=l.user_id).first()
        if l.name == name or new == None:
            l.name = name
            l.update_date = dt.isoformat(dt.now())
            db.session.commit()
            return l,200
        else:
            raise BusinessValidationError(status_code=400, error_code='LIST002', error_message='List Name already exists')



card_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'content': fields.String,
    'deadline': fields.String,
    'toggle': fields.String,
    'create_date': fields.String,
    'complete_date': fields.String,
    'list_id': fields.Integer
}

card_parser = reqparse.RequestParser()
card_parser.add_argument('name')
card_parser.add_argument('content')
card_parser.add_argument('deadline')
card_parser.add_argument('toggle')
card_parser.add_argument('list_id')

class CardAPI(Resource):
    @marshal_with(card_fields)
    def get(self, list_id):
        l = List.query.get(list_id)
        if l:
            c = []
            for card in l.cards:
                c.append(card)
            return c
        else:
            raise NotFoundError(status_code=404)

    @auth_required('token')
    @marshal_with(card_fields)
    def post(self, list_id):
        args = card_parser.parse_args()
        name = args.get('name', None)
        content = args.get('content', None)
        deadline = args.get('deadline', None)
        toggle = '0'
        create_date = dt.isoformat(dt.now())
        complete_date = 'Not completed'

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='CARD001', error_message='Card Name is required')

        if deadline is None:
            raise BusinessValidationError(status_code=400, error_code='CARD002', error_message='Deadline is required')

        today = dt.today().strftime('%Y-%m-%d')
        if deadline < today:
            raise BusinessValidationError(status_code=400, error_code='CARD003', error_message='The Date must be bigger or Equal to today date')

        card = Card.query.filter_by(name=name,list_id=list_id).first()
        if card is not None:
            raise BusinessValidationError(status_code=400, error_code='CARD004', error_message='Card Name already exists in the given list')
        
        c = Card(name=name, content=content, deadline=deadline, toggle=toggle, create_date=create_date, complete_date=complete_date ,list_id=list_id)
        l = List.query.get(list_id)
        l.update_date = dt.isoformat(dt.now())
        db.session.add(c)
        db.session.commit()
        return c, 201

    @auth_required('token')
    def delete(self, card_id):
        card = Card.query.get(card_id)
        if card is None:
            raise NotFoundError(status_code=404)
        else:
            db.session.delete(card)
            db.session.commit()
            return "Successfully Deleted"

    @auth_required('token')
    @marshal_with(card_fields)
    def put(self, card_id):
        card = Card.query.get(card_id)
        if card is None:
            raise NotFoundError(status_code=404)

        args = card_parser.parse_args()
        name = args.get('name', None)
        content = args.get('content', None)
        deadline = args.get('deadline', None)
        toggle = args.get('toggle', None)
        list_id = args.get('list_id', None)

        if list_id is None:
            raise BusinessValidationError(status_code=400, error_code='LIST003', error_message='List Id is required')

        l = List.query.get(list_id)
        if l is None:
            raise NotFoundError(status_code=404)

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='CARD001', error_message='Card Name is required')
        
        if deadline is None:
            raise BusinessValidationError(status_code=400, error_code='CARD002', error_message='Deadline is required')

        today = dt.today().strftime('%Y-%m-%d')
        if deadline < today:
            raise BusinessValidationError(status_code=400, error_code='CARD003', error_message='The Date must be bigger or Equal to today date')

        flag = False
        c = Card.query.filter_by(name=name,list_id=list_id).first()
        if card.list_id == int(list_id):
            if card.name == name or c == None:
                flag = True
        elif c == None:
            card.list_id = list_id
            flag = True
        
        if flag:
            card.name = name
            card.content = content
            card.deadline = deadline
            card.toggle = toggle
            l.update_date = dt.isoformat(dt.now())
            db.session.commit()
            return card,200
        else:
            raise BusinessValidationError(status_code=400, error_code='CARD004', error_message='Card Name already exists in the given list')