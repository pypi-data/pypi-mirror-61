from __future__ import print_function, unicode_literals
from ..tokens import Tokens
from ..singleton import Singleton
from github import Github
from github.GithubException import GithubException, UnknownObjectException
import os

tokens = Tokens()


class GithubHandler(metaclass=Singleton):
    _client = None
    _organization = 'primait'

    def __init__(self):
        self._client = Github(tokens.github)

    def get_repo(self, repo_name):
        return self._client.get_repo('{}/{}'.format(self._organization, repo_name))

    def get_organization(self):
        return self._client.get_organization(self._organization)

    def get_user(self):
        return self._client.get_user()

    def create_pr(self, repo, branch, title, body=''):
        return self.get_repo(repo).create_pull(title=title, head=branch, base='master', body=body)

    def get_pr(self, repo, pr_number):
        return self.get_repo(repo).get_pull(pr_number)

    def get_branch_from_pr(self, repo, pr_number):
        repo = self.get_repo(repo)
        return repo.get_branch(repo.get_pull(pr_number).head.ref)

    def get_team_members(self, team_name=""):
        return self.get_organization().get_team_by_slug(team_name).get_members()

    def get_all_users(self):
        return self.get_organization().get_members()

    def get_list_pr(self, repo):
        pulls = self.get_repo(repo).get_pulls(
            state='open', sort='created', base='master')
        return pulls

    def get_pr_from_branch(self, repo, branch):
        return self.get_repo(repo).get_pulls(
            head="{}:{}".format("primait", branch))

    def get_link_from_pr(self, repo, pr_number):
        return 'https://github.com/primait/{}/pull/{}'.format(repo, str(pr_number))

    def get_commits_since_release(self, repo, release):
        release_commit = repo.get_commit(release.tag_name)
        commits = []
        for c in repo.get_commits():
            if c == release_commit:
                break
            else:
                commits.append(c)
        return commits

    def get_latest_release_if_exists(self, repo):
        try:
            return repo.get_latest_release()
        except:
            return None

    def user_is_admin(self, repo):
        return self.get_repo(repo).permissions.admin

    def get_release_if_exists(self, repo, release):
        try:
            return repo.get_release(release)
        except:
            return None
