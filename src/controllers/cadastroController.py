from flask import request, flash
from flask_login import current_user

from models.models import GESTOR, HELPER, BASES, CARGO, TIME, ANALISTA
from app import database, bcrypt


def gestorCad(form_gestor):
    if form_gestor.validate_on_submit() and 'btn_submit_salvar' in request.form:
        gestor = GESTOR.query.filter_by(
            EMAIL=form_gestor.email.data).first()
        
        if form_gestor.senha.data:
            if (current_user.EMAIL == gestor.EMAIL) or (current_user.TIPO == 'G'):
                gestor.USUARIO = form_gestor.nome.data
                gestor.EMAIL = form_gestor.email.data
                gestor.SENHA = bcrypt.generate_password_hash(
                    form_gestor.senha.data)
                database.session.commit()
                flash('Perfil atualizado com sucesso', 'alert-success')
                return True
            else: 
                flash(
                    'Você não tem permissão para fazer essa alteração', 'alert-danger')      
        else:
            flash(
                'Favor preencher a senha', 'alert-danger')    
 

    elif form_gestor.validate_on_submit() and 'btn_submit_inserir' in request.form:
        gestor = GESTOR.query.filter_by(
            EMAIL=form_gestor.email.data).first()

        if gestor:
            flash(
                'Já existe cadastro com esse E-mail', 'alert-danger')
        else:
            password_cript = bcrypt.generate_password_hash(
                form_gestor.senha.data)
            gestor = GESTOR(USUARIO=form_gestor.nome.data, EMAIL=form_gestor.email.data, SENHA=password_cript)
            database.session.add(gestor)
            database.session.commit()
            flash('Cadastro feito com sucesso', 'alert-success')
        return True
    elif form_gestor.validate_on_submit() and 'btn_submit_excluir' in request.form:
        gestor = GESTOR.query.filter_by(
            EMAIL=form_gestor.email.data).first()
        
        valida_time = TIME.query.filter_by(GESTOR_ID=gestor.id).first()
        if valida_time:
            flash(f'Gestor não pode ser excluido, pois o time {valida_time.NOME} está vinculado a ele', 'alert-danger')
        else:
            database.session.delete(gestor)
            database.session.commit()
            flash('Cadastro excluido com sucesso', 'alert-success')
            return True
    elif form_gestor.validate_on_submit() and 'btn_submit_redirect' in request.form:
        return True


def helperCad(form_helper):
    if form_helper.validate_on_submit() and 'btn_submit_salvar' in request.form:
        helper = HELPER.query.filter_by(
            EMAIL=form_helper.email.data).first()

        if form_helper.senha.data:
            if (current_user.EMAIL == helper.EMAIL) or (current_user.TIPO == 'G'):
                helper.USUARIO = form_helper.nome.data
                helper.EMAIL = form_helper.email.data
                helper.SENHA = bcrypt.generate_password_hash(
                    form_helper.senha.data)
                database.session.commit()
                flash('Perfil atualizado com sucesso', 'alert-success')
                return True
            else: 
                flash(
                    'Você não tem permissão para fazer essa alteração', 'alert-danger')       
        else:
            flash(
                'Favor preencher a senha', 'alert-danger')    

    elif form_helper.validate_on_submit() and 'btn_submit_inserir' in request.form:
        helper = HELPER.query.filter_by(
            EMAIL=form_helper.email.data).first()

        if helper:
            flash(
                'Já existe cadastro com esse E-mail', 'alert-danger')
        else:
            password_cript = bcrypt.generate_password_hash(
                form_helper.senha.data)
            helper = HELPER(USUARIO=form_helper.nome.data, EMAIL=form_helper.email.data, SENHA=password_cript)
            database.session.add(helper)
            database.session.commit()
            flash('Cadastro feito com sucesso', 'alert-success')
        return True
    elif form_helper.validate_on_submit() and 'btn_submit_excluir' in request.form:
        helper = HELPER.query.filter_by(
            EMAIL=form_helper.email.data).first()
        
        valida_time = TIME.query.filter_by(HELPER_ID=helper.id).first()
        if valida_time:
            flash(f'Helper não pode ser excluido, pois o time {valida_time.NOME} está vinculado a ele', 'alert-danger')
        else:
            database.session.delete(helper)
            database.session.commit()
            flash('Cadastro excluido com sucesso', 'alert-success')
            return True
    elif form_helper.validate_on_submit() and 'btn_submit_redirect' in request.form:
        return True

def basesCad(form_bases):
    if form_bases.validate_on_submit() and 'btn_submit_salvar' in request.form:
        base = BASES.query.filter_by(
            CODIGO=form_bases.codigo.data).first()
        
        if form_bases.estrutura.data == 'Oracle': 
            if form_bases.instancia.data is '':
                flash('O Campo instancia é obrigatorio para Oracle', 'alert-danger')
            elif form_bases.usuario.data is '':
                flash('O Campo usuario é obrigatorio para Oracle', 'alert-danger')
            else: 
                base.CLIENTE = form_bases.cliente.data
                base.SERVIDOR = form_bases.servidor.data
                base.ESTRUTURA = form_bases.estrutura.data
                base.INSTANCIA = form_bases.instancia.data
                base.USUARIO = form_bases.usuario.data
                base.MARCA = form_bases.marca.data
                base.TAMANHO = form_bases.tamanho.data
                database.session.commit()
                flash('Registro atualizado com sucesso', 'alert-success')
                return True 
        elif form_bases.estrutura.data == 'SQLServer':
                base.CLIENTE = form_bases.cliente.data
                base.SERVIDOR = form_bases.servidor.data
                base.ESTRUTURA = form_bases.estrutura.data
                base.INSTANCIA = form_bases.instancia.data
                base.USUARIO = form_bases.usuario.data
                base.MARCA = form_bases.marca.data
                base.TAMANHO = form_bases.tamanho.data
                database.session.commit()
                flash('Registro atualizado com sucesso', 'alert-success')
                return True 

    elif form_bases.validate_on_submit() and 'btn_submit_inserir' in request.form:
        base = BASES.query.filter_by(
            CODIGO=form_bases.codigo.data).first()

        if base:
            flash(
                'Já existe cadastro com esse código', 'alert-danger')
        else:
            if form_bases.estrutura.data == 'Oracle': 
                if form_bases.instancia.data is '':
                    flash('O Campo instancia é obrigatorio para Oracle', 'alert-danger')
                elif form_bases.usuario.data is '':
                    flash('O Campo usuario é obrigatorio para Oracle', 'alert-danger')
                else: 
                    base = BASES(CODIGO=form_bases.codigo.data, 
                        CLIENTE=form_bases.cliente.data, 
                        SERVIDOR=form_bases.servidor.data, 
                        ESTRUTURA=form_bases.estrutura.data, 
                        INSTANCIA=form_bases.instancia.data, 
                        USUARIO=form_bases.usuario.data, 
                        MARCA=form_bases.marca.data, 
                        TAMANHO=form_bases.tamanho.data)
                    database.session.add(base)
                    database.session.commit()
                    flash('Registro adicionado com sucesso', 'alert-success')
            elif form_bases.estrutura.data == 'SQLServer':
                if form_bases.instancia.data is None:
                    form_bases.instancia.data = ''
                elif form_bases.usuario.data is None:
                    form_bases.usuario.data = ''
                else: 
                    base = BASES(CODIGO=form_bases.codigo.data, 
                        CLIENTE=form_bases.cliente.data, 
                        SERVIDOR=form_bases.servidor.data, 
                        ESTRUTURA=form_bases.estrutura.data, 
                        INSTANCIA=form_bases.instancia.data, 
                        USUARIO=form_bases.usuario.data, 
                        MARCA=form_bases.marca.data, 
                        TAMANHO=form_bases.tamanho.data)
                    database.session.add(base)
                    database.session.commit()
                    flash('Registro adicionado com sucesso', 'alert-success')
        return True

    elif form_bases.validate_on_submit() and 'btn_submit_excluir' in request.form:
        base = BASES.query.filter_by(
            CODIGO=form_bases.codigo.data).first()
        
        database.session.delete(base)
        database.session.commit()
        flash('Registro excluido com sucesso', 'alert-success')
        return True

    elif form_bases.validate_on_submit() and 'btn_submit_redirect' in request.form:
        return True

def cargoCad(form_cargo):
    if form_cargo.validate_on_submit() and 'btn_submit_salvar' in request.form:
        cargo = CARGO.query.filter_by(
            CODIGO=form_cargo.codigo.data).first()

        cargo.CODIGO = form_cargo.codigo.data
        cargo.CARGO = form_cargo.cargo.data
        cargo.META = form_cargo.metas.data
        database.session.commit()
        flash('Registro atualizado com sucesso', 'alert-success')
        return True
   
    elif form_cargo.validate_on_submit() and 'btn_submit_inserir' in request.form:
        cargo = CARGO.query.filter_by(
            CODIGO=form_cargo.codigo.data).first()

        if cargo:
            flash(
                'Já existe um registro com esse codigo', 'alert-danger')
        else:
            cargo = CARGO(CODIGO=form_cargo.codigo.data, CARGO=form_cargo.cargo.data, META=form_cargo.metas.data)
            database.session.add(cargo)
            database.session.commit()
            flash('Registro feito com sucesso', 'alert-success')
        return True
    elif form_cargo.validate_on_submit() and 'btn_submit_excluir' in request.form:
        cargo = CARGO.query.filter_by(
            CODIGO=form_cargo.codigo.data).first()
        
        database.session.delete(cargo)
        database.session.commit()
        flash('Registro excluido com sucesso', 'alert-success')
        return True
    elif form_cargo.validate_on_submit() and 'btn_submit_redirect' in request.form:
        return True


def timeCad(form_time):
    if form_time.validate_on_submit() and 'btn_submit_salvar' in request.form:
        time = TIME.query.filter_by(
            CODIGO=form_time.codigo.data).first()
        helper = HELPER.query.filter_by(USUARIO=form_time.helper.data).first()
        gestor = GESTOR.query.filter_by(USUARIO=form_time.gestor.data).first()
        time.CODIGO = form_time.codigo.data
        time.NOME = form_time.nome.data
        time.HELPER_ID = helper.id
        time.GESTOR_ID = gestor.id
        database.session.commit()
        flash('Registro atualizado com sucesso', 'alert-success')
        return True
   
    elif form_time.validate_on_submit() and 'btn_submit_inserir' in request.form:
        time = TIME.query.filter_by(
            CODIGO=form_time.codigo.data).first()

        if time:
            flash(
                'Já existe um registro com esse codigo', 'alert-danger')
        else:
            helper = HELPER.query.filter_by(USUARIO=form_time.helper.data).first()
            gestor = GESTOR.query.filter_by(USUARIO=form_time.gestor.data).first()
            time = TIME(CODIGO=form_time.codigo.data, NOME=form_time.nome.data, HELPER_ID=helper.id, GESTOR_ID=gestor.id)
            database.session.add(time)
            database.session.commit()
            flash('Registro feito com sucesso', 'alert-success')
        return True
    elif form_time.validate_on_submit() and 'btn_submit_excluir' in request.form:
        time = TIME.query.filter_by(
            CODIGO=form_time.codigo.data).first()
    
        database.session.delete(time)
        database.session.commit()
        flash('Registro excluido com sucesso', 'alert-success')
        return True
    elif form_time.validate_on_submit() and 'btn_submit_redirect' in request.form:
        return True


def analistaCad(form_analista):
    if form_analista.validate_on_submit() and 'btn_submit_salvar' in request.form:
        analista = ANALISTA.query.filter_by(
            EMAIL=form_analista.email.data).first()
        
        if (current_user.EMAIL == analista.EMAIL) or (current_user.TIPO == 'G') or (current_user.TIPO == 'H'):
            cargo = CARGO.query.filter_by(CARGO=form_analista.cargo.data).first()
            time = TIME.query.filter_by(NOME=form_analista.time.data).first()
            analista.USUARIO = form_analista.nome.data
            analista.EMAIL = form_analista.email.data   
            if form_analista.senha.data:    
                analista.SENHA = bcrypt.generate_password_hash(
                    form_analista.senha.data)
            analista.CARGO_ID = cargo.id
            analista.TIME_ID = time.id
            database.session.commit()
            flash('Perfil atualizado com sucesso', 'alert-success')
            return True
 

    elif form_analista.validate_on_submit() and 'btn_submit_inserir' in request.form:
        analista = ANALISTA.query.filter_by(
            EMAIL=form_analista.email.data).first()

        if analista:
            flash(
                'Já existe cadastro com esse E-mail', 'alert-danger')
        else:
            cargo = CARGO.query.filter_by(CARGO=form_analista.cargo.data).first()
            time = TIME.query.filter_by(NOME=form_analista.time.data).first()
            password_cript = bcrypt.generate_password_hash(
                form_analista.senha.data)
            analista = ANALISTA(USUARIO=form_analista.nome.data, EMAIL=form_analista.email.data, SENHA=password_cript, CARGO_ID=cargo.id, TIME_ID=time.id)
            database.session.add(analista)
            database.session.commit()
            flash('Cadastro feito com sucesso', 'alert-success')
            return True
    elif form_analista.validate_on_submit() and 'btn_submit_excluir' in request.form:
        analista = ANALISTA.query.filter_by(
            EMAIL=form_analista.email.data).first()
        
        database.session.delete(analista)
        database.session.commit()
        flash('Cadastro excluido com sucesso', 'alert-success')
        return True
    elif form_analista.validate_on_submit() and 'btn_submit_redirect' in request.form:
        return True