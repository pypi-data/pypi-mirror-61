# pymaxdb
Projeto que visa padronizar a comunicação com alguns bancos de dados.

## Objetivo
- Padronizar a conexão com bancos de dados distintos; 
- Utilizar métodos padronizados para realizar operações em bancos de dados;
- Melhorar controle de operações que envolvem atualizações em bancos de dados.

## Instalação
```sh
pip install pymaxdb
```

## Utilização
A comunicação é realizada através da instanciação da classe ***conexao***, que recebe em um de seus parâmetros o nome do banco de dados que se deseja conectar. O parâmetro ***nome_conexao*** recebe nomes pré-definidos, que podem ser: Postgres, (conexão PostgreSQL), DBMakerODBC (necessário criação prévia de uma conexão DBMaker ODBC), SQLServerODBC (conexão SQL Server ODBC) e Firebird (conexão Firebird).

```python
from pymaxdb import conexao

try:
    # Conexão PostgreSQL
    con = conexao(nome_conexao='postgres', host='127.0.0.1', port='5432', db='nome_database', usr='usuário', pwd='senha')

    # Conexão DBMaker ODBC
    # con = conexao(nome_conexao='dbmakerodbc', db='nome_dsn', usr='usuário', pwd='senha')  
    
    # Conexão SQL Server ODBC
    # con = conexao(nome_conexao='sqlserverodbc', db='nome_dsn', usr='usuário', pwd='senha')
    
    # Conexão Firebird
    # con = conexao(nome_conexao='firebird', host='127.0.0.1', port='3050', db='/caminho_database/nome_database.fdb', usr='usuário', pwd='senha')

    con.executar('insert into nome_database values(1)')
    
    con.efetivar() # commit

    rs = con.consultar('select * from nome_database')
    print(rs)

    proximo_registro = con.proxima_chave('nome_database', 'campo_chave')
    print(proximo_registro)

    con.fechar() # close connection       
except Exception as e:    
    print(e)
```

O pacote também possui mais algumas classes e funções utilitárias:

- ***conexao_dbmaker***
  - Permite controlar a quantidade de tentativas de conexão ao banco de dados DBMaker, no caso do número de conexões permitidas exceder.

```python
from pymaxdb import conexao_dbmaker

try:
    con_dbmaker = conexao_dbmaker(tentativas_conexao=3, dsn='nome_dsn', usr='usuário', pwd='senha').conectar()
    print(con_dbmaker.consultar('select * from nome_database'))
    con_dbmaker.fechar()
except Exception as e:
    print(e)
```

- ***remove_ace***
  - Recebe uma string e retorna apenas letras sem acentuação, números e espaços.

```python
from pymaxdb import remove_ace

rem_ace = remove_ace('Composto so de espaço, e/ou tabulação e/ou quebra de linha & números 1, 2 e 3')
print(rem_ace)
```

- ***configurador***
  - Recebe o caminho completo de um arquivo de configuração separado por sessões do tipo chave e valor e retorna um dicionário ou o valor de uma chave, dependendo do método chamado.

```sh
[config1]
chave1 = valor1
chave2 = valor2

[config2]
chave1 = valor1
chave2 = valor2
```

```python
from pymaxdb import configurador

config = configurador(file_config='config/config.cfg')

dic_config = config.get_sessao('config2') # retorna um dicionário com itens da sessão config2
print(dic_config)

valor_config = config.get_item_sessao('config1', 'chave2') # retorna o valor da chave2
print(valor_config)

config.set_file_config('config/config2.cfg') # define outro arquivo de configuração

arquivo_config = config.get_file_config() # retona o nome do arquivo de configuração
print(arquivo_config)
```