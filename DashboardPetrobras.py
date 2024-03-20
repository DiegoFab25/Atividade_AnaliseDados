import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
#from token_craft import st_token_table

# MEU DATAFRAME:
df = pd.read_csv("RelatorioPetro.csv", sep = ";")
print(df)


# Tela de proteção Token: - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Plano de fundo: - - - - - - - - - - - - - - - - - - -
page_bg_img = f"""
<style>
[data-testid = "stAppViewContainer"] > .main {{
background-image: url("https://img.freepik.com/vetores-gratis/fundo-de-textura-empoeirado-grunge_1048-9793.jpg");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid = "stHeader"]{{
background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html = True)


# STREAMLIT - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# BARRA LATERAL : = = = = = = = = = = = = = = = = = =  
st.sidebar.header("Análise de Dados - Diego")

anos = df["Ano"].unique().tolist()
anos_selecionados = st.sidebar.multiselect("Ano", anos, default=[2019])  # Por ano !!!

regioes = df["RegiãoAgregada"].unique().tolist()  # Por Região
regioes_selecionadas = st.sidebar.multiselect("Regiões Agregadas", regioes, default=["Norte-Nordeste"])  # Por Região

tipos_mercado = df["TipoMercado"].unique().tolist()  # Por Mercado
tipos_selecionados = st.sidebar.multiselect("Tipo de Mercado", tipos_mercado, default=["Térmico","Não Térmico"])  # Por Mercado

if st.sidebar.button("Exibir Gráfico"):
    st.header("Tabela")    


# Barra de Filtragem - - - - -
df_filtrado = df[df['Ano'].isin(anos_selecionados)]  # Ano
df_filtrado = df_filtrado[df_filtrado["RegiãoAgregada"].isin(regioes_selecionadas)]  # Região
df_filtrado = df_filtrado[df_filtrado["TipoMercado"].isin(tipos_selecionados)]  # Tipo de Mercado

# Criar checkboxes para escolher qual DataFrame exibir
mostrar_df = st.checkbox("Mostrar DataFrame com base nos filtros", value=True)


# Def's Gráfico : - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

df['Preço em Reais por MMBtu'] = df['Preço em Reais por MMBtu'].str.replace(',', '.').astype(float)
df['data'] = pd.to_datetime(df['Ano'].astype(str) + '-' + df['Mês'].astype(str).str.zfill(2))

def scatter_plot(df, x, y, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))
    plt.scatter(df[x], df[y])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    st.pyplot()

def line_plot(df, x, y, hue, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))
    for key, grp in df.groupby(hue):
        plt.plot(grp[x], grp[y], label=key)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(title=hue)
    st.pyplot()

def aba():
    st.title("Meu Hub")

    # HTML personalizado
    st.markdown("<h2 style='color: blue;'>Sejam bem-vindo, a minha análise de dados!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: green;'>Selecione uma opção no menu lateral para começar.</p>", unsafe_allow_html=True)

# Abas -- -- -- -- -- -- --- --- --- --- --- -- -- -- 

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Hub","Filtragem","📈 Vendas","Pedidos/Estoque","Crescimento/Analise de Retorno","🗃 Dados Brutos"])

with tab1: #PRIMEIRA ABAAAA
    "Tabelas do Stremlit"       
    aba()

    # Criar gráfico com base nas escolhas feitas
    selected_columns = st.multiselect("Selecione as colunas para o gráfico", df_filtrado.columns)
    if selected_columns:
        st.bar_chart(df_filtrado[selected_columns])
    else:
        st.warning("Selecione pelo menos uma coluna para exibir no gráfico.")

with tab2: # SEGUNDA ABAAAAAAAAAAA

    # Exibir DataFrame com base nas escolhas feitas
    if mostrar_df:
        st.dataframe(df_filtrado)
    else:
        st.warning("Selecione pelo menos um DataFrame para exibir.")


    st.subheader("Filtragem Inicial")
    scatter_plot(df, 'Ano', 'Preço em Reais por MMBtu', 'Ano', 'Preço em Reais por MMBtu', 'Preço em Reais por MMBtu ao longo do Tempo')

    
    
with tab3: #TERCEIRA ABAAAAAAAAA

    st.subheader("📈 Vendas")

    if mostrar_df:
        st.dataframe(df_filtrado)
        st.bar_chart(df_filtrado)
    else:
        st.warning("Selecione pelo menos um DataFrame para exibir.")

    scatter_plot(df, 'Ano', 'Preço em Reais por MMBtu', 'Ano', 'Preço em Reais por MMBtu', 'Preço em Reais por MMBtu ao longo do Tempo')



with tab4: #QUARTA ABAAAAAAAAA

    st.subheader("PEDIDOS & ESTOQUES")

    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Gráfico 1: Estoque (Volume em mil metros cúbicos/dia)
    plt.figure(figsize=(10, 6))
    plt.plot(df['data'], df['Volume em mil metros cúbicos/dia'], marker='o', linestyle='-')
    plt.title('Estoque ao longo do tempo')
    plt.xlabel('data')
    plt.ylabel('Volume (mil metros cúbicos/dia)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()

    # Gráfico 2: Pedidos (Preço em Reais por MMBtu)
    plt.figure(figsize=(10, 6))
    plt.plot(df['data'], df['Preço em Reais por MMBtu'], marker='o', linestyle='-')
    plt.title('Preço por MMBtu ao longo do tempo')
    plt.xlabel('data')
    plt.ylabel('Preço (Reais/MMBtu)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()
    

with tab5: #QUINTA ABAAAAAAAAA
    st.subheader("CRESCIMENTO & ANÁLISE DE RETORNO")

    # Verificar se há dados filtrados para exibir
    if mostrar_df:
        # Gráfico de crescimento ao longo do tempo
        st.subheader("Crescimento ao longo do Tempo")
        line_plot(df, 'data', 'Volume em mil metros cúbicos/dia', 'RegiãoAgregada', 'Data', 'Volume em mil metros cúbicos/dia', 'Crescimento ao longo do Tempo')
        
        # Gráfico de análise de retorno
        st.subheader("Análise de Retorno")
        scatter_plot(df, 'Ano', 'Preço em Reais por MMBtu', 'Ano', 'Preço em Reais por MMBtu', 'Preço em Reais por MMBtu ao longo do Tempo')

    else:
        st.warning("Selecione pelo menos uma DataFrame para exibir.")



with tab6: #SEXTA ABAAAAAAAAAAAAAA
    st.subheader("🗃 Dados Brutos")
    st.write(df) 






    