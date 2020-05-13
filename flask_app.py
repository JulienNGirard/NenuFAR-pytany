
# A very simple Flask Hello World app for you to get started with...

#from flask import Flask

#app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello from Flask!'


from flask import Flask, request, render_template, jsonify

from data_rate_vol import data_rate_vol

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def init():
    return render_template('index.html',res='not yet computed')

@app.route("/ajax", methods=["GET","POST"])
def indexajax():
    errors = ""
    if request.method == "POST":
        Nma = None
        Nch = None
        dt = None
        Df = None
        Nb= None
        Tobs = None
        Mode = None
        Sum = False


       # Nma=96,Nch=64,dt=1,Df=75,Nb=1,Tobs=3600,mode="BF",Sum=False)
        try:
            Nma = int(request.form["nma"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["nma"])
        try:
            Nch = int(request.form["nch"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["nch"])

        try:
            dt = float(request.form["dt"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["dt"])
        try:
            Df = float(request.form["df"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["df"])

        try:
            Nb = float(request.form["nb"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["nb"])

        try:
            Tobs = float(request.form["tobs"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["tobs"])
        try:
            Mode = str(request.form["mode"])
        except:
            errors += "<p>{!r} is not a valid choice.</p>\n".format(request.form["mode"])

        if Nma is not None and Nch is not None and dt is not None and Df is not None and Tobs is not None and Mode is not None:
            results = data_rate_vol(Nma,Nch,dt,Df,Nb,Tobs,Mode,Sum)
            return jsonify(results=results)


    return '''
        <html>
        {errors}
        </html>
    '''.format(errors=errors)

@app.route("/", methods=["GET", "POST"])
def index():
    errors = ""
    if request.method == "POST":
        Nma = None
        Nch = None
        dt = None
        Df = None
        Nb= None
        Tobs = None
        Mode = None
        Sum = False


       # Nma=96,Nch=64,dt=1,Df=75,Nb=1,Tobs=3600,mode="BF",Sum=False)
        try:
            Nma = int(request.form["nma"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["nma"])
        try:
            Nch = int(request.form["nch"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["nch"])

        try:
            dt = float(request.form["dt"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["dt"])
        try:
            Df = float(request.form["df"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["df"])

        try:
            Nb = float(request.form["nb"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["nb"])

        try:
            Tobs = float(request.form["tobs"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["tobs"])
        try:
            Mode = str(request.form["mode"])
        except:
            errors += "<p>{!r} is not a valid choice.</p>\n".format(request.form["mode"])

        if Nma is not None and Nch is not None and dt is not None and Df is not None and Tobs is not None and Mode is not None:
            results = data_rate_vol(Nma,Nch,dt,Df,Nb,Tobs,Mode,Sum)
            return render_template("index.html",results=results)


    return '''
        <html>
        {errors}
        </html>
    '''.format(errors=errors)




