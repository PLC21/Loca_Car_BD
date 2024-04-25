import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from util import get_connection

app = Flask(__name__) 

@app.route('/')

def index():
    return render_template('index.html')

#cliente________________________________________________________________________________________________________

@app.route('/clientes/')
def lista_Clientes():
    con  = get_connection()
    if con is not None:
        cur = con.cursor(dictionary=True)
        sql = """select * from cliente"""
        cur.execute(sql)
        tuplas = cur.fetchall()
        con.close()
        cur.close()
        return render_template("lista_clientes.html", dados=tuplas)
    else:
        return "Erro na conexão com o banco de dados."


@app.route('/clientes/cadastrar/', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        con = get_connection()
        
        if con is not None:
            cur = con.cursor()
            sql = """INSERT INTO cliente (Nome, Telefone) VALUES (%s, %s)"""
            cur.execute(sql, (nome, telefone))
            con.commit()
            cur.close()
            con.close()
            return lista_Clientes()  # Redireciona para a lista de clientes após o cadastro.
        else:
            return "Erro na conexão com o banco de dados."
    else:
        return render_template("cadastro_cliente_form.html")
    
#carros___________________________________________________________________________________________________

@app.route('/Carros/')
def lista_carros():
    con = get_connection()
    if con is not None:
        cur = con.cursor(dictionary=True)
        sql = """
            SELECT c.ID_Carro, c.Modelo, c.Marca, c.Ano, tc.Nome_tipo
            FROM Carro c
            INNER JOIN Tipo_Carro tc ON c.ID_Tipo = tc.ID_Tipo
        """
        cur.execute(sql)
        carros = cur.fetchall()
        cur.close()
        con.close()
        return render_template("lista_carros.html", carros=carros)
    else:
        return "Erro na conexão com o banco de dados."


@app.route('/carros/cadastrar/', methods=['GET', 'POST'])
def cadastrar_carro():
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        ano = request.form['ano']
        tipo_id = request.form['tipo']

        con = get_connection()

        if con is not None:
            cur = con.cursor()
            sql = """INSERT INTO Carro (ID_Tipo, Modelo, Marca, Ano) VALUES (%s, %s, %s, %s)"""
            cur.execute(sql, (tipo_id, modelo, marca, ano))
            con.commit()
            cur.close()
            con.close()
            return lista_carros()
        else:
            return "Erro na conexão com o banco de dados."
    else:
        con = get_connection()
        if con is not None:
            cur = con.cursor(dictionary=True)
            sql = """SELECT ID_Tipo, Nome_tipo FROM Tipo_Carro"""
            cur.execute(sql)
            tipos_carro = cur.fetchall()
            cur.close()
            con.close()
            return render_template("cadastro_carro_form.html", tipos_carro=tipos_carro)
        else:
            return "Erro na conexão com o banco de dados."

#Aluguel____________________________________________________________________________________________

# parte 1 do formulario aluguel
@app.route('/aluguel/realizar/', methods=['GET', 'POST'])
def Realizar_aluguel():
    if request.method == 'POST':
        ID_Cliente = request.form['ID_Cliente']
        Data_inicio = request.form['Data_inicio']
        Numero_dias = request.form['Numero_dias']
        Data_retorno = request.form['Data_retorno']

        
        con = get_connection()

        if con is not None:
            # Redireciona para "carros_disponiveis.html"
            return redirect(url_for('mostrar_carros_disponiveis', ID_Cliente=ID_Cliente, Data_inicio=Data_inicio, Numero_dias=Numero_dias, Data_retorno=Data_retorno))
        else:
            return "Erro na conexão com o banco de dados."
    else:
        con = get_connection()
        if con is not None:
            cur = con.cursor(dictionary=True)
            sql = """SELECT ID_Cliente, Nome FROM cliente"""
            cur.execute(sql)
            tupla = cur.fetchall()
            cur.close()
            con.close()
            return render_template("realizar_aluguel_form.html", ID_Cliente=tupla)
        else:
            return "Erro na conexão com o banco de dados."


# parte 2 do formulario Aluguel

@app.route('/carros/disponiveis/<int:ID_Cliente>/<Data_inicio>/<int:Numero_dias>/<Data_retorno>', methods=['GET', 'POST'])
def mostrar_carros_disponiveis(ID_Cliente, Data_inicio, Numero_dias, Data_retorno):
    if request.method == 'POST':
        ID_Cliente = request.form['ID_Cliente']
        Data_inicio = request.form['Data_inicio']
        Numero_dias = request.form['Numero_dias']
        Data_retorno = request.form['Data_retorno']
        ID_Carro = request.form['ID_Carro'] 
        Valor_total = calcular_valor_total(ID_Carro, Numero_dias)
        
        con = get_connection()

        if con is not None:
            # Redireciona para "finalizar_aluguel.html" com o parâmetro 'Valor_total'
            print("ID_Cliente:", ID_Cliente)
            print("Data_inicio:", Data_inicio)
            print("Numero_dias:", Numero_dias)
            print("Data_retorno:", Data_retorno)
            return redirect(url_for('finalizar_aluguel', ID_Cliente=ID_Cliente, ID_Carro=ID_Carro, Data_inicio=Data_inicio, Numero_dias=Numero_dias, Data_retorno=Data_retorno, Valor_total=Valor_total))
        else:
            return "Erro na conexão com o banco de dados."
    elif request.method == 'GET':
        con = get_connection()
        if con is not None:
            carros_disponiveis = obter_carros_disponiveis(Data_inicio, Numero_dias)
            return render_template("carros_disponiveis.html", carros_disponiveis=carros_disponiveis, ID_Cliente=ID_Cliente, Data_inicio=Data_inicio, Numero_dias=Numero_dias, Data_retorno=Data_retorno)
        else:
            return "Erro na conexão com o banco de dados."
    else:
        return "Método HTTP não suportado."


# parte 3 do formulario ALuguel


@app.route('/alugueis/finalizar/<int:ID_Cliente>/<Data_inicio>/<int:Numero_dias>/<Data_retorno>/<int:ID_Carro>/<float:Valor_total>', methods=['GET', 'POST'])
def finalizar_aluguel(ID_Cliente, ID_Carro, Data_inicio, Numero_dias, Data_retorno, Valor_total):
    # Seu código da rota finalizar_aluguel aqui

    if request.method == 'POST':
        ID_Cliente = int(request.form['ID_Cliente'])
        Data_inicio = request.form['Data_inicio']
        Numero_dias = int(request.form['Numero_dias'])
        Data_retorno = request.form['Data_retorno']
        Valor_total = float(request.form['Valor_total'])
        ID_carro = int(request.form['ID_Carro'])
        Valor_pago = float(request.form['Valor_pago'])

        # Obtenha a data atual
        data_atual = datetime.date.today()
        # Converta Data_inicio para um objeto datetime
        data_inicio = datetime.datetime.strptime(Data_inicio, "%Y-%m-%d").date()
        # Verifique se a Data_inicio está no futuro em relação à data atual
        if data_inicio > data_atual:
            status_tipo = "Agendado"
        else:
            status_tipo = "Ativo"

        con = get_connection()
        if con is not None:
            # Redirecione para a função finalizar_aluguel 
            print("Cheguei Aqui:", ID_Cliente)   
            inserir_aluguel(id_cliente=ID_Cliente, id_carro=ID_carro, data_inicio=Data_inicio, numero_dias=Numero_dias, data_retorno=Data_retorno, valor_total=Valor_total, valor_pago=Valor_pago, status_tipo=status_tipo)
            return redirect(url_for('index'))
        else:
            return "Ação desconhecida."
        
    elif request.method == 'GET':
        con = get_connection()
        # Consulte o banco de dados para obter informações sobre o carro
        cursor = con.cursor(dictionary=True)
        query = """
            SELECT c.Modelo, c.Ano, tc.Nome_tipo, tc.Valor_dias, tc.Valor_semanal
            FROM Carro c
            INNER JOIN Tipo_Carro tc ON c.ID_Tipo = tc.ID_Tipo
            WHERE c.ID_Carro = %s
          """
        cursor.execute(query, (ID_Carro,))
        carro_info = cursor.fetchone()
        cursor.close()

        if con is not None:          
            return render_template("finalizar_aluguel.html", ID_Cliente=ID_Cliente, ID_Carro=ID_Carro, Data_inicio=Data_inicio, Numero_dias=Numero_dias, Data_retorno=Data_retorno, Valor_total=Valor_total, carro_info=carro_info)
            
        else:
            return "Erro na conexão com o banco de dados."
    else:
        return "Método HTTP não suportado."
        
#todos aluguies   
@app.route('/alugueis/consultar/')
def lista_alugueis():
    con  = get_connection()
    if con is not None:
        cur = con.cursor(dictionary=True)
        sql = """select * from aluguel"""
        cur.execute(sql)
        tuplas = cur.fetchall()
        con.close()
        cur.close()
        return render_template("lista_aluguel.html", dados=tuplas)
    else:
        return "Erro na conexão com o banco de dados."
    
#exibe somente alugueis ativos
@app.route('/alugueis/consultar/ativos/')
def lista_alugueis_ativo():
    con = get_connection()
    if con is not None:
        cur = con.cursor(dictionary=True)
        sql = """SELECT * FROM aluguel WHERE Status_Tipo = 'Ativo'"""  
        cur.execute(sql)
        tuplas = cur.fetchall()
        con.close()
        cur.close()
        return render_template("lista_aluguel_ativo.html", dados=tuplas)
    else:
        return "Erro na conexão com o banco de dados."
#exibe somente aluguies agendados

@app.route('/alugueis/consultar/agendados/')
def lista_alugueis_agendados():
    con = get_connection()
    if con is not None:
        cur = con.cursor(dictionary=True)
        sql = """SELECT * FROM aluguel WHERE Status_Tipo = 'Agendado'"""  
        cur.execute(sql)
        tuplas = cur.fetchall()
        con.close()
        cur.close()
        return render_template("lista_aluguel.html", dados=tuplas)
    else:
        return "Erro na conexão com o banco de dados."
    



# finalizar aluguel Ativo





# Função para calcular as datas e valores
def calcular_valores(aluguel, data_entrega, pagamento_final):
    data_retorno = aluguel['Data_retorno']
    valor_dias = aluguel['Valor_dias']

    data_entrega = datetime.datetime.strptime(data_entrega, '%Y-%m-%d').date()

    diferenca_dias = (data_entrega - data_retorno).days

    if diferenca_dias > 0:
        valor_taxa_atraso = aluguel['valor_taxa_atraso']
        valor_semanal = aluguel['Valor_semanal']

        diferenca = 0

        if valor_semanal is not None and diferenca_dias >= 7:
            diferenca = valor_semanal * (diferenca_dias // 7)
        else:
            diferenca = valor_dias * diferenca_dias

        novo_valor_total = aluguel['Valor_Total'] + diferenca
        status_tipo = 'Finalizado_Atrasado'
    else:
        diferenca_dias = abs(diferenca_dias)
        valor_semanal = aluguel['Valor_semanal']

        diferenca = 0

        if valor_semanal is not None and diferenca_dias >= 7:
            diferenca = valor_semanal * (diferenca_dias // 7)
        else:
            diferenca = valor_dias * diferenca_dias

        novo_valor_total = aluguel['Valor_Total'] - diferenca
        status_tipo = 'Finalizado_Adiantado'

    valor_restante = novo_valor_total - pagamento_final

    return novo_valor_total, valor_restante, diferenca, diferenca_dias, status_tipo





# Defina a rota para finalizar a parte 1 do aluguel
@app.route('/alugueis/consultar/ativos/<int:ID_Aluguel>/finalizar/', methods=['GET', 'POST'])
def finalizar_aluguel_ativo_parte1(ID_Aluguel):
    con = get_connection()
    if con is not None:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT a.*, c.ID_Tipo FROM Aluguel a JOIN Carro c ON a.ID_Carro = c.ID_Carro WHERE ID_Aluguel = %s", (ID_Aluguel,))
        aluguel = cursor.fetchone()
    
        if aluguel:
            # Recupere informações do tipo de carro associado ao aluguel
            cursor.execute("SELECT c.ID_Tipo FROM Carro c WHERE c.ID_Carro = %s", (aluguel['ID_Carro'],))
            tipo_carro = cursor.fetchone()

            if tipo_carro:
                aluguel['ID_Tipo'] = tipo_carro['ID_Tipo']
                # Acessando O ID do tipo de carro para buscar as informações necessárias na tabela Tipo_Carro
                cursor.execute("SELECT valor_taxa_atraso, Valor_dias, Valor_semanal FROM Tipo_Carro WHERE ID_Tipo = %s", (tipo_carro['ID_Tipo'],))
                tipo_carro_info = cursor.fetchone()



                if tipo_carro_info:
                    aluguel['valor_taxa_atraso'] = tipo_carro_info['valor_taxa_atraso']
                    aluguel['Valor_dias'] = tipo_carro_info['Valor_dias']
                    aluguel['Valor_semanal'] = tipo_carro_info['Valor_semanal'] 
                  


                    

            if request.method == 'POST':
                data_entrega = request.form['data_entrega']
                pagamento_final = float(request.form.get('pagamento_final', 0.0))  # Usar get com valor padrão
                novo_valor_total, valor_restante, diferenca, num_dias, status_tipo = calcular_valores(aluguel, data_entrega, pagamento_final)
                aluguel['novo_valor_total'] = novo_valor_total
                aluguel['valor_restante'] = valor_restante
                aluguel['diferenca'] = diferenca
                aluguel['num_dias'] = num_dias
                aluguel['status_tipo'] = status_tipo



                return render_template("finalizar_aluguel_ativo_parte2.html",
                                       aluguel=aluguel,
                                       data_entrega=data_entrega,
                                       novo_valor_total=novo_valor_total,
                                       valor_restante=valor_restante,
                                       num_dias=num_dias,
                                       diferenca=diferenca,
                                       status_tipo=status_tipo)
                                       
                                       
            return render_template("finalizar_aluguel_ativo_parte1.html", aluguel=aluguel)
        else:
            flash("Aluguel não encontrado.", "error")
            return redirect(url_for('listar_alugueis_ativos'))
    else:
        flash("Erro na conexão com o banco de dados.", "error")
        return redirect(url_for('listar_alugueis_ativos'))

    







    
# Defina a rota para a parte final da finalização do aluguel
@app.route('/alugueis/consultar/ativos/<int:ID_Aluguel>/finalizar/<string:data_entrega>/final', methods=['POST'])
def finalizar_aluguel_final(ID_Aluguel, data_entrega):
    con = get_connection()
    aluguel = request.args.get('aluguel')


    print("Conteúdo do dicionário 'aluguel' na parte final:", aluguel)  # Linha de depuração



    if con is not None:
        cursor = con.cursor(dictionary=True)

        # Recupere os dados do aluguel do banco de dados
        cursor.execute("SELECT * FROM Aluguel WHERE ID_Aluguel = %s", (ID_Aluguel,))
        aluguel = cursor.fetchone()

        if aluguel is not None:
            pagamento_final = float(request.form.get('pagamento_final', 0.0))  # Usar get com valor padrão
            novo_valor_total = float(aluguel['novo_valor_total'])
            status_tipo = aluguel['status_tipo']
            valor_restante = float(aluguel['valor_restante'])

            cursor = con.cursor()
            cursor.execute("""
                UPDATE Aluguel 
                SET Data_retorno = %s, Valor_Total = %s, Status_Tipo = %s, Valor_pago = Valor_pago + %s 
                WHERE ID_Aluguel = %s
            """, (data_entrega, novo_valor_total, status_tipo, pagamento_final, ID_Aluguel))

            if pagamento_final >= valor_restante:
                cursor.execute("UPDATE Aluguel SET Status_Tipo = 'Finalizado' WHERE ID_Aluguel = %s", (ID_Aluguel,))

            con.commit()
            cursor.close()

            return render_template("finalizar_aluguel_ativo_final.html",
                                   aluguel=aluguel,
                                   num_dias=aluguel['num_dias'],
                                   novo_valor_total=novo_valor_total,
                                   valor_restante=valor_restante,
                                   diferenca=aluguel['diferenca'])
        else:
            flash("Aluguel não encontrado.", "error")
            return redirect(url_for('listar_alugueis_ativos'))
    else:
        flash("Erro na conexão com o banco de dados.", "error")
        return redirect(url_for('listar_alugueis_ativos'))












# Funcoes necessaras______________________________________________________________________________

# Função para obter carros disponíveis
def obter_carros_disponiveis(data_inicio, numero_dias):
    try:
        con = get_connection()
        cursor = con.cursor(dictionary=True)

        # Converter a data de início para um objeto datetime
        data_inicio = datetime.datetime.strptime(data_inicio, "%Y-%m-%d").date()

        # Calcular a data de retorno com base no número de dias
        data_retorno = data_inicio + datetime.timedelta(days=numero_dias)

        # Consulta para obter carros disponíveis
        query = """
            SELECT c.ID_Carro, c.Modelo
            FROM Carro c
            WHERE c.ID_Carro NOT IN (
                SELECT al.ID_Carro
                FROM Aluguel al
                WHERE al.Data_inicio <= %s AND al.Data_retorno >= %s
            )
        """
        cursor.execute(query, (data_retorno, data_inicio))
        carros_disponiveis = cursor.fetchall()

        return carros_disponiveis

    except Exception as e:
        print(f"Erro ao obter carros disponíveis: {str(e)}")
        return []

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

            
#funcao para calcular valor Total

def calcular_valor_total(id_carro, numero_dias):
    print("ID_Cliente: dentro da funcao calcular_valor_total", id_carro)
    print("numero dias: dentro da funcao calcular_valor_total", numero_dias)
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Obtenha as informações de preço do carro com base no ID do carro
        query = """
            SELECT tc.Valor_dias, tc.Valor_semanal
            FROM Carro c
            INNER JOIN Tipo_Carro tc ON c.ID_Tipo = tc.ID_Tipo
            WHERE c.ID_Carro = %s
        """
        cursor.execute(query, (id_carro,))
        carro_info = cursor.fetchone()

        if carro_info:
            #converte valores para float
            valor_dias = float(carro_info["Valor_dias"])
            valor_semanal = float(carro_info["Valor_semanal"])

            # Converta numero_dias para um inteiro
            numero_dias = int(numero_dias)



            # Calcule o valor total com base na duração do aluguel
            semanas = numero_dias // 7
            dias_extras = numero_dias % 7

            valor_total = (semanas * valor_semanal) + (dias_extras * valor_dias)

            return valor_total

    except Exception as e:
        # Trate qualquer erro que possa ocorrer durante o cálculo
        print(f"Erro ao calcular valor total: {e}")

    finally:
        # Certifique-se de fechar o cursor e a conexão, independentemente do resultado
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return 0  # Retorne 0 quando não houver informações disponíveis.


# Função para inserir aluguel no banco de dados
def inserir_aluguel(id_cliente, id_carro, status_tipo, data_inicio, numero_dias, data_retorno, valor_total, valor_pago):
    try:
        # Conecte-se ao banco de dados
        conn = get_connection()
        cursor = conn.cursor()
        # Lógica para inserir o aluguel no banco de dados
        query = """
            INSERT INTO Aluguel (ID_Cliente, ID_Carro, Status_Tipo, Data_inicio, Numero_dias, Data_retorno, Valor_Total, Valor_Pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_cliente, id_carro, status_tipo, data_inicio, numero_dias, data_retorno, valor_total, valor_pago))
        # Commit da transação
        conn.commit()
        # Feche a conexão com o banco de dados
        cursor.close()
        conn.close()
        return True  # Indica que a inserção foi bem-sucedida
    except Exception as e:
        print(f"Erro ao inserir aluguel: {str(e)}")
        return False  # Indica que ocorreu um erro durante a inserção




@app.route('/alterar_taxas/', methods=['GET', 'POST'])
def alterar_taxas():
    con = get_connection()
    if con is not None:
        cursor = con.cursor(dictionary=True)
        
        if request.method == 'POST':
            # Processar o formulário enviado
            tipos_carros = cursor.execute("SELECT * FROM Tipo_Carro")
            
            for tipo_carro in tipos_carros:
                novo_valor_dias = request.form.get(f"novo_valor_dias_{tipo_carro['ID_Tipo']}")
                novo_valor_semanal = request.form.get(f"novo_valor_semanal_{tipo_carro['ID_Tipo']}")
                nova_taxa_atraso = request.form.get(f"nova_taxa_atraso_{tipo_carro['ID_Tipo']}")
                
                # Atualizar os valores no banco de dados
                cursor.execute("UPDATE Tipo_Carro SET Valor_dias = %s, Valor_semanal = %s, valor_taxa_atraso = %s WHERE ID_Tipo = %s",
                               (novo_valor_dias, novo_valor_semanal, nova_taxa_atraso, tipo_carro['ID_Tipo']))
            
            # Commit das alterações no banco de dados
            con.commit()
            
            flash("Valores atualizados com sucesso!", "success")
            return redirect('/alterar_taxas/')
        else:
            # Consulta para obter todos os tipos de carros
            cursor.execute("SELECT * FROM Tipo_Carro")
            tipos_carros = cursor.fetchall()
            con.close()
            cursor.close()
            return render_template("alterar_taxas.html", tipos_carros=tipos_carros)
    else:
        return "Erro na conexão com o banco de dados."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug= True)
