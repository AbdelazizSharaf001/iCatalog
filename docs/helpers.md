# Helpers
some files that will help you developing

# bash
`start.sh [bash]`

A well organized bash script tested on ubuntu environment that could be helping
for more than one python project a the same time

script has no GUI thus you'll need a shell to only type one word thin your work
will be choosing how to run unless you choosen to customize some options

```bash
$ ./start.sh
```
```
Select process number or any other thing to exit: 
1) clear         3) requirements  5) autopep8      7) deploy
2) run           4) test          6) push
#?
```
> note: important to note any data you need from the shell as script clears
    the shel whenever starting or terminated

- options
    > typing any thing except for options clear the screen and exit
    * clear:
    
        clear workspace

    * run:

        Run the app

        [c] customize host, port & FLASK_APP dir.

        https check [ ssl_cert/adhoc ]
        1. ssl_cert: use self signed certificate to run https
        2. adhoc: use flask adhoc config to run https
            > not good with cross site APIs or scripts like facebook sdk
            as the script doesn't specify a valid certificate for to
            the browser to authorize connection

        [ dev/test/production/wsgi ]
        1. dev: development flask debuging server
        2. test: testing flask debuging server
        3. production: production flask server
        4. wsgi: wsgi server powered by `gunicorn (installed with requirements)`

    * requirements:

        install requirements ( pip|ssl )

        *   install requirements.txt (pip) [ pipenv/pip3/pip ]
            1. pipenv: install python required modules on the virtual
                active environment
            1. pip3: install python required modules for python3
            1. pip: install python required modules for python2
        * ssl (self signed certificate) [Y|N]*

            create a self signed certificate to run https on development server

            openssl package is required

    * test:
    
        Test only python files [ pycodestyle|PEP.8 ]
        
        both are the same tool but PEP8 is the old name
        > both is here as there are some changes from one to another
        in output that doesn't make conflect

    * autopep8:

        automatic style severy pythonscript inside i_catalog folder to fit
        PEP8 specifications

        autopep8 should be installed

    * push:
    
        push to github master branch

        git is required

    * deploy:
        
        deploy on heruku [heroku/git]

        1. heroku: push project to heroku original repo
        
            heroku-cli & git are required
            
        2. git: push project to heroku branch on git repo

            git is required
            
            this is for automatic deploying from git from custom branch

            default branch: heroku

            if you do so but from master thin use push opthon insteade of deploy
            