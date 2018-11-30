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

	def printList(self):
		req = request.get_json()
		return self.jsonify(self.client.lists.all(get_all=True, fields="lists.name,lists.id"))


	def jsonify(self, data):
		res = make_response(json.dumps(data))
		return res


	

if __name__ == '__main__':
	handler = Handler()
	handler.app.add_url_rule('/add', 'add', handler.printList, methods=['post'])
	handler.app.run(host='0.0.0.0', port=8000)