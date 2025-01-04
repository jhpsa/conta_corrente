# Gerenciador de conta corrente
- main.py: implementação do gerenciador de conta corrente
- cadastros.json: base de dados dos correntistas cadastrados e suas informações (obs: a única forma de um correntista ser VIP é alterando seu atributo VIP para true nesse arquivo)
- movimentacoes.json: base de dados com as informações de todas as movimentações realizadas entre contas de correntistas
## Projeto baseado em um desafio detalhado a seguir:
### Identificação/Login do correntista 

entradas: conta corrente (5 dígitos) e senha (4 dígitos)
  
Haverá pelo menos 2 correntistas "cadastrados". Pelo menos um correntista terá o perfil "Normal" e o outro terá o perfil "VIP".

### Opções

  1. Ver Saldo
  2. Extrato
  3. Saque
  4. Depósito
  5. Transferencia
  6. Solicitar visita do gerente 
  7. Trocar de usuário

### Saldo
Apenas o valor atualizado em R$.

### Extrato
O extrato exibirá data, hora, descrição e valor (entre parênteses quando negativo) de cada movimentação.

### Saque
O usuário Normal não pode sacar além do valor em saldo. O VIP pode, mas terá seu saldo reduzido em 0.1% por minuto até que sejam feitos depósitos suficientes para cobrir o saldo negativo.

### Transferências
Cada usuário poderá realizar transferências informando o valor e a conta corrente do destinatário (não pode transferir para si mesmo nem para conta inexistente).
- As transferências aparecerão nos extratos tanto do cedente quanto do sacado.
- O usuário Normal poderá fazer transferências de até R$1000,00. O VIP não terá limite. 
- O usuário Normal será debitado em R$8,00 por transferência e o VIP em 0,8% do valor transferido. Deverão ser destacados esses débitos no extrato.

### Visita do gerente
Apenas o usuário VIP pode ver a opção "Solicitar visita do gerente". Esta opção precisa ser confirmada pelo usuário e, após a confirmação, apenas debita R$50,00 da conta do usuário.

### Trocar de usuário
Deve ser possível sair da conta de usuario e entrar em outro para verificar as movimentações.
