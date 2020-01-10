#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import requests
import os


class TrelloClient():
    def __init__(self):
        self.session = None
        self.auth = {
            'key': '',
            'token': '',
        }
        self.read_trello_auth()
        self.BASE_URL = "https://api.trello.com/1"
        self.headers = {
            'type': "type",
            'content-type': "application/json",
        }

    def read_trello_auth(self):
        with open(os.path.join(os.path.expanduser("~"), '.trello_key')) as file_:
            self.auth['key'] = file_.read().rstrip("\n")
        with open(os.path.join(os.path.expanduser("~"), '.trello_token')) as file_:
            self.auth['token'] = file_.read().rstrip("\n")

    def get_account_details(self):
        account_url = self.BASE_URL + "/members/me"
        response = requests.get(url=account_url, headers=self.headers, params=self.auth)
        if response.status_code == 200:
            return response.json()
        return {}

    def get_all_board_ids(self):
        boards = self.get_account_details()
        all_board_ids = []
        if boards and 'idBoards' in boards:
            all_board_ids = boards['idBoards']
        return all_board_ids

    def get_board_by_name(self, board_name=None):
        board_detail = {}
        if board_name is None:
            return board_detail
        board_url = self.BASE_URL + '/members/me/boards'
        response = requests.get(
            url=board_url,
            headers=self.headers,
            params=self.auth,
        )
        if response.status_code == 200:
            board_details = response.json()
            for i in range(len(board_details)):
                if board_details[i]['name'] == board_name:
                    return board_details[i]
        return board_detail

    def get_board_id(self, board_name=None):
        board_id = ''
        if board_name is None:
            return board_id

        board_detail = self.get_board_by_name(board_name=board_name)
        if not board_detail:
            return board_id
        return board_detail['id']

    def get_all_lists(self, board_id=None):
        if board_id is None:
            return []
        list_url = self.BASE_URL + "/boards/%s/lists" % board_id
        response = requests.get(
            url=list_url,
            headers=self.headers,
            params=self.auth,
        )
        if response.status_code == 200:
            board_lists = response.json()
            return board_lists

    def get_list_by_name(self, board_id=None, list_name=None):
        list_detail = {}
        if not any([board_id, list_name]):
            return list_detail
        all_lists = self.get_all_lists(board_id=board_id)
        for i in range(len(all_lists)):
            if all_lists[i]['name'] == list_name:
                return all_lists[i]
        return list_detail

    def create_card(self, list_id=None, card_details={}):
        if not any([list_id, card_details]):
            return False
        create_card_url = self.BASE_URL + '/cards'
        self.auth.update(card_details)
        self.auth.update({
            'idList': list_id,
            'pos': 'top',
        })
        response = requests.post(
            url=create_card_url,
            headers=self.headers,
            params=self.auth,
        )
        if response.status_code == 200:
            return response.text
        return False
