import layout
import callbacks

from app import app

app.layout = layout.body


if __name__ == '__main__':
    app.run_server(debug=True)