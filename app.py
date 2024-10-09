from flask import Flask, render_template, redirect, url_for, session, request, flash

app = Flask(__name__)
app.secret_key = 's3gR3D0_Muito_Secreta'  # Use uma chave secreta mais complexa

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_dados', methods=['GET', 'POST'])
def cadastro_dados():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        endereco = request.form['endereco']

        # Validação simples
        if not nome or not email or not endereco:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('cadastro_dados'))

        session['nome'] = nome
        session['email'] = email
        session['endereco'] = endereco
        session['materiais'] = []  # Inicializar a lista de materiais

        return redirect(url_for('cadastro_material'))

    return render_template('cadastro_dados.html')

@app.route('/cadastro_material', methods=['GET', 'POST'])
def cadastro_material():
    if 'materiais' not in session:
        session['materiais'] = []

    if request.method == 'POST':
        tipo = request.form['material']
        peso = request.form['peso']

        # Validação do peso
        try:
            peso = float(peso)
            if peso <= 0 or peso > 10000:  # Peso deve ser positivo e não exceder 10.000g
                flash('Peso inválido! Insira um peso entre 1 e 10.000 gramas.', 'error')
                return redirect(url_for('cadastro_material'))
        except ValueError:
            flash('Peso deve ser um número!', 'error')
            return redirect(url_for('cadastro_material'))

        session['materiais'].append({'tipo': tipo, 'peso': peso})
        flash('Material cadastrado com sucesso!', 'success')
        
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
    
    return render_template('recompensas.html', total_pontos=total_pontos, recompensas_obtidas=recompensas_obtidas)

def calcular_pontos(materiais):
    total_pontos = 0
    for material in materiais:
        if material['tipo'] == 'metal':
            total_pontos += material['peso'] * 0.05  # 5 pts por grama de metal
        elif material['tipo'] == 'plastico':
            total_pontos += material['peso'] * 0.01  # 1 pt por grama de plástico
        elif material['tipo'] == 'papel':
            total_pontos += material['peso'] * 0.01   # 10 pts por grama de papel
        elif material['tipo'] == 'vidro':
            total_pontos += material['peso'] * 0.03  # 3 pts por grama de vidro
            
    return total_pontos

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Para o Heroku
