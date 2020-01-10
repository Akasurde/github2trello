#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import requests
import sys


class GitHubClient():
    def __init__(self):
        self.GITHUB_BASE_URL = "https://api.github.com"
        self.token = None
        self.session = None

    def create_github_session(self):
        self.session = requests.Session()
        with open(os.path.join(os.path.expanduser("~"), '.github_api')) as file_:
            token = file_.read().rstrip("\n")

        if not token:
            sys.exit("Unable to read github api file")

        self.session.headers.update({
            'Authorization': 'token %s' % token
        })

    def get_issue(self, project_full_name=None, issue_number=None):
        if not all([project_full_name, issue_number]):
            return {}
        pr_url = self.GITHUB_BASE_URL + "/repos/%s/issues/%s" % (project_full_name, issue_number)
        return self.session.get(pr_url).json()
