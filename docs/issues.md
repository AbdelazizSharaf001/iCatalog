# issues
> Pull requests and stars are always welcome.

For bugs and feature requests, [Kindly create an issue](/../../issues/new).


# Common issues

- Flask-SQLAlchemy.orm

    This sub class of the module sometimes raise many confusing
    errors when developing that each leads to others

    there is two states that could happen
    1. working outside SQLAlchemy session scope

        after commiting, SQLAlchemy session is being expired,
        that makes an error cycle of out of various errors when
        working with a pre commit instance

        this is bieng solved by initing the engine with
        session_options: expire_on_commit > False

        ```python
        SQLAlchemy(session_options={'expire_on_commit': False})
        ```

    
    2. template syntax error along with an instance of SQLAlchemy

        when an error is raised from a template showing muliple
        statements of html as an error place, just work around last
        things you modifed in the template related to SQLAlchemy,
        and note that the error arised is not correct, the correct
        is that you have syntax error in a statement (usually if)
        that contains SQLAlchemy instance.

- oAuth2
    1. google sign in api button stopped working on https returning
        an error with https

        you are runing the server with `adhoc` or self signed
        certificate that hasn't been verified

        use `start.sh` to generate ssl crt & key then run
        the script using `ssl_cert` option and not adhoc,

        > note that you could modify that bash file to fit your needs

    2. Sign in button disappeared

        Ok it's not disappeared, it's removed..

        the script couldn't / limited from getting state value to
        sign in with, so removed the button

        this could happen when
        * sending the wrong state to the server
        * no client_secrets file provided for the script
        * trying to access the server from a different domain that
            are listed in Google client secrets
        * state is prevented by the server for development or
            not supporting it
