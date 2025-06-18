from flask import render_template, current_app
from flask_mail import Mail, Message
from threading import Thread

mail = Mail()

def init_mail(app):
    mail.init_app(app)


def run_async_with_context(func, *args, **kwargs):
    """Ejecuta una función en un hilo nuevo con el contexto de la app Flask."""
    app = current_app._get_current_object()
    def wrapper():
        with app.app_context():
            func(*args, **kwargs)
    Thread(target=wrapper).start()

def send_reserva_confirmada(data_email, reserva_url, logo_url):
    html_body = render_template(
        'reserva_confirmada.html',
        inquilino_nombre=data_email['inquilino_nombre'],
        propiedad_nombre=data_email['propiedad_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        monto_pagado=data_email['monto_pagado'],
        logo_url=logo_url,
        cta_url=reserva_url,
        cta_text="Ver mi reserva",
        current_year=2025,
    )
    text_body = render_template(
        'reserva_confirmada.txt',
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
def send_reserva_creada_inquilino(data_email, reserva_url, logo_url):
    html_body = render_template(
        'reserva_creada_inquilino.html',
        inquilino_nombre=data_email['inquilino_nombre'],
        propiedad_nombre=data_email['propiedad_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        monto_pagado=data_email['monto_pagado'],
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
        monto_pagado=data_email['monto_pagado'],
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
        monto_pagado=data_email['monto_pagado'],
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


def send_reset_password(logo_url, reset_password_url, user_email):
    html_body = render_template(
        'solicitud_reset_password.html',
        logo_url=logo_url,
        cta_url=reset_password_url,
        cta_text="Ver reserva",
        current_year=2025,
    )

    text_body = render_template(
        'solicitud_reset_password.txt',
        cta_url=reset_password_url,
        current_year=2025,
    )

    msg = Message(
        subject="Recuperación de contraseña",
        recipients=[user_email],
        body=text_body,
        html=html_body
    )
    mail.send(msg)

def send_mensaje_chat(data_email, reserva_url, logo_url, message, rol):
    if rol == 3:
        from src.models.users.logica import get_correos_administradores
        recipients = [data_email['correo_encargado']]
        recipients.extend(get_correos_administradores())
    else:
        recipients = [data_email['correo_inquilino']]
    html_body = render_template(
        'mensaje_chat.html',
        reserva_id=data_email['id'],
        propiedad_nombre=data_email['propiedad_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        logo_url=logo_url,
        cta_url=reserva_url,
        cta_text="Ver reserva",
        current_year=2025,
        mensaje=message
    )
    text_body = render_template(
        'mensaje_chat.txt',
        reserva_id=data_email['id'],
        propiedad_nombre=data_email['propiedad_nombre'],
        fecha_inicio=data_email['fecha_inicio'],
        fecha_fin=data_email['fecha_fin'],
        cta_url=reserva_url,
        current_year=2025,
        mensaje=message
    )
    msg = Message(
        subject="Nuevo mensaje en tu reserva",
        recipients=recipients,
        body=text_body,
        html=html_body
    )
    mail.send(msg)
