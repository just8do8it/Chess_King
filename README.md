## ![Chess King](https://raw.githubusercontent.com/just8do8it/Chess_King/master/templates/images/chessKingLogo.png)

[Документация](https://github.com/just8do8it/TUES/blob/master/Documentation/Chess%20Website%20Documentation.docx) || Разработено от **Благовест Атанасов** [just8do8it](https://github.com/just8do8it)

### Описание на проекта: 
Сайт за игра на шах, в който се регистрират потребители и може да се играе в два режима - обикновен мултиплеър, или турнир, съставен от 8 играчи, като по време на играта потребителите могат да комуникират помежду си в чат. Пази се история на изиграните досега игри, като всеки играч може да прегледа своите предишни игри ход по ход в профилната си страница, като там се изписва и неговия коефициент на победи.

### Инструкции за сваляне на проекта: 
Когато се намирате в началото на страницата (скролнете нагоре), горе вдясно се намира зелен бутон с надпис "Code". Щом го натиснете изберете опцията "Download ZIP", като след свалянето разархивирайте файла.

### Използвани технологии:

1. [Python](https://www.python.org/) - популярен и прогресивен език за програмиране
2. [Flask](https://flask.palletsprojects.com/en/1.1.x/) - библиотека за изграждане на WEB приложения (за Python)
3. [SQLite](https://www.sqlite.org/index.html) - лека и функционална система за управление на база данни (СУБД) 
4. [SQLAlchemy](https://www.sqlalchemy.org/) - функционален инструмент за работа с база данни (за Python)
5. HTML+CSS - задължителни технологии за базовата структура на всеки сайт 
6. JavaScript (+ jQuery) - език за програмиране, позволяващ дизайна на динамични WEB страници, както и сървърна комуникация в рамките на WEB приложение

## Подготовка и стартиране на проекта

Това ръководство е ориентирано главно към потребителите на някаква форма на Linux операционна система (Ubuntu-базирана)

1. Инсталиране на нужните програми. Отворете терминален прозорец и пуснете:

```bash
sudo apt update && sudo apt install software-properties-common && sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt install python3.9 && pip install pip Flask Flask-Login Flask-Session Flask-API SQLAlchemy Flask-SQLAlchemy Werkzeug
```

2. Трябва да създадете две „env“ променливи във файла “.bashrc”.
Първо отваряте файла през терминала, например с командата:
```bash
$ nano ~/.bashrc
```

3. След това отивате на най-долния ред на файла и създавате две променливи – `CHESS_DATABASE` и `PYTHON_GAME`, като те ще съдържат пътищата до съответните файлови ресурси. Последната папка “TUES” в примерните пътища е папката на Github репозиторито. Пътищата могат да варират в зависимост от ситемата Ви, така че показания по-долу пример е само образец.
```
export CHESS_DATABASE='sqlite:///C:\\TUES\\Github\\TUES\\chess.db'
export PYTHON_GAME='/mnt/c/TUES/Github/TUES/python_game'
```                                                                                                              

4. След това запишете файла с командите Ctrl+X, Y, Enter.
За да се сигурни, че променливите са запазени трайно в системата изпълнете следната команда в терминала:
```bash
$ source ~/.bashrc
```
5. Вече сте готови да стартирате приложението. Влезте в папката, където са изходните ресурси и изпълнете командата:
```bash
$ export FLASK_APP=main.py
```
6. Сега можете да стартирате приложението (всеки път) с командата:
```bash
$ flask run
```

Ако искате да терминирате приложението, използвайте `Ctrl+C.`

Щом пуснете приложението, заредете адреса на `localhost:5000` в браузъра си (в случая порта е `5000`, но това може да варира) и ще се озовете на началната страница. Потребителския интерфейс е достатъчно опростен, за да може всеки да се ориентира в която и да е негова част и да тества функционалността на продукта.
