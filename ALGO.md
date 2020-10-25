# Алгоритмы САВС

В данном файле приведены некоторые алгоритмы, реализующие функционал
системы автоматического восстановления (САВС) электроснабжения
потребителей в распределительной (6-10кВ) сети.

Все запросы используют СУБД neo4j и язык запросов Cypher.

Возможно, будет дополнятся более сложными алгоритмами.

## Выбор подсети элемента по RTID

```
MATCH p = (:BusBarSection {RTID: 266})-[r*0..]->(x)
RETURN x
```

## Валидация топологии сети

```
MATCH (n {RTID:30})
MATCH p=(n)-[:CONNECTED_TO*1..5]->(n)
UNWIND TAIL(NODES(p)) AS m WITH p 
RETURN p
```

## Поиск специфичных элементов (BFS)

```
MATCH (n {RTID:266})
WITH id(n) AS startNode
CALL gds.alpha.bfs.stream("graph", {startNode: startNode})
YIELD path
RETURN path
```

## Алгоритм Дейкстры для мощностей потребителей

```
MATCH (start {RTID: 1596}), (end {RTID: 1460})
CALL gds.alpha.shortestPath.stream({
  nodeProjection: '*',
  relationshipProjection: "*",
  startNode: start,
  endNode: end,
  writeProperty: 'capacity'
})
YIELD nodeId, cost
RETURN gds.util.asNode(nodeId).name AS name, cost
```

## Изменение состояния элемента сети по RTID

```
MATCH (n {RTID: 1543})
SET n.closed = 0 
RETURN n
```

