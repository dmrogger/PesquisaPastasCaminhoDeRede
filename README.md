
# PesquisaPastasCaminhoDeRede
Este código foi desenvolvido para sanar um problema que estava ocorrendo no momento de  gerar um determinado relatório de uma empresa. 

Existe ao final deste README.md, algumas informações adicionais como: Bibliotecas utilizadas o porque a aplicação ainda não está tão perfomática e etc.

## Orientações para execução da aplicação
A aplicação pode ser executada diretamente no Pycharm ou o código pode ser compilado, com o pyinstaller ou outros. É importante se atentar a algumas váriaveis que devem ser alteradas.

Aqui devem ser inseridos o usuário que possuí acesso a pasta de rede, não precisa ser o mesmo que está logado na máquina.

![Captura de tela 2023-06-11 165804](https://github.com/dmrogger/AcademiaFitnessCenter/assets/86617363/cfedce94-80c6-4cff-aca6-bf3351b32586)

Aqui deve ser inserido o caminho de rede que deseja fazer a busca, **atenção** o caminho de rede não pode possuir números, caso o possua é necessário fazer uma adptação no código para remoção dos números do caminho de rede antes que ele execute as funções de busca, caso contrário os resultados podem ser inconsistentes.

![Captura de tela 2023-06-11 170101](https://github.com/dmrogger/AcademiaFitnessCenter/assets/86617363/045cb99a-b217-47b2-b0fb-19719b61a908)

## Contexto
Existiam diversas pastas de rede nomeadas com números de CNPJ de acordo com a imagem abaixo:

![PastaDeRede](https://github.com/dmrogger/AcademiaFitnessCenter/assets/86617363/453c2d75-ecd4-4486-b6b5-d491b3ab4fc3)

Estas pastas CNPJ's eram de lojas parceiras e dentro delas existiam varias pastas CPF's que eram basicamente onde ficavam os alguns arquivos relacionados aos clientes destas lojas parceiras.
 
![PastaDeRede2](https://github.com/dmrogger/AcademiaFitnessCenter/assets/86617363/e7abc5d7-3c7d-4c56-a877-04191d17ba8d)

## Problema 
O problema era que era necessário que fosse extraído um relatório dessas lojas parceiras e seus respectivos clientes. 

O relatório deveria conter: CNPJ da loja parceira, CPF do cliente e uma flag informando se dentro da pasta do cliente havia ou não arquivos(de qualquer extensão). OBS: A aplicação deveria varrer também possíveis subpastas dentro da pasta do cliente. 

Inicialmente a ideia era gerar esse relatório em forma de um arquivo .CSV, o que até chegou a ser feito, entretando como não se sabia ao certo a quantidade de clientes dentro das pastas CPNJ's optamos por gravar diretamente em um Banco de dados estas informações

Exemplo de relatório CSV:

![PastaDeRede5](https://github.com/dmrogger/AcademiaFitnessCenter/assets/86617363/4a032e09-5928-45da-9305-a2f1b15d4fb8)

O primeiro Campo seria o CNPJ o segundo o CPF e o terceiro a Flag de arquivo, neste exemplo a pasta CNPJ possuía 3 clientes, sendo um deles com uma pasta vazia.

Como eu disse anteriormente esse modelo de relatório CSV foi abandonado, primeiro por questões de desempenho, pois o processo de percorrer as pastas na rede que já é lento ficava ainda pior com o processo de escrita no arquivo CSV, e segundo por não se saber ao certo quantos clientes cada pasta CNPJ possuía.

## Solução
Essas questões relacionadas a performance da aplicação e a quantidade de dados, levou a inserir as informações diretamente no banco de dados, a estrutura segue a mesma do arquivo CSV, com exeção de um campo "data_relatório" que foi adicionado na gravação em banco, esse processo de registrar em banco tornou o software um pouco mais perfomático, porém acredito que ainda está longe do ideal, mas funciona bem até determinada quantidade de dados. 

Até o momento a a aplicação está trabalhando com 6.300.00 pastas CPF e para concluir a varredura completa leva em torno de 2 dias, rodando em uma máquina convencional (i5 16gb ram). Como a aplicação não "pesa" muito na máquina, ela não impacta no uso da mesma enquanto é executada

## Informações adicionais :)
Primeiramente obrigado por dar uma olhada no projeto, sei que ele está longe de ser perfeito, mas considerando o prazo que eu tinha para o faze-lo e o meu pouco tempo de experiência como programador, acho que ele está ok.

### Performance
Acredito que a aplicação ainda não está 100% perfomática por conta da varredura das pastas, pois ele busca pastas e subpastas, também acredito que eu poderia ter travado a busca por pastas assim que ele localizasse um arquivo ele travesse a busca naquela pasta. Existem também questões de Big O e estrutura de dados que ainda não domino 100% que poderiam tornar a estrutura mais perfomática.

### Bibliotecas utilizadas 
 **OS** Para: Funcionalidades do sistema operacional como escrita em arquivos, percorrer pastas...

 **RE** Para: Expressões regulares famoso Regex, aqui neste projeto foi utilziado para trabalhar com os caminhos de pastas durante a varredura

 **logging** Para: Facilitar o processo de criação de arquivos de log 

 **datetime** Para: Trabalhar com datas e tempo. Foi utilizada no momento de gerar os Logs

 **psycopg2** Para: Estabelecer conexão e trabalhar com banco de dados PostgresSQL


 **win32** 
 **win32con**
 **win32security**
 **win32.win32api**
 **win32.win32security** Para: trabalhar com questões do Windows, no projeto foi utlizada para logar com outro usuário no momento de fazer a busca na pasta de rede
