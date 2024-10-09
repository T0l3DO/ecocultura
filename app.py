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
        
        # Verificar os dados da sessão
        print(session)  # Isso permitirá visualizar os dados no console
        
        return redirect(url_for('dashboard'))

    return render_template('cadastro_material.html')


@app.route('/dashboard')
def dashboard():
    nome = session.get('nome', 'Usuário')
    materiais = session.get('materiais', [])
    total_pontos = calcular_pontos(materiais)

    recompensas_disponiveis = [
        {'nome': '1h de estacionamento', 'pontos': 150},
        {'nome': 'Ingresso de cinema', 'pontos': 300},
        {'nome': 'Entrada para o Inhotim', 'pontos': 700}
    ]

    recompensas_obtidas = [r['nome'] for r in recompensas_disponiveis if total_pontos >= r['pontos']]
    
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
    app.run(debug=True)
