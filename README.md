# Sistema de Empacotamento Inteligente

Sistema web para simulação e otimização de empacotamento de produtos, com recomendação automática de caixas e interface interativa em tempo real.

## 🚀 Funcionalidades

- Geração automática de pedidos para simulação
- Recomendação inteligente de caixas baseada nas dimensões dos produtos
- Interface em tempo real com WebSocket
- Visualização do processo de empacotamento
- Estatísticas detalhadas do processamento
- Sistema de aprovação/rejeição de recomendações

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.8+
- Flask (Framework Web)
- Flask-SocketIO (WebSocket)
- SimPy (Simulação)
- Flask-CORS (Gerenciamento CORS)

### Frontend
- Vue.js 2
- Socket.IO Client
- Bootstrap 5
- Font Awesome

## 🚦 Como Executar

### Backend

1. Instale as dependências:
```sh
 cd backend
 pip install -r requirements.txt
```

2. Inicie o servidor:
```sh
python app.py
```
O servidor será iniciado em `http://localhost:5001`


### Frontend

1. Instale um servidor local:
   ```sh
   # Usando Python 3
   python -m http.server 8000
```

2. Acesse o sistema em seu navegador:
   - Abra `http://localhost:8000/frontend`
   - Navegadores recomendados: Chrome, Firefox ou Edge

## Uso

1. Ao abrir a interface, clique em "Novo Lote de Pedidos" para gerar pedidos para simulação
2. Para cada pedido:
   - Visualize o produto e a caixa recomendada
   - Aceite (✓) ou rejeite (✗) a recomendação
3. Acompanhe as estatísticas em tempo real na barra inferior
4. Ao final do lote, visualize as estatísticas completas
