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
            }})
		except Exception as e:
			return str(e)

		return "Successfully added {0} to {1} list!".format(first_name + " " + last_name, list_name)
		

	#get list ID from list name
	def get_listid(self, list_name):
		for x in self.client.lists.all(get_all=True, fields="lists.name,lists.id")['lists']:
			if(x['name'] == list_name):
				return x['id']

	

if __name__ == '__main__':
	handler = Handler()
	handler.app.add_url_rule('/add', 'add', handler.add_to_list, methods=['post'])
	handler.app.run(host='0.0.0.0', port=8000)


