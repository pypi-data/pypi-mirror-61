import os
from git import Repo
from git.exc import InvalidGitRepositoryError


class GitProjects:

    def __init__(self, path=None):
        supplied_path = os.path.join(os.environ['HOME'], 'Projects')
        path_from_env = os.path.join(os.environ['PROJECT_ROOT'], 'Projects')
        self.path = path_from_env or path or supplied_path

    def _get_top_level_directories(self, path):
        paths = next(os.walk(path))[1]
        directory_list = [os.path.join(self.path, d) for d in paths]
        return directory_list

    def get_dirty_projects(self):
        repo_directories = self._get_top_level_directories(self.path)
        dirty = []

        for d in repo_directories:
            try:
                repo = Repo(path=d)
                if repo.is_dirty():
                    dirty.append(os.path.basename(d))
            except InvalidGitRepositoryError:
                pass

        return dirty
