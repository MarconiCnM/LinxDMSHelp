from flask import Flask, redirect, render_template, url_for, request
from flask_login import login_required

from views.cadastroForms import FormCadGestor, FormCadHelper, FormCadBase, FormCadCargo, FormCadTime, FormCadAnalista
from models.models import GESTOR, HELPER, BASES, CARGO, TIME, ANALISTA
from controllers.cadastroController import gestorCad, helperCad, basesCad, cargoCad, timeCad, analistaCad


def init_app(app: Flask):
    @app.route("/cadastros/analista", methods=['GET', 'POST'])
    @login_required
    def cadastroAnalista():
        analistas = ANALISTA.query.all()
        form_analista = FormCadAnalista()
        analista_cad = analistaCad(form_analista)
        if analista_cad is True:
            return redirect(url_for('cadastroAnalista'))
        return render_template('main/cadastros/analista.html', form_analista=form_analista, analistas=analistas)
    
    @app.route("/cadastros/analista/<analista_id>", methods=['GET', 'POST'])
    @login_required
    def cadastroAnalistaID(analista_id):
        analistaID = ANALISTA.query.get(analista_id)
        form_analista = FormCadAnalista()
        if analistaID and request.method == "GET":
            form_analista.nome.data = analistaID.USUARIO
            form_analista.email.data = analistaID.EMAIL
            form_analista.cargo.data = analistaID.grupo.CARGO
            form_analista.time.data = analistaID.time.NOME
        analistas = ANALISTA.query.all()
        analista_cad = analistaCad(form_analista)
        if analista_cad is True:
            return redirect(url_for('cadastroAnalista'))
        return render_template('main/cadastros/analista.html', form_analista=form_analista, analistas=analistas, analistaID=analistaID)


    @app.route("/cadastros/bases", methods=['GET', 'POST'])
    @login_required
    def cadastroBases():
        bases = BASES.query.all()
        form_bases = FormCadBase()
        base_cad = basesCad(form_bases)
        if base_cad is True:
            return redirect(url_for('cadastroBases'))
        return render_template('main/cadastros/bases.html', form_bases=form_bases, bases=bases)

    @app.route("/cadastros/bases/<base_id>", methods=['GET', 'POST'])
    @login_required
    def cadastroBasesID(base_id):
        baseID = BASES.query.get(base_id)
        form_bases = FormCadBase()
        if baseID and request.method == "GET":
                form_bases.codigo.data = baseID.CODIGO
                form_bases.cliente.data = baseID.CLIENTE
                form_bases.servidor.data = baseID.SERVIDOR
                form_bases.estrutura.data = baseID.ESTRUTURA
                form_bases.instancia.data = baseID.INSTANCIA
                form_bases.usuario.data = baseID.USUARIO
                form_bases.marca.data = baseID.MARCA
                form_bases.tamanho.data = baseID.TAMANHO
        bases = BASES.query.all()
        base_cad = basesCad(form_bases)
        if base_cad is True:
            return redirect(url_for('cadastroBases'))
        return render_template('main/cadastros/bases.html', form_bases=form_bases, bases=bases, baseID=baseID)


    @app.route("/cadastros/cargo", methods=['GET', 'POST'])
    @login_required
    def cadastroCargo():
        cargos = CARGO.query.all()
        form_cargo = FormCadCargo()
        cargo_cad = cargoCad(form_cargo)
        if cargo_cad is True:
            return redirect(url_for('cadastroCargo'))
        return render_template('main/cadastros/cargo.html', form_cargo=form_cargo, cargos=cargos)
    
    @app.route("/cadastros/cargo/<cargo_id>", methods=['GET', 'POST'])
    @login_required
    def cadastroCargoID(cargo_id):
        cargoID = CARGO.query.get(cargo_id)
        form_cargo = FormCadCargo()
        if cargoID and request.method == "GET":
                form_cargo.codigo.data = cargoID.CODIGO
                form_cargo.cargo.data = cargoID.CARGO
                form_cargo.metas.data = cargoID.META
        cargos = CARGO.query.all()
        cargo_cad = cargoCad(form_cargo)
        if cargo_cad is True:
            return redirect(url_for('cadastroCargo'))
        return render_template('main/cadastros/cargo.html', form_cargo=form_cargo, cargos=cargos, cargoID=cargoID)

    @app.route("/cadastros/gestor", methods=['GET', 'POST'])
    @login_required
    def cadastroGestor():
        gestores = GESTOR.query.all()
        form_gestor = FormCadGestor()
        gestor_cad = gestorCad(form_gestor)
        if gestor_cad is True:
            return redirect(url_for('cadastroGestor'))
        return render_template('main/cadastros/gestor.html', form_gestor=form_gestor, gestores=gestores)
    
    @app.route("/cadastros/gestor/<gestor_id>", methods=['GET', 'POST'])
    @login_required
    def cadastroGestorID(gestor_id):
        gestorID = GESTOR.query.get(gestor_id)
        form_gestor = FormCadGestor()
        if gestorID and request.method == "GET":
            form_gestor.nome.data = gestorID.USUARIO
            form_gestor.email.data = gestorID.EMAIL
        gestores = GESTOR.query.all()
        gestor_cad = gestorCad(form_gestor)
        if gestor_cad is True:
            return redirect(url_for('cadastroGestor'))
        return render_template('main/cadastros/gestor.html', form_gestor=form_gestor, gestores=gestores, gestorID=gestorID)

    @app.route("/cadastros/helper", methods=['GET', 'POST'])
    @login_required
    def cadastroHelper():
        helpers = HELPER.query.all()
        form_helper = FormCadHelper()
        helper_cad = helperCad(form_helper)
        if helper_cad is True:
            return redirect(url_for('cadastroHelper'))
        return render_template('main/cadastros/helper.html', form_helper=form_helper, helpers=helpers)
    
    @app.route("/cadastros/helper/<helper_id>", methods=['GET', 'POST'])
    @login_required
    def cadastroHelperID(helper_id):
        helperID = HELPER.query.get(helper_id)
        form_helper = FormCadHelper()
        if helperID and request.method == "GET":
            form_helper.nome.data = helperID.USUARIO
            form_helper.email.data = helperID.EMAIL
        helpers = HELPER.query.all()
        helper_cad = helperCad(form_helper)
        if helper_cad is True:
            return redirect(url_for('cadastroHelper'))
        return render_template('main/cadastros/helper.html', form_helper=form_helper, helpers=helpers, helperID=helperID)

    @app.route("/cadastros/time", methods=['GET', 'POST'])
    @login_required
    def cadastroTime():
        times = TIME.query.all()
        form_time = FormCadTime()
        time_cad = timeCad(form_time)
        if time_cad is True:
            return redirect(url_for('cadastroTime'))
        return render_template('main/cadastros/time.html', form_time=form_time, times=times)

    @app.route("/cadastros/time/<time_id>", methods=['GET', 'POST'])
    @login_required
    def cadastroTimeID(time_id):
        timeID = TIME.query.get(time_id)
        form_time = FormCadTime()
        if timeID and request.method == "GET":
            form_time.codigo.data = timeID.CODIGO
            form_time.nome.data = timeID.NOME
            form_time.helper.data = timeID.HELP.USUARIO
            form_time.gestor.data = timeID.GESTAO.USUARIO
        times = TIME.query.all()
        time_cad = timeCad(form_time)
        if time_cad is True:
            return redirect(url_for('cadastroTime'))
        return render_template('main/cadastros/time.html', form_time=form_time, times=times, timeID=timeID)
