from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    if 'matrix_ta' not in session:
        session['matrix_ta'] = [[0] * session['rowa'] for _ in range(session['cola'])]
    if 'matrix_tb' not in session:
        session['matrix_tb'] = [[0] * session['rowb'] for _ in range(session['colb'])]

    return render_template(
        'index.html',
        rowa=session['rowa'], cola=session['cola'],
        rowb=session['rowb'], colb=session['colb'],
        matrix_a=session['matrix_a'],
        matrix_b=session['matrix_b'],
        matrix_ta=session['matrix_ta'],
        matrix_tb=session['matrix_tb']
    )

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    action = data.get('action', None)

    if action in ['update_a', 'update_b']:
        matrix_name = 'matrix_a' if action == 'update_a' else 'matrix_b'
        session[matrix_name] = data['matrix']
    elif action == 'add_row_a' and session['rowa'] < 10:
        session['rowa'] += 1
        session['matrix_a'].append([0] * session['cola'])
    elif action == 'remove_row_a' and session['rowa'] > 1:
        session['rowa'] -= 1
        session['matrix_a'].pop()
    elif action == 'add_column_a' and session['cola'] < 10:
        session['cola'] += 1
        for row in session['matrix_a']:
            row.append(0)
    elif action == 'remove_column_a' and session['cola'] > 1:
        session['cola'] -= 1
        for row in session['matrix_a']:
            row.pop()
    elif action == 'add_row_b' and session['rowb'] < 10:
        session['rowb'] += 1
        session['matrix_b'].append([0] * session['colb'])
    elif action == 'remove_row_b' and session['rowb'] > 1:
        session['rowb'] -= 1
        session['matrix_b'].pop()
    elif action == 'add_column_b' and session['colb'] < 10:
        session['colb'] += 1
        for row in session['matrix_b']:
            row.append(0)
    elif action == 'remove_column_b' and session['colb'] > 1:
        session['colb'] -= 1
        for row in session['matrix_b']:
            row.pop()
    elif action == 'TrA':
        session['matrix_ta'] = [
            [session['matrix_a'][row][col] for row in range(session['rowa'])]
            for col in range(session['cola'])
        ]
        session['matrix_a'] = session['matrix_ta']
    elif action == 'TrB':
        session['matrix_tb'] = [
            [session['matrix_b'][row][col] for row in range(session['rowb'])]
            for col in range(session['colb'])
        ]

    session.modified = True

    return jsonify({
        'matrix_a': session['matrix_a'],
        'matrix_b': session['matrix_b'],
        'matrix_ta': session['matrix_ta'],
        'matrix_tb': session['matrix_tb'],
        'rowa': session['rowa'],
        'cola': session['cola'],
        'rowb': session['rowb'],
        'colb': session['colb']
    })

if __name__ == "__main__":
    app.run(debug=True)
