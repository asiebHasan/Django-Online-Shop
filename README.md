# Django-Online-Shop

Django project that consists of a fully featured online shop

celery and flower commands:

eventlet is required for celery to work:

```bash
pip install eventlet
```

celery:

```bash
    celery -A myshop worker --loglevel=info -P eventlet
    celery -A myshop worker -l info
```

flower:

```bash
    celery -A myshop flower
```
