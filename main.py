#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import click
import sys
from libgithub import GitHubClient
from libtrello import TrelloClient


@click.command()
@click.option('-p', '--pr')
@click.option('-d', '--debug', help='Debug', is_flag=True, default=False)
@click.option('-b', '--board', help="Trello Board", default='VMware Ansible Development - 2.10')
@click.option('-l', '--list', default='ToDo')
def main(pr, debug, board, list):
    project_full_name = 'ansible/ansible'

    gh = GitHubClient()
    gh.create_github_session()
    issue_details = gh.get_issue(project_full_name=project_full_name, issue_number=pr)

    trello = TrelloClient()
    board_id = trello.get_board_id(board_name=board)
    todo_list = trello.get_list_by_name(board_id=board_id, list_name=list)

    card_creation_status = trello.create_card(
        list_id=todo_list['id'],
        card_details={
            'name': issue_details['title'],
            'desc': issue_details['html_url'],
        },
    )
    if card_creation_status:
        sys.exit('Card created')
    else:
        sys.exit('Failed to create ticket')


if __name__ == "__main__":
    main()
