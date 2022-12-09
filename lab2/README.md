**Описание работы**

Сборка образа и его запуск

```
docker build -t mtu_finder -f Dockerfile .
docker run --rm -p 80:80 -it mtu_finder
```

Запускаем скрипт

```
python3 finder.py название_хоста
```