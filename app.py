from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Matrix operations
def add_matrices(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def subtract_matrices(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def multiply_matrices(a, b):
    result = [[0] * len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            result[i][j] = sum(a[i][k] * b[k][j] for k in range(len(b)))
    return result

def transpose_matrix(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'rowa' not in session:
        session['rowa'] = 2
    if 'cola' not in session:
        session['cola'] = 2
    if 'rowb' not in session:
        session['rowb'] = 2
    if 'colb' not in session:
        session['colb'] = 2
    if 'matrix_a' not in session:
        session['matrix_a'] = [[0] * session['cola'] for _ in range(session['rowa'])]
    if 'matrix_b' not in session:
        session['matrix_b'] = [[0] * session['colb'] for _ in range(session['rowb'])]
    if 'result_matrix' not in session:
        session['result_matrix'] = []

    if request.method == 'POST':
        action = request.form.get('action')

        matrix_a = []
        for row in range(session['rowa']):
            row_data = []
            for col in range(session['cola']):
                cell_value = request.form.get(f'a_{row}_{col}', 0)
                row_data.append(float(cell_value))
            matrix_a.append(row_data)
        session['matrix_a'] = matrix_a

        matrix_b = []
        for row in range(session['rowb']):
            row_data = []
            for col in range(session['colb']):
                cell_value = request.form.get(f'b_{row}_{col}', 0)
                row_data.append(float(cell_value))
            matrix_b.append(row_data)
        session['matrix_b'] = matrix_b

        if action == 'add_row_a':
            if session['rowa'] < 5:
                session['rowa'] += 1
                session['matrix_a'].append([0] * session['cola'])
        elif action == 'remove_row_a' and session['rowa'] > 1:
            session['rowa'] -= 1
            session['matrix_a'].pop()
        elif action == 'add_column_a':
            session['cola'] += 1
            for row in session['matrix_a']:
                row.append(0)
        elif action == 'remove_column_a' and session['cola'] > 1:
            session['cola'] -= 1
            for row in session['matrix_a']:
                row.pop()

        elif action == 'add_row_b':
            if session['rowb'] < 5:
                session['rowb'] += 1
                session['matrix_b'].append([0] * session['colb'])
        elif action == 'remove_row_b' and session['rowb'] > 1:
            session['rowb'] -= 1
            session['matrix_b'].pop()
        elif action == 'add_column_b':
            session['colb'] += 1
            for row in session['matrix_b']:
                row.append(0)
        elif action == 'remove_column_b' and session['colb'] > 1:
            session['colb'] -= 1
            for row in session['matrix_b']:
                row.pop()

        session.modified = True
        return redirect(url_for('index'))

    return render_template(
        'index.html',
        rowa=session['rowa'], cola=session['cola'],
        rowb=session['rowb'], colb=session['colb'],
        matrix_a=session['matrix_a'],
        matrix_b=session['matrix_b'],
        result_matrix=session['result_matrix']
    )

# AJAX route for matrix operations
@app.route('/operation', methods=['POST'])
def matrix_operation():
    operation = request.json.get('operation')
    matrix_a = session['matrix_a']
    matrix_b = session['matrix_b']

    if operation == 'add':
        result = add_matrices(matrix_a, matrix_b)
    elif operation == 'subtract':
        result = subtract_matrices(matrix_a, matrix_b)
    elif operation == 'multiply':
        if len(matrix_a[0]) == len(matrix_b):
            result = multiply_matrices(matrix_a, matrix_b)
        else:
            return jsonify({'error': 'Matrix dimensions must match for multiplication.'})
    elif operation == 'transpose_a':
        result = transpose_matrix(matrix_a)
    elif operation == 'transpose_b':
        result = transpose_matrix(matrix_b)
    else:
        return jsonify({'error': 'Invalid operation.'})

    return jsonify({'result_matrix': result})

if __name__ == "__main__":
    app.run(debug=True)
