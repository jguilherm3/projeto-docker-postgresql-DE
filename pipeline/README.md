Data Engineering Pipeline: Lakehouse & Orquestração

Este repositório documenta a construção de um ecossistema de Engenharia de Dados completo, integrando automação de arquivos não estruturados (PDFs), ingestão de dados estruturados (NY Taxi Data) e orquestração de pipelines via Docker e Apache Airflow.

# Sobre o Projeto

O projeto aborda dois desafios principais do mundo real da engenharia de dados:

Data Cleaning & Organization (Unstructured): Automação e normalização de nomenclatura de arquivos brutos (Provas de Vestibular) utilizando Regex avançado para detecção de anos, semestres (2025.1 vs 24.2) e tipos de prova (Medicina, Verão/Inverno).

Data Ingestion & Orchestration (Structured): Construção de um Data Warehouse local usando PostgreSQL e Docker, com pipelines de ingestão orquestrados e conteinerizados, replicando uma arquitetura de produção (ETL do NY Taxi Dataset).

# Arquitetura e Tecnologias

O ambiente foi totalmente conteinerizado para garantir reprodutibilidade.

Linguagem: Python 3.10+ (Pandas, SQLAlchemy, Regex).

Gerenciador de Pacotes: uv (para alta performance) e pip.

Containerização: Docker e Docker Compose.

Orquestração: Apache Airflow (Executando via Docker em localhost:8080).

Banco de Dados: PostgreSQL 16.

Interface DB: pgAdmin4 e pgcli (via terminal).

##  Funcionalidades Detalhadas

1. Organizador Inteligente de Vestibulares

Script Python capaz de varrer diretórios "sujos", identificar padrões complexos em nomes de arquivos PDF e movê-los para uma estrutura de Lakehouse organizada.

Lógica de Regex: Tratamento de anos abreviados (24.2 -> 2024 e SEM2).

Regras de Negócio: Classificação automática de "Verão/Inverno" baseada no semestre.

Prevenção de Colisão: Renomeação automática de arquivos duplicados.

2. Pipeline de Ingestão (Dockerized)

Scripts de ingestão de dados massivos (Batch) que rodam dentro da rede Docker.

Desafio Superado: Configuração de rede Docker (bridge network) permitindo que scripts Python em containers isolados se comuniquem com o Banco de Dados.

Otimização: Uso de chunksize no Pandas para processamento eficiente de memória.

## Como Executar

Pré-requisitos

Docker Desktop instalado e rodando (WSL 2 no Windows).

Git Bash (recomendado) ou PowerShell.

Passo 1: Subir a Infraestrutura

Na raiz do projeto, inicie os serviços (Postgres, pgAdmin, Airflow):

docker-compose up -d


Passo 2: Ingestão de Dados (Exemplo NY Taxi)

Para rodar o script de ingestão isolado na mesma rede do banco:

# Nota: Substitua 'pgdatabase' pelo nome do seu serviço no docker-compose
docker run -it \
    --network=pipeline_default \
    taxi_ingest:v001 \
        --pg-user=root \
        --pg-pass=root \
        --pg-host=pgdatabase \
        --pg-port=5432 \
        --pg-db=nytaxi \
        --target-table=yellow_taxi_trips


Passo 3: Acessar o Airflow

Acesse http://localhost:8080 (User/Pass: airflow).
Os arquivos DAG devem ser colocados na pasta ./dags mapeada localmente.

🔧 Solução de Problemas Comuns (Troubleshooting)

Durante o desenvolvimento, diversos desafios de infraestrutura foram mapeados e resolvidos:

1. Erro: Connection Refused em localhost

Causa: Tentar conectar ao banco usando localhost de dentro de um container Docker.

Solução: Em ambientes Docker, localhost refere-se ao próprio container. A conexão deve ser feita usando o nome do serviço (DNS interno), ex: --host=pgdatabase.

2. Erro: ImportError: no pq wrapper available (pgcli)

Causa: Falta da biblioteca libpq-dev no sistema ou instalação pura do psycopg.

Solução: Utilização do pacote binário pré-compilado:

uv add --dev psycopg-binary


3. Sintaxe PowerShell vs Bash

Problema: O caractere \ de quebra de linha do Linux não funciona nativamente no PowerShell.

Solução: Utilizar acento grave ` no Windows ou rodar o comando em linha única.

## Estrutura do Projeto

.
├── dags/                   # DAGs do Airflow (ETL Orchestration)
├── scripts/                # Scripts Python (Organizador de PDFs, Ingestão)
├── docker-compose.yaml     # Definição da Infraestrutura
├── Dockerfile              # Imagem customizada para scripts de ingestão
├── .env                    # Variáveis de ambiente (AIRFLOW_UID)
└── README.md


## Autor

Guilherme Martins
Engenheiro de Dados em formação, focado em resolver problemas complexos de infraestrutura e manipulação de dados.

