from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/determinant', methods=['POST'])
def determinant():
    try:
        matrix = np.array(request.json['matrix'])
        det = round(np.linalg.det(matrix), 2)
        return jsonify({'determinant': det})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/update_matrix', methods=['POST'])
def update_matrix():
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    return jsonify(matrix)

@app.route('/transpose', methods=['POST'])
def transpose():
    matrix = request.json['matrix']
    transposed = [list(row) for row in zip(*matrix)]
    return jsonify(transposed)

@app.route('/check_symmetry', methods=['POST'])
def check_symmetry():
    matrix = request.json['matrix']
    transposed = [list(row) for row in zip(*matrix)]

    is_symmetric = matrix == transposed
    is_anti_symmetric = matrix == [[-cell for cell in row] for row in transposed]

    result = "Simetrična" if is_symmetric else "Anti-Simetrična" if is_anti_symmetric else "Nije Simetrična"
    return jsonify({'symmetry': result})

@app.route('/operate', methods=['POST'])
def operate():
    operation = request.json['operation']
    matrix_a = request.json['matrixA']
    matrix_b = request.json['matrixB']
    result = []

    try:
        if operation == 'add':
            result = [[matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
        elif operation == 'subtract':
            result = [[matrix_a[i][j] - matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
        elif operation == 'multiply':
            if len(matrix_a[0]) != len(matrix_b):
                raise ValueError("Broj stupaca matrice A nije jednak broju redaka matrice B!")
            result = [
                [sum(matrix_a[i][k] * matrix_b[k][j] for k in range(len(matrix_b))) for j in range(len(matrix_b[0]))]
                for i in range(len(matrix_a))
            ]
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(result)

@app.route('/matrix_info', methods=['POST'])
def matrix_info():
    matrix = request.json['matrix']
    transposed = [list(row) for row in zip(*matrix)]

    is_symmetric = matrix == transposed
    is_anti_symmetric = matrix == [[-cell for cell in row] for row in transposed]

    result = "Simetrična" if is_symmetric else "Anti-Simetrična" if is_anti_symmetric else "Nije Simetrična"
    return jsonify({'symmetry': result, 'transposed': transposed})

if __name__ == '__main__':
    app.run(debug=True)
