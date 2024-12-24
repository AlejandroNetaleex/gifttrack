from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os

app = Flask(__name__)
DATABASE = 'database.xlsx'

# Leer datos desde Excel
def read_data():
    return pd.read_excel(DATABASE)

# Escribir datos en Excel
def write_data(df):
    df.to_excel(DATABASE, index=False)

@app.route('/')
def index():
    query = request.args.get('q')  # Obtener término de búsqueda
    data = read_data()

    if query:
        # Filtrar solo por "Código"
        data = data[data['CODIGO'].astype(str).str.contains(query, case=False, na=False)]

    return render_template('index.html', tables=data.to_dict('records'), query=query)

@app.route('/add', methods=['POST'])
def add():
    new_data = {
        'FECHA-ALTA': request.form['fecha'],
        'AREA': request.form['area'],
        'EQUIPO': request.form['equipo'],
        'MARCA': request.form['marca'],
        'NUMERO DE SERIE': request.form['serie'],
        'CODIGO': request.form['codigo']
    }
    df = read_data()
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    write_data(df)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    df = read_data()
    df = df.drop(index).reset_index(drop=True)
    write_data(df)
    return redirect(url_for('index'))

@app.route('/update/<int:index>', methods=['GET', 'POST'])
def update(index):
    df = read_data()

    if request.method == 'POST':
        # Actualizar datos del registro
        df.loc[index, 'FECHA-ALTA'] = request.form['fecha']
        df.loc[index, 'AREA'] = request.form['area']
        df.loc[index, 'EQUIPO'] = request.form['equipo']
        df.loc[index, 'MARCA'] = request.form['marca']
        df.loc[index, 'NUMERO DE SERIE'] = request.form['serie']
        df.loc[index, 'CODIGO'] = request.form['codigo']
        write_data(df)
        return redirect(url_for('index'))

    # Renderizar formulario de actualización
    record = df.loc[index].to_dict()
    return render_template('update.html', record=record, index=index)

@app.route('/export', methods=['POST'])
def export_to_excel():
    df = read_data()
    # Guardar el archivo Excel en la carpeta del proyecto
    file_path = os.path.join(os.getcwd(), "etiquetas.xlsx")
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
