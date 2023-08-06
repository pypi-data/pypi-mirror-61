# dgi

Ferramenta para facilitar o acesso aos dados disponibilizados pelo DGI/INPE.

## Instalação

```{shell}
pip install dgi
```

## Exemplo de utilização

```{python}
from dgi.acesso import BuscaDeImagemNoCatalogo, FacilitaDGI

facilita_dgi = FacilitaDGI("SEU_USUARIO_DO_CATALOGO", "SUA_SENHA_DO_CATALOGO")
catalogo_de_imagens_local = BuscaDeImagemNoCatalogo()

# Fazendo a busca
imagens = catalogo_de_imagens_local.busca_imagens_por_data("01/01/2019", "01/02/2019")

# Realizando o pedido com as imagens encontradas
informacoes_do_pedido = facilita_dgi.realiza_pedido(imagens)
```

## Funcionalidades

## Documentação

Para gerar a documentação, será necessário instalar o `sphinxs` e executar o comando abaixo

```shell
sphinx-build -b html docs docs-compilado
```
