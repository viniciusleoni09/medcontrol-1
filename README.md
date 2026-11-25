
# MedControl — Sistema de Gerenciamento Médico

## Sobre o projeto

O MedControl é um sistema de gerenciamento médico desenvolvido para facilitar a organização de pacientes e consultas de uma clínica.

O sistema permite cadastrar pacientes, consultar informações, agendar consultas e cancelar agendamentos.

## Funcionalidades

- Cadastro de pacientes.
- Listagem de pacientes.
- Pesquisa de pacientes pelo nome.
- Exclusão de pacientes.
- Agendamento de consultas.
- Listagem de consultas.
- Cancelamento de consultas.
- Painel inicial com informações dinâmicas.
- API para consultar pacientes em formato JSON.

## Tecnologias utilizadas

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite

## Estrutura do projeto

```text
MedControl/
│
├── app.py
├── medcontrol.db
├── README.md
│
├── templates/
│   ├── index.html
│   ├── pacientes.html
│   ├── cadastrar.html
│   └── consultas.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js
```

## Como executar o projeto

1. Instale o Python.
2. Instale o Flask:

```bash
pip install flask
```

3. Abra o terminal na pasta do projeto.
4. Execute:

```bash
python app.py
```

5. Abra o navegador e acesse:

```text
http://127.0.0.1:5000
```

## API de pacientes

O sistema possui uma rota para consultar os pacientes cadastrados em formato JSON:

```text
http://127.0.0.1:5000/api/pacientes
```

## Desenvolvedor

Projeto desenvolvido como atividade prática do curso MedTec 2026.
