from .__init__ import app


@app.route('/')
def root_view():
    return 'Hello World '
