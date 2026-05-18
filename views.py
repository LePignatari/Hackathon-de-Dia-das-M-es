from main import app
from flask import render_template, request, session, redirect, url_for, flash
from models.users import User
from models.messages import Message
from models.checkins import Checkin
from db import db
import random
import string

@app.route('/')
def homepage():
    return render_template('homepage.html')

# Rota de registro
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        fam_code = request.form.get('fam_code')

        existing_user = User.query.filter_by(email=email).first()

        # se já tiver cadastro
        if existing_user:
            flash('Já existe um usuário cadastrado com este email.', 'warning')
            return redirect(url_for('signup'))
        
        # se não tiver selecionado o tipo de usuário
        if not user_type:
            flash('Selecione o tipo de usuário', 'warning')
            return redirect(url_for('signup'))
        
        # gera código se for mãe | se for filho pede código
        if user_type == 'mae':
            fam_code = 'FAM-' + ''.join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=4
                )
            )
        elif user_type == 'filho':
            if not fam_code:
                flash('Informe o código da família.', 'warning')
                return redirect(url_for('signup'))
            
            family = User.query.filter_by(fam_code=fam_code).first()

            if not family:
                flash('Nenhuma família com este código foi encontrada.', 'error')
                return redirect(url_for('signup'))

        user = User(
            name=name,
            email=email,
            password=password,
            user_type=user_type,
            fam_code=fam_code
        )

        db.session.add(user)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('signin'))

    return render_template('auth/signup.html')

# Rota de login
@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form.get('user_type')
        fam_code = request.form.get('fam_code')

        user = User.query.filter_by(email=email).first()

        # se não tiver cadastro
        if not user:
            flash('Usuário não encontrado', 'error')
            return redirect(url_for('signin'))

        # senha errada
        if user.password != password:
            flash('Senha incorreta!', 'error')
            return redirect(url_for('signin'))
        
        # sem tipo = filho ou mãe
        if user_type == None:
            flash('Informe o tipo de usuário.', 'warning')
            return redirect(url_for('signin'))
    
        # se selecionou o tipo de usuário errado
        if user.user_type != user_type:
            flash('Tipo de usuário incorreto!', 'error')
            return redirect(url_for('signin'))

        # valida o código se for tipo = filho
        if user.user_type == 'filho':
            if user.fam_code != fam_code:
                flash('Código incorreto!', 'error')
                return redirect(url_for('signin'))
            
        session['user_id'] = user.id 

        if user.user_type == 'mae':
            return redirect(url_for('dashboard_mae'))
        
        return redirect(url_for('dashboard_filho'))
    
    return render_template('auth/signin.html')

@app.route('/dashboard-mae', methods=['GET','POST'])
def dashboard_mae():
    user_id = session.get('user_id')

    # sem login
    if not user_id:
        flash('Faça login antes de acessar qualquer dashboard!', 'warning')
        return redirect(url_for('signin'))

    user = User.query.get(user_id)

    # usuário não encontrado
    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('signin'))

    # se não for mãe | proteção da rota
    if user.user_type != 'mae':
        flash('Ops...Acesso negado.', 'error')
        return redirect(url_for('signin'))
    
    # mostra as últimas 3 mensagens recebidas
    received_messages = Message.query.filter_by(
        receiver_id=user_id
    ).order_by(Message.id.desc()).limit(3).all()
    
    if request.method == 'POST':
        emotion = request.form.get('emotion')
        message = request.form.get('message')

        if emotion:
            checkin = Checkin(
                emotion=emotion,
                user_id=user.id
            )
            db.session.add(checkin)

        if message and message.strip():
            children = User.query.filter_by(
                fam_code=user.fam_code, 
                user_type='filho').all()

            for child in children:
                msg = Message(
                    content=message,
                    sender_id=user.id,
                    receiver_id=child.id
                )
                db.session.add(msg)
            
        db.session.commit()

        flash('Dados enviados com sucesso!', 'success')
        return redirect(url_for('dashboard_mae'))

    return render_template(
        'dashboard/dashboard-mae.html',
        user=user,
        received_messages=received_messages
        )

@app.route('/dashboard-filho', methods=['GET','POST'])
def dashboard_filho():
    user_id = session.get('user_id')

    # sem login
    if not user_id:
        flash('Faça login antes de acessar qualquer dashboard!', 'warning')
        return redirect(url_for('signin'))
    
    user = User.query.get(user_id)

    # se não for filho | proteção da rota
    if user.user_type != 'filho':
        flash('Ops...Acesso negado.', 'error')
        return redirect(url_for('signin'))
    
    # encontra a mãe pelo fam_code
    mother = User.query.filter_by(
        fam_code=user.fam_code,
        user_type='mae'
    ).first()

    last_checkin = None

    # Vai pegar o último registro feito no check-in da mãe
    if mother:
        last_checkin = Checkin.query.filter_by(
            user_id=mother.id
        ).order_by(Checkin.id.desc()).first()

    if not mother:
            flash('Código da família não encontrado.', 'error')
            return redirect(url_for('signin'))
    
    # pega 3 últimas mensagens enviadas pela mãe
    mother_message = Message.query.filter_by(
        receiver_id=user.id,
        sender_id=mother.id
    ).order_by(Message.id.desc()).limit(3).all()

    if request.method == 'POST':
        message = request.form.get('message')

        if message and message.strip():
            msg = Message(
                content=message,
                sender_id=user.id,
                receiver_id=mother.id,
            )

            db.session.add(msg)
            db.session.commit()
            flash('Dados enviados com sucesso!', 'success')  

      
    return render_template(
        'dashboard/dashboard-filho.html',
        user=user,
        receiver=mother,
        last_checkin=last_checkin,
        mother_message=mother_message
        )

@app.route('/logout')
def logout():
    session.clear()

    flash('Logout realizado.', 'success')
    return redirect(url_for('homepage'))

# DELETE
@app.route('/delete-account')
def delete_account():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('signin'))
    
    user = User.query.get(user_id)

    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('signin'))

    # se a mãe excluir a conta exclui toda a família
    if user.user_type == 'mae':
        children = User.query.filter_by(
            fam_code=user.fam_code,
            user_type='filho'
        ).all()

        # apaga mensagens
        for child in children:
            Message.query.filter(
                (Message.receiver_id==child.id) | (Message.sender_id==child.id)
            ).delete()

            # apaga checkins
            Checkin.query.filter_by(user_id=child.id).delete()

            db.session.delete(child)

    # excluindo usuário
    Message.query.filter(
        (Message.receiver_id==user_id) | (Message.sender_id==user_id)
    ).delete()

   
    Checkin.query.filter_by(user_id=user_id).delete()

    db.session.delete(user)
    db.session.commit()

    session.clear()

    flash('Conta excluida com sucesso!', 'success')
    return render_template('homepage.html')