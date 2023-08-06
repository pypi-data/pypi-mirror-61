# dgipy

Ferramenta para facilitar o acesso aos dados disponibilizados pelo DGI/INPE.

## Instalação

dgipy pode ser instalado em sistemas operacionais Linux, Windows e MacOS com versões do Python 3.6+. Para tal, o seguinte comando pode ser utilizado

```{shell}
pip install dgi
```

## Exemplo de utilização

A utilização do dgipy é dividida em três partes, estas apresentadas abaixo:

* (i) População do banco de dados

A primeira etapa necessária para a utilização do dgipy é a população do banco de dados em que o dgipy vai consumir, com todas as imagens disponíveis no DGI/INPE.

Para esta etapa é possível definir diferentes regiões e datas de busca. O exemplo de código abaixo recupera imagens geradas pelo CBERS-4, de todo o território brasileiro para o intervalo de datas de 01/01/2019 até 25/01/2019

```{python}
from dgi.catalogo import CatalogoDGI

data_de_busca = {"inicial": "01/01/2019", "final": "25/01/2019"}
localizacoes = {
    "norte": "11.04024846",
    "sul": "-36.49917303",
    "leste": "-30.77297895",
    "oeste": "-74.80618208"
}

catalogo = CatalogoDGI()
catalogo.lista_imagens_dgi_regiao("CB4", "", data_de_busca, localizacoes)
```

* (ii) Consumo dos serviços do DGI/INPE

Com o banco de dados populado, o dgipy consegue realizar buscas das imagens que foram registradas no banco e também fazer pedidos no catálogo.

O código abaixo busca todas as imagens que possuem data entre os dias 01/01/2019 e 01/02/2019 e realiza o pedido dessas no catálogo

```{python}
from dgi.acesso import BuscaDeImagemNoCatalogo, FacilitaDGI

facilita_dgi = FacilitaDGI("SEU_USUARIO_DO_CATALOGO", "SUA_SENHA_DO_CATALOGO")
catalogo_de_imagens_local = BuscaDeImagemNoCatalogo()

# Fazendo a busca
imagens = catalogo_de_imagens_local.busca_imagens_por_data("01/01/2019", "01/02/2019")

# Realizando o pedido com as imagens encontradas
informacoes_do_pedido = facilita_dgi.realiza_pedido(imagens)
```

* (iii) Download das imagens

Com o pedido realizado, você receberá um link, onde estarão todas as imagens disponíveis para o *download*, para esta etapa o dgipy pode te ajudar com o *download*.

Para tal, basta pegar o link que o DGI/INPE te enviou e inserir no código abaixo.

```{python}
from dgi.acesso import BuscaDeImagemNoCatalogo, FacilitaDGI

facilita_dgi = FacilitaDGI("SEU_USUARIO_DO_CATALOGO", "SUA_SENHA_DO_CATALOGO")
imagens_ja_baixadas = facilita_dgi.baixa_imagens_de_link_do_pedido(
    "LINK_DO_PEDIDO", "LOCAL_ONDE_SERA_SALVO")
```

> Note que para a execução dos exemplos apresentados acima, é assumido que existe uma instância do MongoDB rodando em sua máquina. Para detalhes mais completos sobre toda a configuração do ambiente necessário para utilizar o dgipy, consulte a documentação do projeto.

## Documentação

Para aprender mais sobre o dgipy e suas possibilidades de utilização, consulte a documentação do projeto.
