from game.run import *

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chess():
    command = receive_command()
    game = Game()
    if isinstance(command, str) == False:
        result = game.chess_board.board
        return render_template('main.html', result=result)
    else:
        result = game.run([command])
        return render_template('main.html', result=result)

@app.route('/postmethod', methods=['POST'])
def receive_command():
    if request.method == 'POST':
        jsdata = request.get_json()
        return jsdata

if __name__=='__main__':
    app.run(debug=True)



# return ' '.join(map(str, result))
# return jsonify(result)