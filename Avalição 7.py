import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from fpdf import FPDF


def extrair_dados_protocolos(url):
    
    html_content = """
    <html>
    <body>
        <div class="protocolo">
            <h2>Protocolo 1</h2>
            <p class="descricao">Descrição do Protocolo 1</p>
            <span class="data">2023-01-01</span>
            <span class="responsavel">João Silva</span>
            <span class="status">Aprovado</span>
        </div>
        <div class="protocolo">
            <h2>Protocolo 2</h2>
            <p class="descricao">Descrição do Protocolo 2</p>
            <span class="data">2023-02-15</span>
            <span class="responsavel">Maria Santos</span>
            <span class="status">Em Revisão</span>
        </div>
        <div class="protocolo">
            <h2>Protocolo 3</h2>
            <p class="descricao">Descrição do Protocolo 3</p>
            <span class="data">2023-03-20</span>
            <span class="responsavel">José Almeida</span>
            <span class="status">Aguardando Aprovação</span>
        </div>
    </body>
    </html>
    """

    
    soup = BeautifulSoup(html_content, 'html.parser')

    protocolos = []
    for protocolo in soup.find_all('div', class_='protocolo'):
        titulo = protocolo.find('h2').text.strip()
        descricao = protocolo.find('p', class_='descricao').text.strip()
        data_criacao = protocolo.find('span', class_='data').text.strip()
        responsavel = protocolo.find('span', class_='responsavel').text.strip()
        status = protocolo.find('span', class_='status').text.strip()

        protocolos.append({
            'Título': titulo,
            'Descrição': descricao,
            'Data de Criação': data_criacao,
            'Responsável': responsavel,
            'Status': status
        })

    return protocolos


url_protocolo = 'https://www.protocolo.com.br'


dados_protocolos = extrair_dados_protocolos(url_protocolo)


df_protocolos = pd.DataFrame(dados_protocolos)


def plotar_grafico_status():
    status_counts = df_protocolos['Status'].value_counts()
    plt.figure(figsize=(8, 5))
    status_counts.plot(kind='bar', color='skyblue')
    plt.title('Contagem de Protocolos por Status')
    plt.xlabel('Status')
    plt.ylabel('Número de Protocolos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()


def main():
    st.title('Análise de Protocolos de Segurança')

    
    st.subheader('Dados dos Protocolos')
    st.dataframe(df_protocolos)

    
    st.subheader('Contagem de Protocolos por Status')
    plotar_grafico_status()

    
    st.subheader('Exportar para PDF')
    if st.button('Gerar Relatório em PDF'):
        conteudo_relatorio = df_protocolos.to_string()
        gerar_pdf('relatorio_protocolos.pdf', conteudo_relatorio)
        st.success('Relatório gerado com sucesso!')


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Protocolos de Segurança', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()


def gerar_pdf(nome_arquivo, conteudo):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Dados dos Protocolos')
    pdf.chapter_body(conteudo)
    pdf.output(nome_arquivo)


if __name__ == '__main__':
    main()

