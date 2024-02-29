from flask import Flask, render_template, request, redirect, url_for, flash
from math import sqrt

app = Flask(__name__)
app.secret_key = '109-862-759'
solutions_history = []\

@app.route('/home')
def homew():
    return render_template('home.html')
@app.route('/about_as')
def about_as():
    return render_template('about_as.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'adminchik':
            return redirect(url_for('homew'))
        else:
            flash('Неправильный логин или пароль!')
    return render_template('login.html')

@app.route('/history')
def history():
    return render_template('history.html', history=solutions_history)

@app.route('/calc', methods=['GET', 'POST'])
def home():
    result = None
    solution = None

    if request.method == 'POST':
        if 'a' in request.form:
            a = float(request.form.get('a'))
            b = float(request.form.get('b'))
            c = float(request.form.get('c'))
            D = b * b - 4 * a * c

            if D >= 0:
                x1 = (-b + sqrt(D)) / (2 * a)
                x2 = (-b - sqrt(D)) / (2 * a)
                result = (
                    f"a= {a}<br>"
                    f"b= {b}<br>"
                    f"c= {c}<br>"
                    f"D=b²-4*a*c= {D}<br>"
                    f"X1=(-b+√D):(2*a)= {x1}<br>"
                    f"X2=(-b-√D):(2*a)= {x2}<br>"
                    f"D= {b} * {b} -4* {a} * {c} = {D}<br>"
                    f"X1=(-{b} +√ {D} ):(2* {a} )= {x1}<br>"
                    f"X2=(-{b} -√ {D} ):(2* {a} )= {x2}"
                )
                solutions_history.append({'equation': f'Квадратное уравнение: {a}x² + {b}x + {c} = 0', 'result': result})

            else:
                result = f"Дискриминант равен: {D}. Решений нет."
                solutions_history.append({'equation': f'Квадратное уравнение: {a}x² + {b}x + {c} = 0', 'result': result})
        else:
            a1 = float(request.form.get('a1'))
            b1 = float(request.form.get('b1'))
            c1 = float(request.form.get('c1'))
            a2 = float(request.form.get('a2'))
            b2 = float(request.form.get('b2'))
            c2 = float(request.form.get('c2'))
            solution = solve_linear_system(a1, b1, c1, a2, b2, c2)
            solutions_history.append({'equation': f'Система уравнений: {a1}x + {b1}y = {c1} и {a2}x + {b2}y = {c2}', 'solution': solution})

    return render_template('calc.html', result=result, solution=solution)


def solve_linear_system(a1, b1, c1, a2, b2, c2):
    if a1 / b1 != a2 / b2:
        m = a1 / a2 if a2 != 0 else 0
        n = b1 / b2 if b2 != 0 else 0
        if m != 0:
            k = a1 / a2
            b2_new = b2 * k - b1
            c2_new = c2 * k - c1
            y = c2_new / b2_new
            x = (c1 - b1 * y) / a1
            return (x, y)
        elif n != 0:
            k = b1 / b2
            a2_new = a2 * k - a1
            c2_new = c2 * k - c1
            x = c2_new / a2_new
            y = (c1 - a1 * x) / b1
            return (x, y)
        else:
            return None
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)