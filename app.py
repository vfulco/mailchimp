# -*- coding: utf-8 -*-
import json
import os
import sys
import requests


from flask import Flask, make_response, request
from flask import jsonify
from mailchimp3 import MailChimp



class Handler:
	app = Flask(__name__)

	def __init__(self):
		self.client = MailChimp(mc_api=os.getenv('API_KEY'), mc_user=os.getenv('USERNAME'))
		return None


	def add_to_list(self):
		req = request.get_json()
		list_name = req['list_name']
		user_email = req['user_email']
		status = req['status']
		first_name = req['first_name']
		last_name = req['last_name']
		list_id = self.get_listid(list_name)

		try:
			self.client.lists.members.create(list_id, {
			'email_address': user_email,
			'status': status,
			'merge_fields': {
			'FNAME': first_name,
			'LNAME': last_name,
			},
			})
		except Exception as e:
			return str(e)

		return "Successfully added {0} to {1} list.".format(first_name + " " + last_name, list_name)
		



	def delete_from_list(self):
		req = request.get_json()
		list_name = req['list_name']
		user_email = req['user_email']
		list_id = self.get_listid(list_name)
		user_id = self.get_user_id(list_id, user_email)

		try:
			self.client.lists.members.delete(list_id, user_id)
		except Exception as e:
			return str(e)

		return "Successfully deleted {0} from {1} list".format(user_email, list_name)

		
	def add_tags(self):
		req = request.get_json()
		list_name = req['list_name']
		user_email = req['user_email']
		tag_name = req['tag']
		list_id = self.get_listid(list_name)
		user_id = self.get_user_id(list_id, user_email)
		data = {'tags': [{'name': tag_name, 'status': 'active'}]}
		

		try:
			self.client.lists.members.tags.update(list_id, user_id, data)
		except Exception as e:
			return str(e)

		return "Successfully added the tag {0} to {1}".format(tag_name, user_email)



	#get list ID from list name
	def get_listid(self, list_name):
		for x in self.client.lists.all(get_all=True, fields="lists.name,lists.id")['lists']:
			if(x['name'] == list_name):
				return x['id']

	def get_user_id(self, list_id, user_email):
		for x in self.client.lists.members.all(list_id, get_all=True, fields="members.email_address,members.id")['members']:
			if (x['email_address'] == user_email):
				return x['id']


if __name__ == '__main__':
	handler = Handler()
	handler.app.add_url_rule('/add', 'add', handler.add_to_list, methods=['post'])
	handler.app.add_url_rule('/delete', 'delete', handler.delete_from_list, methods=['post'])
	handler.app.add_url_rule('/addtag', 'addtag', handler.add_tags, methods=['post'])
	handler.app.run(host='0.0.0.0', port=8000)


