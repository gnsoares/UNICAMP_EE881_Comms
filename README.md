# Transmissor digital EE881
----

### Criação do ambiente virtual

`virtualenv env`

`source env/bin/activate`

`pip install -r requirements.txt`

### Transmitindo uma mensagem

`python main.py`

E digita a mensagem a ser transmitida. Ou:

`python main.py < file.txt`

### Alterando a variância do AWGN

`python main.py --var {{variance}}`

### Teste de porcentagem de erro

`python test.py {{tamanho da mensagem (em caracteres)}} {{repeticoes}}`

