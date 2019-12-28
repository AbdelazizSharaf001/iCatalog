#!/usr/bin/env bash
# this is a helper script to facilitate working with the project.
# some parts will be in need to modify in case you changed any of
# - dir names [i_catalog, secrets, ...]
# - 

while true; do
    sleep 1
    tput setaf 2
    clear
    echo 'Select process number or any other thing to exit: '
    opts=("clear" "run" "requirements" "test" "autopep8" "push" "deploy")
    select ch in "${opts[@]}"; do
    echo '-------------------'
    case $ch in
        # clear	-----------------------------
        "clear") break;;

        # run	-------------------------------------
        "run")
            read -p "Type c to custumize your app runner (otherwise run defaults): " yn
            case $yn in
                [Cc]*)
                    read -p "Enter your project directory 'FLASK_APP' [i_catalog]: " pdir
                    pdir=${pdir:-i_catalog}

                    read -p "HOST [0.0.0.0]: " ph
                    ph=${ph:-0.0.0.0}

                    read -p "PORT [5000]: " pp
                    pp=${pp:-5000}
                    ;;
                *)
                    pdir='i_catalog'
                    ph='0.0.0.0'
                    pp='5000'
                    ;;

            esac

            read -p "https check (y|n): " yn
            case $yn in
                [Yy]*)
                    opts1=("ssl_cert" "adhoc")
                    select ch1 in "${opts1[@]}"; do
                    case $ch1 in
                        "ssl_cert")
                            ssl="--cert $pdir/secrets/iCatalog.crt \
                            --key $pdir/secrets/iCatalog.key"
                            break
                            ;;

                        "adhoc")
                            export FLASK_RUN_CERT=adhoc
                            break
                            ;;

                        *)
                            ssl=""
                            break
                            ;;
                    esac
                    done
                    ;;
                *) ;;
            esac

            opts1=("production" "deveopment" "testing" "wsgi")
            select ch1 in "${opts1[@]}"; do
            case $ch1 in
                "production")
                    export FLASK_APP=$pdir
                    export FLASK_ENV=production
                    break
                    ;;

                "deveopment")
                    export FLASK_APP="$pdir:create_app('dev')"
                    export FLASK_ENV=development
                    break
                    ;;

                "testing")
                    export FLASK_APP="$pdir:create_app('test')"
                    export FLASK_ENV=testing
                    break
                    ;;

                "wsgi")
                    gunicorn -b 0.0.0.0:5000 wsgi:app
                    break 2
                    ;;

                *) break 2;;
            esac
            done

            flask run -h $ph -p $pp $ssl
            # break
            ;;

        # requirements	-----------------------------
        "requirements")
            read -p "install requirements.txt (pip) (y|n): " yn
            case $yn in
                [Yy]*)
                    opts1=("pipenv" "pip3" "pip")
                    select ch1 in "${opts1[@]}"; do
                    case $ch1 in
                        "pipenv")
                            e='env'
                            break
                            ;;

                        "pip3")
                            e='3'
                            break
                            ;;

                        "pip")
                            e=''
                            break
                            ;;

                        *) break;;
                    esac
                    done
                    sudo pip$e install -r requirements.txt
                    ;;
                    
                *) ;;
            esac

            read -p "ssl (self signed certificate) (y|n): " yn
            case $yn in
                [Yy]*)
                    s="i_catalog/secrets"
                    read -p " -nodes (y|n): " yn
                    case $yn in
                    [Yy]*)
                        openssl req -x509 -newkey rsa:4096 \
                            -keyout $s/iCatalog.key \
                            -out $s/iCatalog.crt \
                            -days 365 -subj '/CN=iCatalog';;

                    *)
                        openssl req -x509 -newkey rsa:4096 \
                            -keyout $s/iCatalog.key \
                            -out $s/iCatalog.crt \
                            -days 365 -subj '/CN=iCatalog' -nodes;;

                    *) break;;
                    esac
                    openssl verify $s/iCatalog.crt
                    ;;

                *) ;;
            esac
            # break
            ;;

        # test	-----------------------------
        "test")
            opts1=("pycodestyle" "pep8")
            select ch1 in "${opts1[@]}"; do
            tput setaf 3
            case $ch1 in
                "pycodestyle")
                    pycodestyle .
                    break
                    ;;

                "pep8")
                    pep8 .
                    break
                    ;;

                *) break 2;;
            esac
            done
            tput setaf 2
            echo 'Done.'
            ;;

        # tree	-----------------------------
        "autopep8")
            du -a $directory |awk '{print $2}' |grep '\.py$' \
            |xargs -n1 autopep8 --in-place --aggressive --aggressive
            echo 'Done'
            ;;

        # push	-----------------------------
        "push")
            git add .
            read -p "commit [New_push]: " com
            com=${com:-New_push}
            git commit -m "$com"
            git push -u origin master:master
            ;;

        # push	-----------------------------
        "deploy")
            opts1=("heroku" "git")
            select ch1 in "${opts1[@]}"; do
            case $ch1 in
                "heroku")
                    git add .
                    read -p "commit [New_deploy]: " com
                    com=${com:-New_deploy}
                    git commit -m "$com"
                    git push heroku master
                    break
                    ;;

                "git")
                    git add .
                    read -p "commit [New_deploy]: " com
                    com=${com:-New_deploy}
                    git commit -m "$com"
                    read -p "branch [heroku]: " branch
                    branch=${branch:-heroku}
                    git push -u origin master:heroku
                    break
                    ;;

                *) echo 'Choose one of the deploy methods listed..';;
            esac
            done
            ;;

        *)
            rm -r __pycache__
            rm -r i_catalog/__pycache__
            tput sgr0
            clear
            exit;;
    esac
    echo '-------------------'
    done
done
