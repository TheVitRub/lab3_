from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'static/uploads'


# Главная страница - название миссии
@app.route('/')
def mission_name():
    return render_template('mission_name.html')


# Страница с девизом миссии
@app.route('/index')
def mission_slogan():
    return render_template('mission_slogan.html')


# Страница с рекламой
@app.route('/promotion')
def promotion():
    return render_template('promotion.html')


# Страница с изображением Марса
@app.route('/image_mars')
def image_mars():
    return render_template('image_mars.html')


# Страница для выбора астронавтов
@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    if request.method == 'POST':
        # Получение данных из формы
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        email = request.form['email']
        education = request.form['education']
        profession = request.form['profession']
        gender = request.form['gender']
        motivation = request.form['motivation']
        stay_on_mars = request.form['stay_on_mars']

        nickname = f"{first_name} {last_name}"

        return redirect(url_for('results', nickname=nickname, level=1, rating=0.0))
    return render_template('astronaut_selection.html')


# Страница с результатом отбора астронавта
@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return render_template('results.html', nickname=nickname, level=level, rating=rating)


@app.route('/photo/<nickname>', methods=['GET', 'POST'])
def photo_upload(nickname):
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('photo_upload.html', nickname=nickname, filename=filename)
    return render_template('photo_upload.html', nickname=nickname, filename=None)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Страница с каруселью галереи марсианских ландшафтов
@app.route('/carousel')
def carousel():
    return render_template('carousel.html')


app.secret_key = 'super_secret_key'

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
