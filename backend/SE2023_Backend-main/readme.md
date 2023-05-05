<h1 align="center">SE2022 Backend</h1>
<div align="center">

  [![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
)](https://www.djangoproject.com/)     [![](https://img.shields.io/badge/License-MIT-9cf?style=for-the-badge)](./LICENSE)</div>

## Description

This is the backend code of the `PaperDaily` project based on [`django2.2`](https://docs.djangoproject.com/en/2.2/).

## Quick Start

1. Install `python3.7` or later（python3.8也行）

2. Copy [`model.pt`](https://drive.google.com/file/d/1iORaaGlxte-r2JrN650ccDe-VEivYBnA/view?usp=sharing) to the root directory

3. Set up the database in `backend/settings.py`

4. Install dependencies

```
$ pip install -r requirements.txt
```

5. Run server 

```
$ python manage.py runserver 0:8000
```

### Error


<details><summary>if error</summary>

```
File "/home/admin/.local/lib/python3.7/site-packages/django/db/backends/mysql/operations.py", line 146, in last_executed_query
    query = query.decode(errors='replace')
AttributeError: 'str' object has no attribute 'decode'
```
则注释掉该文件的`145-146`行
```
145         # if query is not None:
146         # query = query.decode(errors='replace')
147         return query
```

</details>

## Server

[`http://122.9.14.73:8000/`](http://122.9.14.73:8000/)

## Account

目前设置已有的管理员账户为：

```
'USER': admin
'PASSWORD': se-mcdb-o2e
```

也可以自行创建管理员账户：

```
python manage.py createsuperuser
```

## License

[MIT](./LICENSE)



