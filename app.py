from flask import Flask, render_template, redirect, url_for, session, request
import os

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
        
        session['materiais'] = []  # Inicializar a lista de materiais

        return redirect(url_for('cadastro_material'))

    return render_template('cadastro_dados.html')

@app.route('/cadastro_material', methods=['GET', 'POST'])
def cadastro_material():
    if 'materiais' not in session:
        session['materiais'] = []

    if request.method == 'POST':
        tipo = request.form['material']
        peso = float(request.form['peso'])
        session['materiais'].append({'tipo': tipo, 'peso': peso})
        
        return redirect(url_for('recompensas'))

    return render_template('cadastro_material.html')

@app.route('/recompensas')
def recompensas():
    materiais = session.get('materiais', [])
    total_pontos = calcular_pontos(materiais)

    if total_pontos is None:
        total_pontos = 0

    recompensas_disponiveis = [
        {'nome': '1h de estacionamento', 'pontos': 150},
        {'nome': 'Ingresso de cinema', 'pontos': 300},
        {'nome': 'Entrada para o Inhotim', 'pontos': 700}
    ]

    recompensas_obtidas = [r['nome'] for r in recompensas_disponiveis if total_pontos >= r['pontos']]
    
    # Salvar total de pontos e recompensas na sessão
    session['total_pontos'] = total_pontos
    session['recompensas_obtidas'] = recompensas_obtidas

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    nome = session.get('nome', 'Usuário')
    materiais = session.get('materiais', [])
    total_pontos = session.get('total_pontos', 0)
    recompensas_obtidas = session.get('recompensas_obtidas', [])

    return render_template('dashboard.html', nome=nome, materiais=materiais, total_pontos=total_pontos, recompensas_obtidas=recompensas_obtidas)

def calcular_pontos(materiais):
    total_pontos = 0
    for material in materiais:
        if material['tipo'] == 'metal':
            total_pontos += material['peso'] * 0.005  # 5 pts por grama de metal
        elif material['tipo'] == 'plastico':
            total_pontos += material['peso'] * 0.001  # 1 pt por grama de plástico
        elif material['tipo'] == 'papel':
            total_pontos += material['peso'] * 0.01   # 10 pts por grama de papel
        elif material['tipo'] == 'vidro':
            total_pontos += material['peso'] * 0.003  # 3 pts por grama de vidro
            
    return total_pontos

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
