"""Console script for techbox."""
import sys

import fire

from .snippets import print_snippet, get_snippet
from .git import GitProjects




def snippet():
    fire.Fire(generate_snippet)




class TechboxCli:
    
    @staticmethod
    def snippet(path, from_line, to_line):
        snippet = get_snippet(path, from_line, to_line)
        print_snippet(snippet)

    project = GitProjects()


def ep():
    fire.Fire(TechboxCli)
