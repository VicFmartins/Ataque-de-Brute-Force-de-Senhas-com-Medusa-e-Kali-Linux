# Laboratório Defensivo de Detecção de Brute Force em Autenticação

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Foco](https://img.shields.io/badge/foco-blue%20team-2e8b57)
![Status](https://img.shields.io/badge/status-lab%20seguro-0a7ea4)

Projeto educacional voltado para análise, detecção e mitigação de tentativas de brute force e password spraying em ambiente controlado, sem instruções operacionais de ataque e sem automação ofensiva.

## Visão Geral

O repositório foi reposicionado para um uso seguro e defensivo. Em vez de documentar execução de brute force com ferramentas ofensivas, ele agora serve como laboratório para:

- gerar logs sintéticos de autenticação;
- detectar padrões compatíveis com brute force e password spraying;
- treinar análise inicial de incidentes;
- praticar hardening de autenticação e resposta.

## O Que Este Projeto Faz

- Gera eventos fictícios de autenticação bem-sucedida e falha
- Resume suspeitas por IP, usuário e janela de tempo
- Sinaliza padrões compatíveis com brute force simples
- Sinaliza padrões compatíveis com password spraying
- Documenta boas práticas de defesa

## O Que Este Projeto Não Faz

- não executa tentativas reais de login;
- não usa Medusa, Hydra ou ferramentas equivalentes;
- não testa credenciais contra serviços reais;
- não automatiza enumeração, spraying ou brute force.

## Estrutura do Repositório

```text
.
├── README.md
├── requirements.txt
├── lab/
│   └── mock_auth_log_generator.py
├── defense/
│   ├── brute_force_detector.py
│   └── auth_hardening_checklist.md
└── samples/
    └── auth_events.json
```

## Casos de Uso

- aulas introdutórias de segurança defensiva;
- exercícios de SOC e blue team;
- portfólio com foco em análise de autenticação;
- tabletop de resposta a incidentes;
- estudo de padrões de brute force e spraying.

## Como Executar

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Ataque-de-Brute-Force-de-Senhas-com-Medusa-e-Kali-Linux
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux ou macOS:

```bash
source .venv/bin/activate
```

### 4. Instale dependências

```bash
pip install -r requirements.txt
```

### 5. Gere logs sintéticos

```bash
python lab/mock_auth_log_generator.py
```

### 6. Analise os eventos

```bash
python defense/brute_force_detector.py samples/auth_events.json
```

## Exemplo de Saída

```text
Resumo de autenticacao
- Total de eventos: 14
- IPs com alta taxa de falha: 2
- Usuarios alvo de spraying: 3
- Possiveis brute force simples: 1
- Possiveis password spraying: 1
```

## Componentes

### `lab/mock_auth_log_generator.py`

Cria um conjunto seguro de eventos sintéticos de autenticação para treinamento.

### `defense/brute_force_detector.py`

Analisa o dataset e procura padrões simples como:

- muitas falhas do mesmo IP contra um mesmo usuário;
- muitas falhas do mesmo IP contra vários usuários;
- sucesso após sequência de falhas;
- concentração de falhas por janela curta.

### `defense/auth_hardening_checklist.md`

Checklist prático de endurecimento de autenticação para estudo e uso em laboratório.

## Boas Práticas Reforçadas

- MFA para contas críticas;
- rate limiting e backoff progressivo;
- bloqueio temporário inteligente;
- monitoramento por IP, ASN e geolocalização;
- logs centralizados e correlação de eventos;
- senha forte e proteção contra credenciais vazadas.

## Próximos Passos

- adicionar exportação CSV;
- incluir regras Sigma defensivas;
- gerar relatórios HTML;
- adicionar testes automatizados;
- ampliar cenários de detecção com risco/score.

## Nota Ética

Este projeto foi ajustado para permanecer em uma linha segura e defensiva. O objetivo é apoiar o aprendizado de detecção e resposta sem facilitar ataques contra autenticação.
