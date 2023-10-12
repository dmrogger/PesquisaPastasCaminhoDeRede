import os
import re
import win32
import logging
import win32con
import datetime
import psycopg2
import win32security
import win32.win32api
import win32.win32security

# Inicializa o arquivo de LOG
logging.basicConfig(filename='ErroDuranteExecucao', level=logging.ERROR)

# Estabelece Conexão com o banco de dados
conexao = psycopg2.connect(
    host="",
    port="",
    database="",
    user="",
    password="",
    client_encoding='utf-8'
)


# Classe para que seja possível passar um outro usuário, caso o user
# que esteja logado na maquina não tenha permissão para acessar a pasta de rede
class Impersonate:

    def __init__(self, login, password):
        self.domain = ''
        self.login = login
        self.password = password

    def logon(self):
        self.handle = win32.win32security.LogonUser(self.login, self.domain, self.password,
                                                    win32con.LOGON32_LOGON_INTERACTIVE,
                                                    win32con.LOGON32_PROVIDER_DEFAULT)
        win32.win32security.ImpersonateLoggedOnUser(self.handle)

    def logoff(self):
        win32security.RevertToSelf()  # terminates impersonation
        self.handle.Close()  # guarantees cleanup


# Dados do user que ira logar na pasta de rede
if __name__ == '__main__':
    a = Impersonate('usuario', 'Senha')
    a.logon()


# Verifica se as pastas CPF filtradas possuem arquivos
def pesquisa_arquivos(ls_caminho):
    for caminho, nome_pastas_filtradas, arquivos in os.walk(ls_caminho):
        for name in arquivos:
            if (os.path.join(name)) != "":
                caminho = re.sub('[^0-9]', '', caminho)
                cnpj = caminho[0:14]
                cpf = caminho[14:25]
                cursor = conexao.cursor()  # Definindo um cursor
                consulta = 'SELECT num_cpf FROM caerdsrelatorios_documentos ' \
                           'WHERE num_cpf = %s AND num_cnpj = %s'
                cursor.execute(consulta, (cpf, cnpj))
                if len(cursor.fetchall()) > 0:
                    cursor = conexao.cursor()
                    update = 'UPDATE caerdsrelatorios_documentos SET flg_contem_arquivo = (%s) ' \
                             'WHERE num_cpf = %s AND num_cnpj = %s'
                    cursor.execute(update, ('S', cpf, cnpj))
                    conexao.commit()
                else:
                    cursor = conexao.cursor()
                    insert = 'INSERT INTO caerdsrelatorios_documentos (num_cnpj, num_cpf, flg_contem_arquivo) ' \
                             'VALUES (%s, %s, %s)'
                    cursor.execute(insert, (cnpj, cpf, 'S'))
                    conexao.commit()
                return True


# Função que filtra todas as pastas CPF
def pesquisa_pastas_cpf(ls_caminho, li_tamanho_caracteres):
    for caminho, nome_pastas, arquivos in os.walk(ls_caminho):
        for nome_pastas in nome_pastas:
            if nome_pastas.isnumeric() and len(nome_pastas) == li_tamanho_caracteres:
                if not pesquisa_arquivos(caminho + "\\" + nome_pastas):
                    caminho_filtrado = (caminho + "\\" + nome_pastas)
                    caminho_filtrado = re.sub('[^0-9]', '', caminho_filtrado)
                    cnpj = caminho_filtrado[0:14]
                    cpf = caminho_filtrado[14:25]
                    cursor = conexao.cursor()
                    consulta = 'SELECT num_cpf FROM caerdsrelatorios_documentos WHERE num_cpf = %s AND num_cnpj = %s'
                    cursor.execute(consulta, (cpf, cnpj))
                    if len(cursor.fetchall()) > 0:
                        cursor = conexao.cursor()
                        update = 'UPDATE caerdsrelatorios_documentos SET flg_contem_arquivo = (%s) ' \
                                 'WHERE num_cpf = %s AND num_cnpj = %s'
                        cursor.execute(update, ('N', cpf, cnpj))
                        conexao.commit()
                    else:
                        cursor = conexao.cursor()
                        insert = 'INSERT INTO caerdsrelatorios_documentos (num_cnpj,num_cpf, flg_contem_arquivo) ' \
                                 'VALUES (%s, %s, %s)'
                        cursor.execute(insert, (cnpj, cpf, 'N'))
                        conexao.commit()


# Função que filtra todas as pastas CNPJ
def pesquisa_pastas_cnpj(ls_caminho, li_tamanho_caracteres):
    for caminho, nome_pastas, arquivos in os.walk(ls_caminho):
        for nome_pastas in nome_pastas:
            nome_pastas = re.sub('[^0-9]', '', nome_pastas)
            if nome_pastas.isnumeric() and len(nome_pastas) == li_tamanho_caracteres:
                pesquisa_pastas_cpf(caminho + "\\" + nome_pastas, 11)


caminhoRaiz = r"Caminho da pasta aqui"

# Regex para verificar o caminho caso o mesmo tenha números
# verificaCaminho = re.sub('[^0-9]', '', caminhoRaiz) 


try:
    # Grava a data e hora de inicio da execução para fins de log
    inicio = datetime.datetime.now()
    a.logon()
    pesquisa_pastas_cnpj(caminhoRaiz, 14)
    a.logoff()
    conexao.close()

    # Grava a data e hora de fim da execução para fins de log
    fim = datetime.datetime.now()
    tempo_total_execucao = fim - inicio

    # Gera arquivo de log do temp ode execução da aplicação
    with open('meu_arquivo_de_log.txt', 'w') as arquivo_log:
        arquivo_log.write(f'Início Execução: {inicio}')
        arquivo_log.write(f'\n\nFinal Execução: {fim}')
        arquivo_log.write(f'\n\n\n\nTempo gasto na execução: {tempo_total_execucao}')
        arquivo_log.close()

# Gera arquivo de log de erro acaso venha a ocorrer algum erro
except Exception as e:
    # registrar informações sobre o erro em um arquivo de texto
    logging.error(str(e))
