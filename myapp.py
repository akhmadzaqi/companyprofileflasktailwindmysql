from flask import Flask, render_template, redirect, url_for
import mysql.connector
import base64


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'webcourseiseng'
app.config['MYSQL_PORT'] = 3300

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    port=app.config['MYSQL_PORT']
)

def truncate_description(description, length):
    # Split the description into words
    words = description.split()

    # Join the words up to the specified length
    truncated_description = ' '.join(words[:length])

    # Add ellipsis (...) if the description was truncated
    if len(words) > length:
        truncated_description += '...'

    return truncated_description

@app.route('/kontak')
def kontak():
    # Ganti email berikut dengan email Anda
    email_tujuan = 'kidznet082@gmail.com'
    subject = 'Subject email Anda'
    body = 'Isi pesan email Anda'

    # Menggunakan format mailto untuk membuat URL email
    email_link = f'mailto:{email_tujuan}?subject={subject}&body={body}'

    # Redirect ke URL email
    return redirect(email_link)

@app.route('/')
def index():
    with mysql.cursor() as cur:
        cur.execute("SELECT * FROM course")
        data = cur.fetchall()

        data_with_image = []

        for row in data:
            # Assuming the blob column is the fifth column, change it accordingly
            image_data = row[4] if len(row) > 4 else None

            if image_data is not None:
                # Convert BLOB data to a data URI
                image_url = 'data:image/png;base64,' + base64.b64encode(image_data).decode('utf-8')
            else:
                # Set a default value or provide an error message
                image_url = 'data:image/png;base64,'

            # Create a dictionary with the fields and the image URL
            row_with_image = {'id': row[0], 'field1': row[1], 'field2': row[2], 'field3': row[3], 'image_url': image_url}

            # Append the dictionary to the list
            data_with_image.append(row_with_image)

        return render_template('index.html', data=data_with_image)
    
@app.route('/blog')
def blog():
    with mysql.cursor() as cur:
        cur.execute("SELECT * FROM posts")
        data = cur.fetchall()

        data_with_image = []

        for row in data:
            # Assuming the blob column is the fifth column, change it accordingly
            image_data = row[4] if len(row) > 4 else None

            if image_data is not None:
                # Convert BLOB data to a data URI
                image_url = 'data:image/png;base64,' + base64.b64encode(image_data).decode('utf-8')
            else:
                # Set a default value or provide an error message
                image_url = 'data:image/png;base64,'

            # Create a dictionary with the fields and the image URL
            row_with_image = {'id': row[0], 'field1': row[1], 'field2': row[2], 'field3': row[3], 'image_url': image_url}

            # Append the dictionary to the list
            data_with_image.append(row_with_image)

        return render_template('blog.html', data=data_with_image, truncate_description=truncate_description)
    
@app.route('/blogdetail/<id>', methods=['GET'])
def blogdetail(id):
    print(f"Received ID: {id}")
    with mysql.cursor() as cur:
        cur.execute("SELECT posts.post_id, posts.title, posts.content, posts.tag, posts.blog_image, authors.author_name, posts.created_at FROM posts JOIN authors ON posts.author_id = authors.author_id WHERE posts.post_id = %s", (id,))
        data = cur.fetchone()
        image_data = data[4]
        if image_data is not None:
            # Mengubah data BLOB menjadi URL data (data URI)
            image_url = base64.b64encode(image_data).decode('utf-8')
        else:
            # Atur nilai default atau berikan pesan kesalahan
            image_url = 'data:image/png;base64,'
        data_with_image = {'id': data[0], 'field1': data[1], 'field2': data[2], 'field3': data[3], 'image_url': 'data:image/png;base64,' + image_url, 'author_name': data[5], 'field6': data[6],}

        
    return render_template('blogdetail.html', data=data_with_image)

@app.route('/aboutus')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)