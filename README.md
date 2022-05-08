# flask_textboard_app

Hello!

## Quick Start

When using app.py
```
$ python
>> from app import db
>> db.create_all()
```

rest_app.py
```
$ python
>> from rest_app import db
>> db.create_all()
```

After created DB...
```
$ python app.py
or
$ python rest_app.py
```

If you check http://127.0.0.1:5000 abd the page is deiplayed, it's OK.


## How to use

## app.py

### POST method

#### Create a thread

You can change the parameters of the "thread_title".

This request will not work if the thread already exists.

The following is an example when the thread_title is "test".

```
curl -X POST "http://127.0.0.1:5000/api?thread_title=test"
```

#### Write article to specify thread

You can change the parameters of the "thread_id", "name", "article".
This request will not work without the specified thread_id.

The following is an example when the "thread_id"=1, "name" is "rasuk", "article" is hello.

```
curl -X POST "http://127.0.0.1:5000/api?thread_id=1&name=rasuk&article=hello"
```

### GET method
#### Get a list of threads on the bulletin board
You can get these parameters such as "post date", "id", "thread_name".

```
$ curl http://127.0.0.1:5000/api/get_info
```

return to Json

```
[
  {
    "date": "Sun, 08 May 2022 14:08:56 GMT", 
    "id": 1, 
    "thread_name": "test"
  }
]
```

#### Get a list of posts in the specified thread_id
You can get these parameters such as "article_id", "article", "date", "name", "thread_id"
The following is an example when the "thread_id" = 1

```
$ curl "http://127.0.0.1:5000/api?thread_id=1"
```

return to Json

```
{
  "1": [
    {
      "article": "hello", 
      "date": "Sun, 08 May 2022 15:24:01 GMT", 
      "name": "rasuk", 
      "thread_id": 1
    }
  ]
}
```

## rest_app.py

### POST method

#### Create a thread

You can change the parameters of the "thread_title".

This request will not work if the thread already exists.

The following is an example when the thread_title is "test".

```
curl -X POST "http://127.0.0.1:5000/api/thread_title/test"
```

#### Write article to specify thread

You can change the parameters of the "thread_id", "name", "article".
This request will not work without the specified thread_id.

The following is an example when the "thread_id"=1, "name" is "rasuk", "article" is hello.

```
curl -X POST "http://127.0.0.1:5000/api/post_article/1?name=rasuk&article=hello"
```

### GET method
#### Get a list of threads on the bulletin board
You can get these parameters such as "post date", "id", "thread_name".

```
$ curl http://127.0.0.1:5000/api/get_thread
```

return to Json

```
[
  {
    "date": "Sun, 08 May 2022 14:08:56 GMT", 
    "id": 1,  
    "thread_name": "test"
  }
]
```

#### Get a list of posts in the specified thread_id
You can get these parameters such as "article_id", "article", "date", "name", "thread_id"
The following is an example when the "thread_id" = 1

```
$ curl "http://127.0.0.1:5000/api/1"
```

return to Json

```
{
  "1": [
    {
      "article": "hello", 
      "date": "Sun, 08 May 2022 15:24:01 GMT", 
      "name": "rasuk", 
      "thread_id": 1
    }
  ]
}
