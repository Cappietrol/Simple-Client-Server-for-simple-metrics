# Простой клиент-сервер для простых метрик
## Краткое описание
Существует две команды:
- Put для сохранения метрик на сервере. 
- Get для получения метрик
### Сервер
На стороне сервера принимается соединение от клиента. 
После ожидается одна из двух команд
- put
  >**Формат команды put для отправки метрик** <br>
    строка видf put (metric_name) (metric_value) (timestamp)\n <br>
    При принятии корректной команды сервер записывает данные метрики в локальную переменую класса.
    
- get
  >**Формат команды put для получения метрик** <br>
    get (metric_name)\n <br>
    где вместо названия метрики(metric_name) может быть '*', что обозначначает отправка клиенту все данные, всех метрик находящиеся на данный момент на сервере <br>
    При принятии корректной команыд сервер отправляет данные метрики(метрик) в зависимости от metric_name.

### Клиент
Клиент подключившись к серверу передает ему команду ожидая ответа.
При отправке корректной команды:
- put
  >**Ожидаемый ответ** <br>
    ok\n\n <br>
    Что обозначает что сервер принял и корректно обработал переданную метрику <br>
    **Возможный ответ**<br>
    Ошибка сервера: error\nwrong command\n\n 
    
- get
  >**Ожидаемый ответ** <br>
    В случае успешного ответа сервера ok\metric.info 10.5 1501864247\metric.cpu 15.3 1501864259\n\n <br>
    в случае отсутсвие метрики с таким названием (или отуствия их вообще) ok\n\n <br>
    Ошибка сервера: error\nwrong command\n\n <br>

## Используемая версия языка
###Версия языка
Скрипт требует для своей работы установленного интерпретатора Python версии 3.6 и выше

  
## Как Использовать
Примеры использования
### Клиент
```python
  client = Client('127.0.0.1', 8888, timeout=5)
  client1.put("test_value_1", 2.67, 1195371362)
  result = client1.get("test_value_1")
```
### Сервер
 ```python
  run_server('127.0.0.1', 8888)
 ```
