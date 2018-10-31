<p align="center"><img src="https://user-images.githubusercontent.com/14370340/42978617-5260c1b2-8ba4-11e8-932b-89fe566cd730.png" width="350px"></p>

# Pingout 
App para contagem de pings em uma determinada URL, essa contagem pode ser filtrada e exportada em formato CSV. 

## Objetivo
O Pingout foi concebido para resolver o problema de coleta automatizada de métricas de contagem de deploys contínuos em um determinado período da escolha do usuário.

## Contexto

Observ, projeto de EPS-MDS 2018.1.

![](https://raw.githubusercontent.com/fga-eps-mds/2018.1-TropicalHazards-BI/development/docs/project_artefacts/pipeline_devops/pipeline_DevOps.png)

Gráfico de deploys

![](https://user-images.githubusercontent.com/14370340/46961019-36dd6f00-d076-11e8-8339-723b3b344eba.png)

## Tecnologias

### Flask
![](https://mherman.org/presentations/flask-kubernetes/images/flask-logo.png)

### MongoDB
![](https://zdnet3.cbsistatic.com/hub/i/r/2018/02/16/8abdb3e1-47bc-446e-9871-c4e11a46f680/resize/370xauto/8a68280fd20eebfa7789cdaa6fb5eff1/mongo-db-logo.png)

### Pytest
![](https://cdn-images-1.medium.com/max/1600/1*qmz2bNVJ64273TA4TbFxZw.png)

### Pymongo e Mongomock 
![](https://sahilsehwag.files.wordpress.com/2017/10/mongopython.png?w=300&#038;h=300&#038;crop=1)

## Funcionalidades

1. Criação de um Pingout, cada Pingout recebe um UUID único
```
curl -X POST http://localhost:5000/create-pingout 
```
```json
{
  "uuid": "YOURUNIQUEUUID"
}
```

2. Ping! Ao realizar um ping a data de ocorrência é armazenada
```
curl -X POST http://localhost:5000/YOURUNIQUEUUID/ping 
```

3. Filtragem e exportação. É possível filtrar todos os pings dentro de um período de tempo, para obter informação da contagem de pings em cada dia dentro do período filtrado. O filtro ocorre através de dois parâmetros data inicial(`initial_date`) e data final(`final_date`) no formato **YYYY-MM-DD**. Ao realizar a filtragem os resultados estarão disponíveis em formato CSV.

[http://localhost:5000/YOURUNIQUEUUID/filter/?initial_date=2018-01-01&final_date=2018-02-02]()

4. Obter informação de todos os pings. Para obter a informações de todos os pings de um Pingout basta acessar a página de detalhe de um Ping.

[http://localhost:5000/YOURUNIQUEUUID]()

## [Instalação e uso](installation_usage.md)

## TBL2 F3

Para a fase 3 do TBL 2 será necessário forkar o repositório do Pingout que estará disponível na organização da disciplina.

1. Analizar o código e definir os casos de teste;
2. Implementar os testes;
3. Sugerir melhorias no software de acordo com os bugs ou não conformidades encontradas no código.
4. Realizar um PR para o repositório que se encontra na organização da disciplina
    - Descrever no PR as sugestões de melhoria e casos de teste em que o sistema falha

### Dúvidas durante a implementação?
**Abra uma Issue** no repositório do Pingout na organização da disciplina e me marque, que eu vou tentar responder o mais rápido possível :v:

Se por algum motivo não quiserem abrir a Issue me mandem um mensagem no telegram: **@matheusbss**
