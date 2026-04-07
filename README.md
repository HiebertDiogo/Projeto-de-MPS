
# Lava Jato – Projeto OOP + Persistência JSON (CLI)

Sistema de linha de comando para um **lava jato**, com:
- **Programação Orientada a Objetos** (classes + pacotes)
- **Cadastro de Usuários e Veículos**
- **Catálogo de Serviços**
- **Ordem de Serviço / Atendimento**
- **Login** com validações (12 chars, não vazio, sem números)
- **Política de senha estilo IAM**
- **Persistência em JSON** (`data/db.json`)
- **Padrões de Design**: Command, Observer, Memento, Strategy, Logger, Factory
- **Geração de Relatórios** (HTML e TXT)

---

## Como rodar

Requisitos: **Python 3.10+**

Na raiz do projeto:

```bash
python main.py
```

O arquivo `data/db.json` é criado automaticamente na primeira execução.

---

## Estrutura do projeto

```
carwash/
  main_carwash.py  # ponto de entrada principal
  commands/        # padrão Command para operações
  logger/          # logging do sistema
  memento/         # padrão Memento para undo de usuários
  models/          # entidades (User, Vehicle, Service, ServiceOrder, Account)
  observer/        # padrão Observer para notificações de ordens
  repositories/    # camada de persistência (JSON DB + repos + Factory para criação de repositórios)
  services/        # regras de negócio (AuthService, CarWashService, validators, reports)
  strategy/        # padrão Strategy para descontos
  ui/              # menu de CLI
data/
  db.json          # "banco" JSON
  reports/         # relatórios gerados (HTML, TXT)
main.py            # launcher
```

---

## Funcionalidades (menu)

1. **Criar conta**
2. **Login**
3. **Cadastrar usuário + veículo** (precisa estar logado)
4. **Cadastrar serviço** (precisa estar logado)
5. **Listar usuários**
6. **Listar serviços**
7. **Criar atendimento (ordem de serviço)** (precisa estar logado)
8. **Listar atendimentos**
9. **Gerar relatório de estatísticas**
10. **Atualizar dados de usuário** [Memento]
11. **Desfazer última atualização de usuário** [Memento]
12. **Configurar desconto para ordens** [Strategy]
13. **Resumo da sessão** [Observer]
14. **Logout**
0. **Sair**

---

## Regras de Login 

Validação do **login**:
- Não pode ser vazio
- Deve ter **exatamente 12 caracteres**
- **Não pode conter números**
- Implementação adotada: **apenas letras (A–Z)**

---

## Política de senha (estilo IAM)

Validação da **senha**:
- Mínimo **10 caracteres**
- Pelo menos:
  - 1 letra **maiúscula**
  - 1 letra **minúscula**
  - 1 **número**
  - 1 **caractere especial** (ex.: `!@#`)
- Não pode conter o login
- Não pode ser uma senha muito comum (denylist pequena)

**Segurança:** a senha não fica em texto puro. É armazenada como **PBKDF2-HMAC-SHA256** + salt no JSON.

---

## Persistência (JSON)

Todos os dados são salvos em `data/db.json` no formato:

```json
{
  "users": [],
  "vehicles": [],
  "services": [],
  "orders": [],
  "accounts": []
}
```

---

## Padrões de Design Implementados

- **Command**: Usado para encapsular operações como criação de usuários, serviços e ordens.
- **Observer**: Notifica mudanças em ordens de serviço.
- **Memento**: Permite desfazer atualizações de dados de usuário.
- **Strategy**: Implementa diferentes estratégias de desconto para ordens.
- **Factory**: Cria instâncias de repositórios de forma centralizada.
- **Logger**: Sistema de logging para registrar operações.

---

## Geração de Relatórios

O sistema permite gerar relatórios de estatísticas em formatos **HTML** e **TXT**, salvos em `data/reports/`.

---

## Observações

- O CPF tem validação **básica** (11 dígitos). Se o professor exigir, dá para implementar validação completa dos dígitos verificadores.
- O sistema foi feito para ser simples e **fácil de defender** na apresentação: UI (menu) separada das regras de negócio e dos repositórios.
- O atendimento só reconhece os veículos vinculados ao usuário que está logado, por isso, se o carro for cadastrado no nome de outro cliente ele não aparece na criação do atendimento
