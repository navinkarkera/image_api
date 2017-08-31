# Image Management API

Image management REST API

## Getting Started

clone this project using
```
git clone https://github.com/navinkarkera/image_api.git
```

### Installing

```
cd image_api/
pip install -r requirements.txt
python manage.py migrate
```

And run the server using

```
python manage.py runserver
```

### Example Demo

Install httpie for testing the endpoints

```
pip install httpie
```

Since the code is deployed in http://navinkarkera.pythonanywhere.com, we can test it.
Use httpie to register a user
```
http POST http://navinkarkera.pythonanywhere.com/register/ username=demo password=demouser
```
OUTPUT:
```
HTTP/1.1 201 Created
Allow: POST, OPTIONS
Connection: keep-alive
Content-Length: 52
Content-Type: application/json
Date: Thu, 31 Aug 2017 17:29:15 GMT
Server: openresty/1.9.15.1
Vary: Accept
X-Clacks-Overhead: GNU Terry Pratchett
X-Frame-Options: SAMEORIGIN

{
    "token": "d19eb4eb2688c8ece155a0d7cbc53de6f9b72255"
}
```

Use this token to access all endpoints of this API.

Now POST an image.
```
http --form navinkarkera.pythonanywhere.com/images/ "Authorization:Token d19eb4eb2688c8ece155a0d7cbc53de6f9b72255" image@naruto.jpg
```
OUTPUT:
```
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Connection: keep-alive
Content-Length: 91
Content-Type: application/json
Date: Thu, 31 Aug 2017 17:31:05 GMT
Server: openresty/1.9.15.1
Vary: Accept
X-Clacks-Overhead: GNU Terry Pratchett
X-Frame-Options: SAMEORIGIN

{
    "id": 1, 
    "image": null, 
    "url": "http://navinkarkera.pythonanywhere.com/media/2/1%7Cnaruto.jpg"
}
```

Get all images related to this token.
```
http GET navinkarkera.pythonanywhere.com/images/ "Authorization:Token d19eb4eb2688c8ece155a0d7cbc53de6f9b72255"
```
OUTPUT:
```
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Connection: keep-alive
Content-Length: 80
Content-Type: application/json
Date: Thu, 31 Aug 2017 17:32:42 GMT
Server: openresty/1.9.15.1
Vary: Accept
X-Clacks-Overhead: GNU Terry Pratchett
X-Frame-Options: SAMEORIGIN

[
    {
        "id": 1, 
        "url": "http://navinkarkera.pythonanywhere.com/media/2/1%7Cnaruto.jpg"
    }
]
```

To get a single image use:
```
http GET navinkarkera.pythonanywhere.com/images/1/ "Authorization:Token d19eb4eb2688c8ece155a0d7cbc53de6f9b72255"
HTTP/1.1 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Connection: keep-alive
Content-Length: 80
Content-Type: application/json
Date: Thu, 31 Aug 2017 17:33:56 GMT
Server: openresty/1.9.15.1
Vary: Accept
X-Clacks-Overhead: GNU Terry Pratchett
X-Frame-Options: SAMEORIGIN

{
    "id": "1", 
    "url": "http://navinkarkera.pythonanywhere.com/media/2/1%7Cnaruto.jpg"
}
```

To UPDATE an image use PUT:
```
http --form PUT navinkarkera.pythonanywhere.com/images/1/ "Authorization:Token d19eb4eb2688c8ece155a0d7cbc53de6f9b72255" image@Gintama.jpg
HTTP/1.1 201 Created
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Connection: keep-alive
Content-Length: 92
Content-Type: application/json
Date: Thu, 31 Aug 2017 17:35:01 GMT
Server: openresty/1.9.15.1
Vary: Accept
X-Clacks-Overhead: GNU Terry Pratchett
X-Frame-Options: SAMEORIGIN

{
    "id": 1, 
    "image": null, 
    "url": "http://navinkarkera.pythonanywhere.com/media/2/1%7CGintama.jpg"
}
```

To DELETE an image:

```
http DELETE navinkarkera.pythonanywhere.com/images/1/ "Authorization:Token d19eb4eb2688c8ece155a0d7cbc53de6f9b72255"
HTTP/1.1 204 No Content
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Connection: keep-alive
Content-Length: 0
Date: Thu, 31 Aug 2017 17:35:52 GMT
Server: openresty/1.9.15.1
Vary: Accept
X-Clacks-Overhead: GNU Terry Pratchett
X-Frame-Options: SAMEORIGIN
```

To regenerate the token use following.

```
http GET navinkarkera.pythonanywhere.com/regenerateToken/ "Authorization:Token d19eb4eb2688c8ece155a0d7cbc53de6f9b72255"
HTTP/1.1 200 OK
Allow: OPTIONS, GET
Connection: keep-alive
Content-Length: 52
Content-Type: application/json
Date: Thu, 31 Aug 2017 17:46:06 GMT
Server: openresty/1.9.15.1
Vary: Accept
X-Clacks-Overhead: GNU Terry Pratchett
X-Frame-Options: SAMEORIGIN

{
    "token": "aae5ca2acd29a2b60c6ae8d6c92541256ede6332"
}
```

To retrieve token from username and password.
```
http POST http://navinkarkera.pythonanywhere.com/api-token-auth/ username=demo password=demouser
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Connection: keep-alive
Content-Length: 52
Content-Type: application/json
Date: Thu, 31 Aug 2017 17:47:03 GMT
Server: openresty/1.9.15.1
X-Clacks-Overhead: GNU Terry Pratchett
X-Frame-Options: SAMEORIGIN

{
    "token": "aae5ca2acd29a2b60c6ae8d6c92541256ede6332"
}
```
