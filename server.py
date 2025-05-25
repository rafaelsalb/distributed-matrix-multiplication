import time
from flask import Flask, request

from matrix import Matrix


app = Flask(__name__)

@app.route('/multiply', methods=['POST'])
def multiply():
    A = Matrix.from_list(request.json['A'])
    B = Matrix.from_list(request.json['B'])
    key = request.json['key']
    print(f"Multiplicando submatriz {key} com matriz B")

    a = time.monotonic()
    C = A * B
    b = time.monotonic()
    _time = b - a
    print(f"Submatriz {key} multiplicada com matriz B")
    print(f"Tempo de execução: {_time:.2f} s")

    return {
        'result': list(C),
        'time': _time,
        'key': key
    }


if __name__ == "__main__":
    import sys
    app.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)
