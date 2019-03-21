"""usage: git checkout [options] <branch>
       git checkout [options] <branch> -- <file>...

    -q, --quiet           suppress progress reporting
    -b <branch>           create and checkout a new branch
    -B <branch>           create/reset and checkout a branch
    -l                    create reflog for new branch
    -t, --track           set upstream info for new branch
    --orphan <new branch>
                          new unparented branch
    -2, --ours            checkout our version for unmerged files
    -3, --theirs          checkout their version for unmerged files
    -f, --force           force checkout (throw away local modifications)
    -m, --merge           perform a 3-way merge with the new branch
    --conflict <style>    conflict style (merge or diff3)
    -p, --patch           select hunks interactively

"""
from docopt import docopt


if __name__ == "__main__":
    print(docopt(__doc__))
