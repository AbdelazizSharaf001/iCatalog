# How to contribute

I'm really glad you're reading this, because the community needs your efforts.

if this is your first contribute on github,
those are some helpfull rasorces to do that perfectly:
1. [Setting guidelines for repository contributors][x1]
2. [How to contribute to a project on Github][x2]

## Testing

We don't have a specific teaching technique to go throw,
but please read how we started [testing][1] to meet our minimum small tests

## Submitting changes

Please send a [GitHub Pull Request to iCatalog][2] with a clear list of what
you've done (read more about [pull requests][3]).

Please follow our coding conventions (+along with PEP8) and make sure all of
your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

```bash
$ git commit -m "A brief summary of the commit
> 
> A paragraph describing what changed and its impact."
```

## Coding conventions

Start reading our code and you'll get the hang of it. We optimize for readability:

- starting from [PEP8][4]
- importing more than 3 subclasses from a module (or subclass)
    should be separated in multilines like this
    ```python
    from flask import (
        Flask,
        jsonify,
        Blueprint,
        render_template
    )
    ```
    same thing with long names
- imports are orderd in stair like order the less name length followed
    by longer till longest, like this
    ```python
    from . import db, login_manager
    from .fn import rand_str
    from .crud import cuCRUD, rCRUD, gen_pid, gen_tk
    from .models import Usr
    ```
    also multiline subclasses
- only import subclass you need and do not import the itire module as all
- use functional or Object Oreinted Programing as you could instaid off
    proceedual programming
-
- avoid comments inside templates
- comment everything you do with a jonuor/student readable comments

# finally
- have a look on previous code

    ```
    of course I can't be a successful if no one succeded,
    it's for education [the project and it's code
    ```

**Thanks for even being here**


[x1]: https://help.github.com/en/github/building-a-strong-community/setting-guidelines-for-repository-contributors
[x2]: https://gist.github.com/7303312.git

[1]: https://github.com/AbdelazizSharaf001/iCatalog/tree/master/docs/Dev.md#testing
[2]: https://github.com/AbdelazizSharaf001/iCatalog/pull/new/master
[3]: http://help.github.com/pull-requests/
[4]: https://www.python.org/dev/peps/pep-0008