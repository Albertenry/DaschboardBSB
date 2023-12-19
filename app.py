import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# Título da aplicação

st.set_page_config(
    page_title="BSBDASH",
    layout="wide",  # Usa o layout 'wide' para ocupar toda a largura da tela
    # Define o estado inicial do sidebar como fechado
    initial_sidebar_state="collapsed"
)

st.title(":bar_chart: BSBDASH")

if os.path.exists("dados_equipamentos.csv"):
    df = pd.read_csv("dados_equipamentos.csv")
else:
    df = pd.DataFrame(columns=["Mês", "Cliente", "Equipamento", "Quantidade de Ordens de Serviço Abertas",
                               "Quantidade de Horas Usadas nas Ordens de Serviço",
                               "Quantidade de Horas Totais do Equipamento",
                               "Disponibilidade", "Indisponibilidade", "MTTR", "MTBF"])

# Barra lateral para seleção de cliente, equipamento e quantidade de meses
cliente_selecionado = st.sidebar.selectbox("Selecione o Cliente", df["Cliente"].unique())

# Filtrar equipamentos com base no cliente selecionado
equipamentos_cliente = df[df["Cliente"] == cliente_selecionado]["Equipamento"].unique()

# Selecionar equipamento apenas se houver equipamentos associados ao cliente
if equipamentos_cliente.size > 0:  # Verifica se há elementos no array
    equipamento_selecionado = st.sidebar.selectbox("Selecione o Equipamento", equipamentos_cliente)
else:
    st.sidebar.warning("Nenhum equipamento associado ao cliente selecionado.")
    equipamento_selecionado = None


# Filtrar dados com base nas seleções

dados_filtrados = df[(df["Cliente"] == cliente_selecionado) & (
    df["Equipamento"] == equipamento_selecionado)]

# Mostrar quantidade de meses para o equipamento selecionado

quantidade_meses = st.sidebar.multiselect(
    "Selecione os Meses", dados_filtrados["Mês"].unique())

# Criar campos para entrada de dados na barra lateral

st.sidebar.header("Novo Equipamento")
mes = st.sidebar.text_input("Mês:")
cliente = st.sidebar.text_input("Cliente:")
equipamento = st.sidebar.text_input("Equipamento:")
quantidade_ordens_servico = st.sidebar.number_input(
    "Quantidade de Ordens de Serviço Abertas:", min_value=0, step=1)
horas_usadas = st.sidebar.number_input(
    "Quantidade de Horas Usadas nas Ordens de Serviço:", min_value=0, step=1)
horas_totais = st.sidebar.number_input(
    "Quantidade de Horas Totais do Equipamento:", min_value=0, step=1)

# Calcular Disponibilidade, Indisponibilidade, MTTR e MTBF

def calcular_disponibilidade(horas_usadas, horas_totais):
    if horas_totais > 0:
        return (horas_totais - horas_usadas) / horas_totais
    else:
        return 0

# Função para calcular Indisponibilidade

def calcular_indisponibilidade(disponibilidade):
    return 1 - disponibilidade

# Função para calcular MTTR (Mean Time To Repair)

def calcular_mttr(horas_usadas, quantidade_ordens_servico):
    if quantidade_ordens_servico == 0:
        return 0
    return horas_usadas / quantidade_ordens_servico

# Função para calcular MTBF (Mean Time Between Failures)

def calcular_mtbf(horas_totais, quantidade_ordens_servico):
    if quantidade_ordens_servico == 0:
        return 0
    return horas_totais / quantidade_ordens_servico

disponibilidade = calcular_disponibilidade(horas_usadas, horas_totais)
indisponibilidade = calcular_indisponibilidade(disponibilidade)
mttr = calcular_mttr(horas_usadas, quantidade_ordens_servico)
mtbf = calcular_mtbf(horas_totais, quantidade_ordens_servico)

# Mostrar os resultados na barra lateral

st.sidebar.subheader("Resultados:")
st.sidebar.write(f"Disponibilidade: {disponibilidade:.2f}")
st.sidebar.write(f"Indisponibilidade: {indisponibilidade:.2f}")
st.sidebar.write(f"MTTR: {mttr:.2f}")
st.sidebar.write(f"MTBF: {mtbf:.2f}")


dados_filtrados = df[(df["Cliente"] == cliente_selecionado) & (
    df["Equipamento"] == equipamento_selecionado) & (df["Mês"].isin(quantidade_meses))]


# Calcular a quantidade da coluna Indisponibilidade (em porcentagem)
quantidade_indisponibilidade = dados_filtrados["Indisponibilidade"].mean() * 100

quantidade_disponibilidade = 100 - quantidade_indisponibilidade

# Calcular a média da coluna MTTR em horas
media_mttr_horas = dados_filtrados["MTTR"].mean()

# Calcular a média da coluna MTBF em horas
media_mtbf_horas = dados_filtrados["MTBF"].mean()

col1, col2, col3, col4, col5, col6, col7 = st.columns(
    [0.2, 0.05, 0.2, 0.05, 0.2, 0.05, 0.2])

# Criação dos containers
with col1:
    container1 = st.container()
with col3:
    container2 = st.container()
with col5:
    container3 = st.container()
with col7:
    container4 = st.container()

# Card 1: Disponibilidade
container1.markdown(
    """
    <style>
    .custom-container {
        background: linear-gradient(to bottom, #000000, #0000FF);
        border-radius: 12px;
        padding: 30px;
        color: #ffffff;
        text-align: center;
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Adicione o estilo CSS ao contêiner 1 usando a classe personalizada
with container1:
    st.markdown('<div class="custom-container">Disponibilidade<br>{:.2f}%</div>'.format(
        quantidade_disponibilidade), unsafe_allow_html=True)

# Card 2: Indisponibilidade
container2.markdown(
    """
    <style>
    .custom-container {
        background: linear-gradient(to bottom, #000000, #0000FF);
        border-radius: 12px;
        padding: 30px;
        color: #ffffff;
        text-align: center;
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Adicione o estilo CSS ao contêiner 2 usando a classe personalizada
with container2:
    st.markdown('<div class="custom-container">Indisponibilidade<br>{:.2f}%</div>'.format(
        quantidade_indisponibilidade), unsafe_allow_html=True)

# Card 3: MTTR (Média)
container3.markdown(
    """
    <style>
    .custom-container {
        background: linear-gradient(to bottom, #000000, #0000FF);
        border-radius: 12px;
        padding: 30px;
        color: #ffffff;
        text-align: center;
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Adicione o estilo CSS ao contêiner 3 usando a classe personalizada
with container3:
    st.markdown('<div class="custom-container">MTTR (M/h)<br>{:.2f}</div>'.format(
        media_mttr_horas), unsafe_allow_html=True)

# Card 4: MTBF (Média)
container4.markdown(
    """
    <style>
    .custom-container {
        background: linear-gradient(to bottom, #000000, #0000FF);
        border-radius: 12px;
        padding: 30px;
        color: #ffffff;
        text-align: center;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Adicione o estilo CSS ao contêiner 4 usando a classe personalizada
with container4:
    st.markdown('<div class="custom-container">MTBF (M/h)<br>{:.2f}</div>'.format(
        media_mtbf_horas), unsafe_allow_html=True)

st.markdown("""---""")

#############################################################################################################
#############################################################################################################
col1, col2, col3 = st.columns(
    [0.7, 0.1, 0.2])
with col3:
    ###########################
    # Grafico de Rosca
    ###########################

    # Filtrar dados com base nas seleções
    dados_selecionados = df[(df["Cliente"] == cliente_selecionado) & (
        df["Equipamento"] == equipamento_selecionado) & (df["Mês"].isin(quantidade_meses))]

    # Dados para o gráfico de rosca

    labels = ['Disponibilidade', 'Indisponibilidade']
    values = [quantidade_disponibilidade, quantidade_indisponibilidade]

# Criar o gráfico de rosca
    Blue =  color_continuous_scale=[(0, '#000000'), (1, '#0000FF')],
    colors = ['Blue', 'Gold']

# Criar o gráfico de rosca com cores personalizadas
    fig_donut = go.Figure(
        data=[go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=colors))])


# Configurar o layout do gráfico de rosca
    fig_donut.update_layout(
        title='Disponib. vs Indisponib.',
        plot_bgcolor='GhostWhite',  # Cor de fundo do gráfico
        # Posiciona a legenda abaixo do gráfico
        legend=dict(orientation="h", x=0.5, y=-0.2)
    )

# Exibir o gráfico de rosca com tamanho personalizado e rótulos abaixo
    st.plotly_chart(fig_donut, use_container_width=True, width=800, height=600)

    ################################
    # Exibir Tabela
    ################################

st.header("Dados Existentes:")

if quantidade_meses:
    dados_selecionados = dados_filtrados[dados_filtrados["Mês"].isin(
        quantidade_meses)]

    # Calcular o tempo em horas de Disponibilidade
    dados_selecionados["Tempo de Disponibilidade (horas)"] = (
        dados_selecionados["Quantidade de Horas Totais do Equipamento"] -
        dados_selecionados["Quantidade de Horas Usadas nas Ordens de Serviço"]
    ) * (100 - dados_selecionados["Indisponibilidade"]) / 100

    # Multiplicar os valores de Disponibilidade e Indisponibilidade por 100 para porcentagem
    dados_selecionados["Disponibilidade"] *= 100
    dados_selecionados["Indisponibilidade"] *= 100

    # Arredondar os valores para 2 casas decimais
    dados_selecionados["Disponibilidade"] = dados_selecionados["Disponibilidade"].round(
        2)
    dados_selecionados["Indisponibilidade"] = dados_selecionados["Indisponibilidade"].round(
        2)

    # Adicionar o símbolo de porcentagem (%) antes dos valores
    dados_selecionados["Disponibilidade"] = dados_selecionados["Disponibilidade"].astype(
        str) + "%"
    dados_selecionados["Indisponibilidade"] = dados_selecionados["Indisponibilidade"].astype(
        str) + "%"

    # Exibir os dados selecionados
    st.write(dados_selecionados)
else:
    st.write("Nenhum mês selecionado. Por favor, escolha os meses na barra lateral.")


# Verificar se a coluna MTTR está em proporção ou porcentagem e converter para porcentagem
    if dados_selecionados["MTTR"].max() <= 1:
        # Se a coluna MTTR estiver em proporção (0 a 1), multiplicar por 100
        dados_selecionados["MTTR"] *= 100

# Arredondar os valores para 2 casas decimais
        dados_selecionados["MTTR"] = dados_selecionados["MTTR"].round(2)
# Adicionar o símbolo de porcentagem (%) antes dos valores
        dados_selecionados["MTTR"] = dados_selecionados["MTTR"].astype(
            str) + "%"

        st.write(dados_selecionados)

        labels = ['Disponibilidade', 'Indisponibilidade']
        values = [quantidade_disponibilidade, quantidade_indisponibilidade]

    else:
        st.write(
            "Nenhum mês selecionado. Por favor, escolha os meses na barra lateral.")

with col1:

    ########################
    # grafico MTTR
    ########################

    fig_wave = go.Figure()
    fig_wave.add_trace(go.Scatter(
        x=dados_selecionados["Mês"],
        y=dados_selecionados["MTTR"],
        mode='lines',
        line=dict(color='blue', width=2),
        fill='tozeroy',
        fillcolor=("#FFD700"),
        name='MTTR'
    ))
    fig_wave.update_layout(
        xaxis_title='Mês',
        yaxis_title='MTTR',
        xaxis=dict(tickmode='array',
                   tickvals=dados_selecionados["Mês"], ticktext=dados_selecionados["Mês"]),
        yaxis=dict(tickmode='linear', tick0=0, dtick=1),
        plot_bgcolor='WhiteSmoke',
        height=350  # Definir a altura do gráfico
    )

# Exibir o gráfico MTTR
    st.plotly_chart(fig_wave, use_container_width=True)

# Gráfico MTBF
    fig_mtbf_wave = go.Figure()
    fig_mtbf_wave.add_trace(go.Scatter(
        x=dados_selecionados["Mês"],
        y=dados_selecionados["MTBF"],
        mode='lines',
        line=dict(color='Gold', width=2),
        fill='tozeroy',
        fillcolor=("#0000FF"),
        name='MTBF'
    ))
    fig_mtbf_wave.update_layout(
        xaxis_title='Mês',
        yaxis_title='MTBF',
        xaxis=dict(tickmode='array',
                   tickvals=dados_selecionados["Mês"], ticktext=dados_selecionados["Mês"]),
        yaxis=dict(tickmode='linear', tick0=0, dtick=20),
        plot_bgcolor='WhiteSmoke',
        height=350  # Definir a altura do gráfico
    )

# Exibir o gráfico MTBF
    st.plotly_chart(fig_mtbf_wave, use_container_width=True)


######################################################################################################################
#####################################################################################################################

# Salvar dados no arquivo CSV

if st.sidebar.button("Salvar Equipamento"):

    # Criar um novo DataFrame com os dados
    try:
        novo_dado = {
            "Mês": mes,
            "Cliente": cliente,
            "Equipamento": equipamento,
            "Quantidade de Ordens de Serviço Abertas": quantidade_ordens_servico,
            "Quantidade de Horas Usadas nas Ordens de Serviço": horas_usadas,
            "Quantidade de Horas Totais do Equipamento": horas_totais,
            "Disponibilidade": disponibilidade,
            "Indisponibilidade": indisponibilidade,
            "MTTR": mttr,
            "MTBF": mtbf
        }
        novo_df = pd.DataFrame([novo_dado])

        # Concatenar o novo DataFrame com o DataFrame existente ou criar um novo DataFrame
        try:
            df = pd.read_csv("dados_equipamentos.csv")
            df = pd.concat([df, novo_df], ignore_index=True)
        except FileNotFoundError:
            df = novo_df

        # Salvar o DataFrame no arquivo CSV

        df.to_csv("dados_equipamentos.csv", index=False)
        st.sidebar.success("Equipamento cadastrado com sucesso!")
    except Exception as e:
        st.sidebar.error(f"Ocorreu um erro ao salvar os dados: {e}")

# Mostrar tabela com dados existentes na tela principal
