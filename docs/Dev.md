# Development

You'll need to set up your [environment][1] before starting development
and to see if the all [dependancies][2] runs well

# oAuth
## google
1. You'll need:
    - Google account working
    - working Project on [Google APIs][3]
        * just go to [Google APIs][3] page & create a new project
2. now go to [credentials][4] tab
3. click on create credentials
4. choose `OAuth client ID`
5. choose `Web application`
6. edit your app name
7. edit `Authorized JavaScript origins` and `Authorized redirect URIs`

    <span style="color: red">imp:</span> here you'll add multible entries
    of links that your brouser/server would request data from,

    * every entry should be a valid domain
    * multiple protocoles (ex: http/https) should have multiple entries
    > do not miss to add any link even httpsL//localhost this step,
    > otherwise your app won't have access to the api from that domain

## other providers
other providers like [**Facebook**][5], **Github**, **twitter** and **paypal**
are listed to be added as a third party authintication methods, but only
providers that works properly are those which will be documented,

you may find some inside the code you work with incomplete or not working
due to changes with there APIs that are not tracked, you could neglect or
delete them but I really would be happy to see your [contribution][6] even
for a small bit of code

# testing
testing have several ways that could be done with <span style="color:
red">&</span> several purposes

1. app functionality
    * first and best method of testing any app is to try it by hands,
        this makes you find whats wrong as a client not providor
    * you could use any browser of any kind to test your app on any device
2. API
    * using [postman][7] is a good choice to see how your response would be like
    * I recommend adding API test page to your site to have an idea of what
        is the easiest way your API could be accessed
3. Code
    * your editor linter normally helps you to track errors before debugging
    * vscode could help experienced users for test and debuging
    * for code style we use [PEP.8][8] see code style below
    * no encrypted data, any data neded to be secret just read it from a file
        within untracked dir in pushing like `APP_DIR/secrets`
4. deploying
    * some functionalities could work on dev environment with differnt behavoir
        on the server,

        although this is rare, you should keep it in mind especially when you
        work with any thing related by certificates (ssl) or sys permissions


# Style Guide
As mentioned before code goes on [PEP.8][8] style guide

you could use [pycodestyle][9] ( installed within requirments ) or the it's old
name [pep8][10] to test your code and find what is not matching this style guide

> you'll notice that testing with both tools is better

if you found yourself stacked with too much errors from either of both tools
you could use a tool like autopep8

usage will be like this

```bash
# only use autopep8 with python files recrusively
du -a $directory |awk '{print $2}' |grep '\.py$' \
|xargs -n1 autopep8 --in-place --aggressive --aggressive

# test after ending
pycodestyle .
```
> autopep8 is a great tool but not a perfect on
> that you'll need to test after it for some small guide lines missed
> or some code which sectioned with an eye non comforting way

any code that meets this style guide, tested and functionally worked
with no issues wil be accepted as a pull request <span style="color:
red">unless</span>:
- being uncomplete step of a functionality

    inconplete steps for [next step functionality][11] will be accepet
    if correct
- an already stable well precoded functionality exists


[1]: ins.md#environment
[2]: ins.md#dependancies
[3]: https://console.developers.google.com
[4]: https://console.developers.google.com/apis/credentials
[5]: https://developers.facebook.com/docs/facebook-login/web
[6]: /.READs/contribute.md
[7]: https://www.getpostman.com
[8]: https://www.python.org/dev/peps/pep-0008
[9]: http://pycodestyle.pycqa.org/en/latest/intro.html
[10]: https://pep8.readthedocs.io/en/release-1.7.x/
[11]: to_do.md#next-step