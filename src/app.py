from flask import Flask, jsonify, request, Response
import json
app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 123124123123
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 65489756464
    },
    {
        'name': 'Ozz',
        'price': 5.99,
        'isbn': 41515151
    }
]

def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

@app.route('/books')
def get_books():
    return jsonify({'books': books})

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value) 

@app.route('/books', methods=['POST'])
def add_books():
    request_data = request.get_json()
    if validBookObject(request_data):
        new_book = {
            "name": request_data["name"],
            "price": request_data["price"],
            "isbn": request_data["isbn"]
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 123124123123}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }

    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response
    # return jsonify(new_book)

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    update_book = {}
    if "name" in request_data:
        update_book["name"] = request_data["name"]
    if "price" in request_data:
        update_book["price"] = request_data["price"]
    for book in books:
        if book["isbn"] == isbn:
            book.update(update_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

app.run(port=5000)