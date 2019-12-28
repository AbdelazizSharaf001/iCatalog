# Installation

## Dependancies

- python
    * v3.x | `v2 is not fully tested`
    * pip3
- Database
    * SQLAlchemy
    * Flask
- oAuth
    * secrets of your app on oAuth provider

## environment
- Device / server machine
    * ram: 4GB+ `for your device health`
- system
    * any system that runs python
    * any vertual environment
        1. virtualenv
            [ python module | recommended by `flask` official site]
        2. virtualbox
            [ recommended by Course instructors `UdacityFSND` ]
        3. pipenv
            [ heroku pips installer ]
        4. VMware
            [ `commercial` | recommended by vagrant ]
        > when ever running with virtualbox or VMware
        > it's recommended to use vagrant to track your local files on the VM
    * shell with superuser previllages
    * up to date system ( for securety )
- server
    * any server that serves WSGI with any method like
        * gunicorn [python]
        * apache [with wsgi extension package]
    > heroku like servers do that for you in production
- editor `recommended but not a must`
    * vsCode ( highly recommended )
    * customizations
        ```json
        {
            "editor.fontSize": 12,
            "editor.detectIndentation": false,
            "editor.wordWrap": "bounded",
            "editor.minimap.enabled": false,
            "editor.renderWhitespace": "none",
            "editor.wordWrapColumn": 79,
            "sqltools.useNodeRuntime": true,
            "python.linting.pylintArgs": [
                "--load-plugins pylint_flask_sqlalchemy"
            ],
            "terminal.integrated.cursorStyle": "line",
            "terminal.integrated.fontSize": 10
        }
        ```
    * extentions
        | ext                       | for           |
        |-------------------------- | ------------- |
        | `alexcvzz.vscode-sqlite`  | sqlite3       |
        | `hookyqr.beautify`        | beautify      |
        | `ldez.ignore-files`       | .gitignore    |
    
    > once you done your workspace should be like this
    >
    > ![vs_screen][1]


# install
### shell
- if you decided not to work on a VM or your device is not beering it
    you'll need shells
- this is a common thing for developers but if you are a windows user
    and not a developer you could get the [git shell here][2]
- it's working well on most systems but has some small issues,
however it's recommended to run on windows with CMD ( Command Prompt )

> whenever running a command in these documents, it's for ubuntu like systems
>
> unless other platform is mentioned

### Vagrant
**windows**: download and install latest version [here][3]

you could find also versions for various system in the same link,
but the best way to obtain a well interacting copy with your system is cli

run this command in the shell
```bash
sudo apt install vagrant
vagrant --version       # check installation & version
```
> vagrant recomends working with [VMware][4] `( it's up to you )`

### VM
[virtualbox][5]
```bash
# vagrant compatible version
sudo apt install virtualbox             # 6.0


# latest version
# Not compatible with vagrant
sudo add-apt-repository multiverse

echo "deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian `lsb_release -cs` contrib"|sudo tee /etc/apt/sources.list.d/virtualbox.list

wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -

wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -

sudo apt update
sudo apt-get install virtualbox-6.1     # 6.1


# additional
sudo dpkg-reconfigure virtualbox-dkms
sudo dpkg-reconfigure virtualbox
sudo modprobe vboxdrv
sudo modprobe vboxnetflt
sudo apt install virtualbox-ext-pack
```

## python
### python3 & pip3
```bash
sudo apt install python3 python3-pip
```
> this instalation should be proceeded inside the machene you use,
> either bein a VM or your disktop using terminal or using
> [windows excutable][11]

### [vertualenv][6] | [Gusthub][7]
```bash
# install
sudo pip3 install virtualenv

# create virtualenv
# venv /link/to/dir
virtualenv /venv


# work inside /venv
source venv/bin/activate

# get outside /venv
deactivate
```

### [pipenv][8] | [readthedocs][9] - [realpython][10]
```bash
# you could use ab activated virtualenv
# or run this to create/run a pipenv
pipenv shell

# suppose you run into /venv from the upove code
# use pipenv insteade of pip or pip3 ro install packages
#
# it's important to do so if you ara going to deploy on heroku
# note that you will need to set up your environment for your
# ` vscode workspace also if tou are using it
#
# sudo used as /venv is obtained by root
sudo pipenv install -r requirements.txt
```

### `PROJECT_APP/secrets`
By installing requirements on whatever environment you choosen,
you're <span style="color:red;">one</span> step to start your app

inside [`.extras/`][12] there are some schema files that you need to modify,
download or replace them within your project file to release some additional
functionalities like oAuth

as every file could be treated differebtly there are markdown ([EXTRAS.md][13])
files within docs folder to show you where to place every file

<span style="color:red;">For now: files except [`init.json`][14] are optional,
as this file contains schema for your superuser</span>

### Aplication

- when ever you set your environment, thin almost all done
- you now only need to start running your aplication or get into developing it
- so let's start.. oh.. it's time to know about [`start.sh`][15],
    this bash script will help you alot..
- it's very simple to use, just hit [`./start.sh`][16] and choose what you want to do
- feel your self


[1]: screens/vs_screen.png
[2]: https://git-scm.com/download
[3]: https://www.vagrantup.com/downloads.html
[4]: https://www.vagrantup.com/vmware/index.html
[5]: https://www.virtualbox.org/wiki/Downloads
[6]: https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b
[7]: https://docs.python.org/3/library/venv.html
[8]: https://pipenv.kennethreitz.org/en/latest/
[9]: https://pipenv-searchable.readthedocs.io/
[10]: https://realpython.com/pipenv-guide/
[11]: https://www.python.org/downloads/windows/
[12]: /.extras/
[13]: /EXTRAS.md
[14]: .extras/secrets/init.json
[15]: helpers.md
[16]: /start.sh
