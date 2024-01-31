## Описание задания:
1. Написать сервис, который принимает запрос с указанием кадастрового номера, широты и долготы, эмулирует отправку
запроса на внешний сервер, который может обрабатывать запрос до 60 секунд. Затем должен отдавать результат запроса.
2. Считается, что внешний сервер может ответить `true` или `false`.
Данные запроса на сервер и ответ с внешнего сервера должны быть сохранены в БД. Нужно написать АПИ для получения
истории всех запросов/истории по кадастровому номеру.
3. Сервис должен содержать следующие эндпоинты:  
`/query` - для получения запроса  
`/result` - для отправки результата  
`/ping` - проверка, что  сервер запустился  
`/history` - для получения истории запросов
4. Добавить Админку.
5. Сервис завернуть в Dockerfile.
6. *В качестве дополнительного задания. Можно добавить дополнительный сервис, который будет принимать запросы первого сервиса и эмулировать внешний сервер.

### Будет плюсом!
- Документация к сервису
- Тесты функционала

### Отчет о тестировании
```
Found 6 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 0.266s

OK
Destroying test database for alias 'default'...
```
PS: тесты запускать при работающем приложении во втором терминале,
т.к. нужен работающий эмулятор удаленного сервера.

### Образ Docker с приложением
https://hub.docker.com/repository/docker/dmitriishilkin/antipoff/general
