Това ръководство е ориентирано главно към потребителите на някаква форма на Linux операционна система (Ubuntu-базирана)

Отворете програмата терминал. За да инсталирате нужните програми, пакети и модули използвайте командите по-долу:


Python:

$ sudo apt update

$ sudo apt install software-properties-common

$ sudo add-apt-repository ppa:deadsnakes/ppa

$ sudo apt install python3.9


Pip:

$ pip install pip


Flask:

$ pip install Flask

$ pip install Flask-Login

$ pip install Flask-Session

$ pip install Flask-API


SqlAlchemy

$ pip install SQLAlchemy

$ pip install Flask-SQLAlchemy


Werkzeug

$ pip install Werkzeug


Трябва да създадете две „env“ променливи във файла “.bashrc”.
Първо отваряте файла през терминала, например с командата:

 $ nano ~/.bashrc

След това отивате на най-долния ред на файла и създавате две променливи – „CHESS_DATABASE“ и „PYTHON_GAME“, като те ще съдържат пътищата до съответните файлови ресурси. Последната папка “TUES” в примерните пътища е папката на Github репозиторито. Пътищата могат да варират в зависимост от ситемата Ви, така че показания по-долу пример е само образец.

export CHESS_DATABASE='sqlite:///C:\\TUES\\Github\\TUES\\chess.db'

export PYTHON_GAME='/mnt/c/TUES/Github/TUES/python_game'
                                                                                                                 

След това запишете файла с командите Ctrl+X, Y, Enter.
За да се сигурни, че променливите са запазени трайно в системата изпълнете следната команда в терминала:

$ source ~/.bashrc

Вече сте готови да стартирате приложението. Влезте в папката, където са изходните ресурси и изпълнете командата:

$ export FLASK_APP=app.py

Сега можете да стартирате приложението (всеки път) с командата:

$ flask run

Ако искате да терминирате приложението, използвайте Ctrl+C.
