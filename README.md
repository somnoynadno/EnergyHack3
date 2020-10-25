# Хакатон "EnergyHack3"

## Подготовка скриптов и запуск

*Подразумевается установленный Python 3*

### Парсер формата .xsde

Скрипт автоматически проходится по XML-документу и строит топологию сети в виде хеш-таблицы (ключ -- RTID элемента, значение -- узел сети).

0. Подтягиваем зависимости ``` $ pip3 install -r requirements.txt ```

1. При необходимости указываем путь к файлу .xsde в переменной `FILE_PATH` файла `src/parser.py`

2. Запускаем парсер ``` $ python3 src/parser.py <RTID> ``` и строим топологию сети

#### Дополнительные функции

- `print_tree_recursively(node, i=1)`: построение дерева от выбранного узла

- `reverse_lookup(node)`: ищет и возвращает список родителей узла

- `print_full_topology(root)`: объединяет первые две и строит всю топологию от корневого элемента

### Миграция в neo4j

Вторая часть скрипта (`neo4j_connector.py`) проходится по топологии и создаёт узлы и связи между ними в графовой СУБД.

0. Подтягиваем зависимости ``` $ pip3 install -r requirements.txt ```

1. Поднимаем локально (или глобально) [neo4j](neo4j.com/) 

2. Указываем адрес, логин и пароль для СУБД в `src/neo4j_connector.py` (переменные `URI` и `CREDS`)

3. Запускаем скрипт ``` $ python3 src/neo4j_connector.py ``` и идём пить чай

## Алгоритмика САВС

См. файл `ALGO.md`

Язык запросов -- [Cypher](https://ru.bmstu.wiki/Cypher_Query_Language)

## Презентация решения

https://docs.google.com/presentation/d/1JB8ZitUgQQQC4Ozg5IDAKaKQv73zHHHEFrGqNS3tY-w/edit?usp=sharing

По всем вопросам: @somnoynadno.
