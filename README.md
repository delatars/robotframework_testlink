# Robotframework-testlink listener
Robotframework Listener для загрузки результатов тестирования в Testlink.

- Выгружает тесты из *.robot файла только с суффиксом 'T' (X-EXAMPLE-T1, X-EXAMPLE-T2)

### Installation
```bash
pip install git+https://github.com/delatars/robotframework_testlink.git
```
### Usage:

listener модуль: robotframework_testlink_listener

```bash
robot --listener robotframework_testlink_listener \
 -v RT_SERVER:http://testlink.drw/lib/api/xmlrpc/v1/xmlrpc.php \
 -v RT_APIKEY:3d7ad60da3814a61c927889384c0ae79 \
 -v RT_PROJECT:test \
 -v RT_TESTPLAN:robot \
 -v RT_BUILD:4 \
 -v RT_PLATFORM:centos7 \
 robot_testlink.robot
```
Список аргументов для cli:

обязательные:
- RT_SERVER - адрес api тестлинка
- RT_API_KEY - api ключ тестлинка
- RT_PROJECT - имя проекта
- RT_TESTPLAN - имя тестплана
- RT_BUILD - версия сборки
- RT_PLATFORM - платформа

необязательные:
- RT_EXEC_DURATION - время выполнения
- RT_STEPS - шаги
- RT_USER - пользователь
- RT_NOTES - заметки
