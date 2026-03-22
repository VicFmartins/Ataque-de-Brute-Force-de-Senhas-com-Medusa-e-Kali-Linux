# Checklist de Hardening de Autenticação

## Controles de Acesso

- Exigir MFA para contas administrativas
- Bloquear contas após excesso de falhas com janela controlada
- Implementar backoff progressivo por IP e usuário

## Políticas de Senha

- Incentivar senhas longas em vez de apenas complexidade superficial
- Bloquear senhas conhecidamente comprometidas
- Remover contas padrão ou credenciais iniciais não alteradas

## Detecção

- Alertar para múltiplas falhas do mesmo IP
- Alertar para muitas contas testadas pelo mesmo IP
- Correlacionar sucesso após sequência de falhas
- Enriquecer eventos com origem, ASN e contexto

## Resposta

- Isolar origem suspeita quando aplicável
- Redefinir credenciais afetadas
- Revisar se houve reutilização de senha
- Preservar logs para análise posterior
