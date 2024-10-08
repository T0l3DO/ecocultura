from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = 'segredo'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_dados', methods=['GET', 'POST'])
def cadastro_dados():
    if request.method == 'POST':
        session['nome'] = request.form['nome']
        session['email'] = request.form['email']
        session['endereco'] = request.form['endereco']
        
        session['materiais'] = []  # Inicializa a lista de materiais

        return redirect(url_for('cadastro_material'))

    return render_template('cadastro_dados.html')

@app.route('/cadastro_material', methods=['GET', 'POST'])
def cadastro_material():
    if 'materiais' not in session:
        session['materiais'] = []  # Inicializa se não existir

    if request.method == 'POST':
        tipo = request.form['material']
        peso = float(request.form['peso'])
        session['materiais'].append({'tipo': tipo, 'peso': peso})  # Armazena materiais na sessão
        return redirect(url_for('recompensas'))  # Redireciona para a página de recompensas

    return render_template('cadastro_material.html')

@app.route('/recompensas')
def recompensas():
    materiais = session.get('materiais', [])  # Obtém materiais da sessão
    total_pontos = calcular_pontos(materiais)  # Calcula os pontos

    # Se total_pontos for None, define como 0
    total_pontos = 0

    recompensas_disponiveis = [
        {'nome': '1h de estacionamento', 'pontos': 150},
        {'nome': 'Ingresso de cinema', 'pontos': 300},
        {'nome': 'Entrada para o Inhotim', 'pontos': 700}
    ]

    recompensas_obtidas = [r['nome'] for r in recompensas_disponiveis if total_pontos >= r['pontos']]
    
    return render_template('recompensas.html', total_pontos=total_pontos, recompensas_obtidas=recompensas_obtidas)

def calcular_pontos(materiais):
    total_pontos = 0
    for material in materiais:
        print("Material:", material)  # Para verificar cada material
        if material['tipo'] == 'metal':
            total_pontos += material['peso'] * 0.005
        elif material['tipo'] == 'plastico':
            total_pontos += material['peso'] * 0.001
        elif material['tipo'] == 'papel':
            total_pontos += material['peso'] * 0.01
        elif material['tipo'] == 'vidro':
            total_pontos += material['peso'] * 0.003
            
    print("Total de pontos calculados:", total_pontos)  # Para verificar o total
    return total_pontos  # Sempre retorna um número, mesmo que seja 0

if __name__ == '__main__':
    app.run(debug=True)
