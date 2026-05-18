# 💙 Sempre Perto

> Um espaço de acolhimento emocional entre mães e filhos.

Projeto desenvolvido para o **Hackathon de Dia das Mães do Servidor dos Programadores**, com o objetivo de fortalecer a comunicação, o acolhimento emocional e a conexão familiar através de check-ins emocionais e mensagens de apoio.

---

## ✨ Sobre o projeto

O **Sempre Perto** foi criado para aproximar mães e filhos emocionalmente, mesmo à distância.

A proposta é simples: a mãe pode registrar diariamente como está se sentindo, enquanto o filho acompanha seu estado emocional e pode enviar mensagens de apoio e carinho.

A plataforma cria um ambiente de cuidado, escuta e fortalecimento dos vínculos familiares.

---

## 🚀 Funcionalidades

### 👩 Dashboard da mãe
- Registro de **check-in emocional diário**
- Seleção de emoções
- Visualização de mensagens recebidas dos filhos
- Envio de mensagens para filhos conectados
- Código familiar exclusivo
- Exclusão de conta

### 🧑 Dashboard do filho
- Visualização do estado emocional atual da mãe
- Recebimento de mensagens da mãe
- Envio de mensagens de apoio
- Histórico limitado de mensagens
- Exclusão de conta

### 🔐 Sistema de autenticação
- Cadastro de mãe e filho(a)
- Login com validação de tipo de usuário
- Conexão familiar via **código de família**
- Sessão de usuário com Flask

---

## 🛠️ Tecnologias utilizadas

### Back-end
- **Python**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLite**

### Front-end
- **HTML5**
- **CSS3**
- **Jinja2**
- **JavaScript**

### Arquitetura
- Estrutura inspirada em **MVC**
- Templates dinâmicos com Flask/Jinja

---

## 🧠 Emoções disponíveis

- 😄 Feliz  
- 😊 Bem  
- 😥 Triste  
- 😟 Ansiosa  
- 😫 Sobrecarregada  
- 💔 Saudade

Cada emoção possui uma **cor personalizada**, facilitando a visualização do estado emocional.

---

## 📂 Estrutura do projeto

```txt
Hackaton Dia das Mães/
│
├── main.py
├── views.py
├── db.py
├── requirements.txt
│
├── models/
│   ├── users.py
│   ├── messages.py
│   └── checkins.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/
│   ├── auth/
│   └── dashboard/
│
└── README.md