from controlador import app


if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(host='0.0.0.0',port=5000, debug=True)