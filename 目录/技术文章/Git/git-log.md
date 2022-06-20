# Git log

2022-06-05

## Git history simplification

> https://docs.microsoft.com/en-us/azure/devops/repos/git/git-log-history-simplification?view=azure-devops

> https://stackoverflow.com/questions/56553346/git-log-missing-merge-commit-that-undid-a-change

Understand Git history simplification

The thing about history simplification is that most of the time you will never notice it. But when a merge conflict goes wrong and you want to know what happened -- you may find yourself looking at the git log history and wondering where your changes went.

Now, instead of panicking, you know that:

History simplification for files is turned on by default
The --full-history flag will give you a more comprehensive file history

## Other optional method to view modified parts

full command:
```bash
git log -p -m file.txt
```

```
--diff-merges=m
-m
```
This option makes diff output for merge commits to be shown in the default format. -m will produce the output only if -p is given as well. The default format could be changed using log.diffMerges configuration parameter, which default value is separate.


```
--diff-merges=combined
--diff-merges=c
-c
```
With this option, diff output for a merge commit shows the differences from each of the parents to the merge result simultaneously instead of showing pairwise diff between a parent and the result one at a time. Furthermore, it lists only files which were modified from all parents. -c implies -p.

```
--diff-merges=dense-combined
--diff-merges=cc
--cc
```
With this option the output produced by --diff-merges=combined is further compressed by omitting uninteresting hunks whose contents in the parents have only two variants and the merge result picks one of them without modification. --cc implies -p