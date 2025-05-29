from flask import render_template
from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    mail.init_app(app)


def send_reserva_creada_inquilino(data_email, reserva_url, logo_url):
    html_body = render_template(
        'reserva_creada_inquilino.html',
        inquilino_nombre=data_email['inquilino_nombre'],
        propiedad_nombre=data_email['propiedad_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        logo_url=logo_url,
        cta_url=reserva_url,
        cta_text="Ver mi reserva",
        current_year=2025,
    )

    text_body = render_template(
        'reserva_creada_inquilino.txt',
        inquilino_nombre=data_email['inquilino_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        cta_url=reserva_url,
        current_year=2025,
    )

    msg = Message(
        subject="¡Tu reserva está confirmada!",
        recipients=[data_email['correo_inquilino']],
        body=text_body,
        html=html_body
    )

    mail.send(msg)


def send_reserva_creada_encargado(data_email, reserva_url, logo_url):
    html_body = render_template(
        'reserva_creada_encargado.html',
        encargado_nombre=data_email['encargado_nombre'],
        propiedad_nombre=data_email['propiedad_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        logo_url=logo_url,
        cta_url=reserva_url,
        cta_text="Ver reserva",
        current_year=2025,
    )

    text_body = render_template(
        'reserva_creada_encargado.txt',
        encargado_nombre=data_email['encargado_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        cta_url=reserva_url,
        current_year=2025,
    )

    msg = Message(
        subject="¡Nueva reserva!",
        recipients=[data_email['correo_encargado']],
        body=text_body,
        html=html_body
    )

    mail.send(msg)


def send_reserva_cancelada(data_email, reserva_url, logo_url, from_inquilino):
    if from_inquilino:
        template_html = 'reserva_cancelada_encargado.html'
        template_txt = 'reserva_cancelada_encargado.txt'
        recipient = data_email['correo_encargado']
    else:
        template_html = 'reserva_cancelada_inquilino.html'
        template_txt = 'reserva_cancelada_inquilino.txt'
        recipient = data_email['correo_inquilino']

    html_body = render_template(
        template_html,
        reserva_id=data_email['id'],
        propiedad_nombre=data_email['propiedad_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        logo_url=logo_url,
        cta_url=reserva_url,
        cta_text="Ver reserva",
        current_year=2025,
    )

    text_body = render_template(
        template_txt,
        reserva_id=data_email['id'],
        propiedad_nombre=data_email['propiedad_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        cta_url=reserva_url,
        current_year=2025,
    )

    msg = Message(
        subject="¡La reserva fue cancelada!",
        recipients=[recipient],
        body=text_body,
        html=html_body
    )

    mail.send(msg)
