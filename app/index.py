import analysis
import callbacks

from app import app

app.layout = analysis.body


if __name__ == '__main__':
    app.run_server(debug=True)