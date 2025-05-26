from flask import url_for, render_template
from flask_mail import Mail, Message

mail = Mail()

detalle_reserva_url = "http://localhost:4200/detalle-reserva"

def init_mail(app):
    mail.init_app(app)


def send_reserva_creada_inquilino(reserva):
    logo_url = url_for('static', filename='img/laTrinidadAzulChico.png', _external=True)

    html_body = render_template(
        'reserva_creada_inquilino.html',
        user_name=reserva.inquilino.nombre,
        propiedad_nombre=reserva.propiedad.nombre,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
        logo_url=logo_url,
        cta_url=f"{detalle_reserva_url}/{reserva.id}",
        cta_text="Ver mi reserva",
        current_year=2025,
    )

    text_body = render_template(
        'reserva_creada_inquilino.txt',
        user_name=reserva.inquilino.nombre,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
        cta_url=f"{detalle_reserva_url}/{reserva.id}",
        current_year=2025,
    )

    msg = Message(
        subject="¡Tu reserva está confirmada!",
        recipients=[reserva.inquilino.correo],
        body=text_body,
        html=html_body
    )

    mail.send(msg)


def send_reserva_creada_encargado(reserva):
    logo_url = url_for('static', filename='img/laTrinidadAzulChico.png', _external=True)

    html_body = render_template(
        'reserva_creada_encargado.html',
        user_name=reserva.propiedad.encargado.nombre,
        propiedad_nombre=reserva.propiedad.nombre,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
        logo_url=logo_url,
        cta_url=f"{detalle_reserva_url}/{reserva.id}",
        cta_text="Ver reserva",
        current_year=2025,
    )

    text_body = render_template(
        'reserva_creada_encargado.txt',
        user_name=reserva.propiedad.encargado.nombre,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
        cta_url=f"{detalle_reserva_url}/{reserva.id}",
        current_year=2025,
    )

    msg = Message(
        subject="¡Nueva reserva!",
        recipients=[reserva.propiedad.encargado.correo],
        body=text_body,
        html=html_body
    )

    mail.send(msg)


def send_reserva_cancelada(reserva, sender):
    logo_url = url_for('static', filename='img/laTrinidadAzulChico.png', _external=True)
    if sender.get_roles()['is_inquilino']:
        template_html = 'reserva_cancelada_encargado.html'
        template_txt = 'reserva_cancelada_encargado.txt'
        recipient = reserva.propiedad.encargado.correo
    else:
        template_html = 'reserva_cancelada_inquilino.html'
        template_txt = 'reserva_cancelada_inquilino.txt'
        recipient = reserva.inquilino.correo

    html_body = render_template(
        template_html,
        reserva_id=reserva.id,
        propiedad_nombre=reserva.propiedad.nombre,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
        logo_url=logo_url,
        cta_url=f"{detalle_reserva_url}/{reserva.id}",
        cta_text="Ver reserva",
        current_year=2025,
    )

    text_body = render_template(
        template_txt,
        reserva_id=reserva.id,
        propiedad_nombre=reserva.propiedad.nombre,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
        cta_url=f"{detalle_reserva_url}/{reserva.id}",
        current_year=2025,
    )

    msg = Message(
        subject="¡La reserva fue cancelada!",
        recipients=[recipient],
        body=text_body,
        html=html_body
    )

    mail.send(msg)
