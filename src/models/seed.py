from src.models import users, propiedades, parametricas, reservas
from src.models.users.user import Tarjeta
from datetime import datetime, date


def run():
    # Roles
    administrador = parametricas.create_rol("Administrador")
    encargado = parametricas.create_rol("Encargado")
    inquilino = parametricas.create_rol("Inquilino")

    # Tipos de identificación
    dni = parametricas.create_tipo_identificacion("DNI")
    pasaporte = parametricas.create_tipo_identificacion("Pasaporte")
    cedula = parametricas.create_tipo_identificacion("Cédula")

    # Tipos de propiedades
    dpto = parametricas.create_tipos_propiedad("Departamento")
    cabana = parametricas.create_tipos_propiedad("Cabaña")
    casa = parametricas.create_tipos_propiedad("Casa")
    casa_de_campo = parametricas.create_tipos_propiedad("Casa de Campo") # O "Finca", "Chacra" en algunos contextos (ej. Argentina)
    casa_en_la_playa = parametricas.create_tipos_propiedad("Casa en la Playa") # O "Casa de Veraneo"
    chalet = parametricas.create_tipos_propiedad("Chalet") # Común en zonas de montaña o residenciales
    cabaña = parametricas.create_tipos_propiedad("Cabania")
    estudio = parametricas.create_tipos_propiedad("Estudio") # Un solo ambiente con dormitorio, sala y cocina integrados
    loft = parametricas.create_tipos_propiedad("Loft") # Espacio abierto, a menudo industrial-chic, con techos altos y a veces entrepiso
    duplex = parametricas.create_tipos_propiedad("Dúplex") # Dos unidades de vivienda en un mismo edificio, a menudo una encima de la otra o adosadas
    condominio = parametricas.create_tipos_propiedad("Condominio") # Una unidad de propiedad individual dentro de un complejo grande (ej. con áreas comunes)

    # Porcentajes del primer pago
    cero = parametricas.create_pol_reserva(
        "Seña del 0% del valor de la estadía", 0)
    veinte = parametricas.create_pol_reserva(
        "Seña del 20% del valor de la estadía", 0.2)
    cien = parametricas.create_pol_reserva(
        "Seña del 100% del valor de la estadía", 1)

    # Paises de ejemplo
    pais_arg = parametricas.create_pais("Argentina")
    pais_uru = parametricas.create_pais("Uruguay")
    pais_chi = parametricas.create_pais("Chile")
    pais_bra = parametricas.create_pais("Brasil")
    pais_col = parametricas.create_pais("Colombia")
    pais_mex = parametricas.create_pais("México")
    pais_per = parametricas.create_pais("Perú")
    pais_ecu = parametricas.create_pais("Ecuador")
    pais_bol = parametricas.create_pais("Bolivia")
    pais_par = parametricas.create_pais("Paraguay")
    pais_ven = parametricas.create_pais("Venezuela")
    pais_esp = parametricas.create_pais("España")
    pais_fra = parametricas.create_pais("Francia")
    pais_ita = parametricas.create_pais("Italia")
    pais_ale = parametricas.create_pais("Alemania")
    pais_rei = parametricas.create_pais("Reino Unido")
    pais_por = parametricas.create_pais("Portugal")
    pais_sui = parametricas.create_pais("Suiza")
    pais_aus = parametricas.create_pais("Austria")
    pais_hol = parametricas.create_pais("Países Bajos")
    pais_bel = parametricas.create_pais("Bélgica")
    pais_sue = parametricas.create_pais("Suecia")
    pais_nor = parametricas.create_pais("Noruega")
    pais_din = parametricas.create_pais("Dinamarca")
    pais_fin = parametricas.create_pais("Finlandia")
    pais_iru = parametricas.create_pais("Irlanda")
    pais_gre = parametricas.create_pais("Grecia")
    pais_tur = parametricas.create_pais("Turquía")
    pais_can = parametricas.create_pais("Canadá")
    pais_usa = parametricas.create_pais("Estados Unidos")
    pais_aus_nz = parametricas.create_pais("Australia")
    pais_nue = parametricas.create_pais("Nueva Zelanda")
    pais_jap = parametricas.create_pais("Japón")
    pais_cor = parametricas.create_pais("Corea del Sur")
    pais_chi_rp = parametricas.create_pais("China")
    pais_ind = parametricas.create_pais("India")
    pais_sud = parametricas.create_pais("Sudáfrica")
    pais_egp = parametricas.create_pais("Egipto")
    pais_mar = parametricas.create_pais("Marruecos")
    pais_tun = parametricas.create_pais("Túnez")
    pais_isr = parametricas.create_pais("Israel")
    pais_arab = parametricas.create_pais("Arabia Saudita")
    pais_emir = parametricas.create_pais("Emiratos Árabes Unidos")
    pais_qtr = parametricas.create_pais("Qatar")
    pais_pan = parametricas.create_pais("Panamá")
    pais_cos = parametricas.create_pais("Costa Rica")
    pais_gua = parametricas.create_pais("Guatemala")
    pais_hon = parametricas.create_pais("Honduras")
    pais_nic = parametricas.create_pais("Nicaragua")
    pais_els = parametricas.create_pais("El Salvador")
    pais_cub = parametricas.create_pais("Cuba")
    pais_rdo = parametricas.create_pais("República Dominicana")
    pais_pue = parametricas.create_pais("Puerto Rico") # Aunque es territorio de EE. UU., se lista a menudo
    pais_jam = parametricas.create_pais("Jamaica")
    pais_bah = parametricas.create_pais("Bahamas")
    pais_tri = parametricas.create_pais("Trinidad y Tobago")
    pais_bar = parametricas.create_pais("Barbados")
    pais_isl = parametricas.create_pais("Islandia")
    pais_pol = parametricas.create_pais("Polonia")
    pais_che = parametricas.create_pais("República Checa")
    pais_hun = parametricas.create_pais("Hungría")
    pais_cro = parametricas.create_pais("Croacia")
    pais_esl = parametricas.create_pais("Eslovenia")
    pais_ser = parametricas.create_pais("Serbia")
    pais_bul = parametricas.create_pais("Bulgaria")
    pais_rum = parametricas.create_pais("Rumania")
    pais_ucr = parametricas.create_pais("Ucrania")
    pais_rus = parametricas.create_pais("Rusia")
    pais_vie = parametricas.create_pais("Vietnam")
    pais_tai = parametricas.create_pais("Tailandia")
    pais_mal = parametricas.create_pais("Malasia")
    pais_sin = parametricas.create_pais("Singapur")
    pais_fil = parametricas.create_pais("Filipinas")
    pais_ind_one = parametricas.create_pais("Indonesia")
    pais_mal_a = parametricas.create_pais("Malta")
    pais_lux = parametricas.create_pais("Luxemburgo")
    pais_mon = parametricas.create_pais("Mónaco")
    pais_san = parametricas.create_pais("San Marino")
    pais_and = parametricas.create_pais("Andorra")
    pais_est = parametricas.create_pais("Estonia")
    pais_let = parametricas.create_pais("Letonia")
    pais_lit = parametricas.create_pais("Lituania")
    pais_esl_a = parametricas.create_pais("Eslovaquia")
    pais_bos = parametricas.create_pais("Bosnia y Herzegovina")
    pais_mon_ne = parametricas.create_pais("Montenegro")
    pais_mac = parametricas.create_pais("Macedonia del Norte")
    pais_alb = parametricas.create_pais("Albania")
    pais_chi_ch = parametricas.create_pais("Chipre")
    pais_geo = parametricas.create_pais("Georgia")
    pais_aze = parametricas.create_pais("Azerbaiyán")
    pais_arm = parametricas.create_pais("Armenia")
    pais_kaz = parametricas.create_pais("Kazajistán")
    pais_uzb = parametricas.create_pais("Uzbekistán")
    pais_nep = parametricas.create_pais("Nepal")
    pais_sri = parametricas.create_pais("Sri Lanka")
    pais_ban = parametricas.create_pais("Bangladés")
    pais_pak = parametricas.create_pais("Pakistán")
    pais_ira = parametricas.create_pais("Irán")
    pais_iraq = parametricas.create_pais("Irak")
    pais_sir = parametricas.create_pais("Siria")
    pais_leb = parametricas.create_pais("Líbano")

    print("Paises creados con exito")


    passwordAll = "Grupo12!"
    # Usuarios de ejemplo con múltiples roles y tipo de identificación
    user1 = users.create_usuario(
        nombre="Juan",
        apellido="Pérez",
        correo="juan@mail.com",
        roles_ids=[administrador.id],
        password=passwordAll,
        id_tipo_identificacion=dni.id,
        numero_identificacion="12345678",
        id_pais=pais_arg.id,
        fecha_nacimiento="1990-01-01"
    )
    user2 = users.create_usuario(
        nombre="Franco",
        apellido="Rodriguez",
        correo="francogrch@gmail.com",
        roles_ids=[encargado.id],
        password=passwordAll,
        id_tipo_identificacion=pasaporte.id,
        numero_identificacion="A1234567",
        id_pais=pais_uru.id,
        fecha_nacimiento="1985-05-10"
    )
    user3 = users.create_usuario(
        nombre="Roberto",
        apellido="López",
        correo="roberto@mail.com",
        roles_ids=[inquilino.id],
        password=passwordAll,
        id_tipo_identificacion=cedula.id,
        numero_identificacion="87654321",
        id_pais=pais_chi.id,
        fecha_nacimiento="2000-12-31"
    )
    print("Usuarios y tipos de identificación de ejemplo creados")

    # Usuarios adicionales empleados
    user4 = users.create_usuario(
        nombre="Emilia",
        apellido="Martínez",
        correo="emilia@mail.com",
        roles_ids=[encargado.id],
        password=passwordAll,
        id_tipo_identificacion=dni.id,
        numero_identificacion="23456789",
        id_pais=pais_arg.id,
        fecha_nacimiento="1992-03-15"
    )
    user5 = users.create_usuario(
        nombre="Sofía",
        apellido="Fernández",
        correo="sofia@mail.com",
        roles_ids=[encargado.id],
        password=passwordAll,
        id_tipo_identificacion=cedula.id,
        numero_identificacion="34567890",
        id_pais=pais_uru.id,
        fecha_nacimiento="1988-07-22"
    )
    # Usuarios adicionales inquilinos
    user6 = users.create_usuario(
        nombre="Lucía",
        apellido="García",
        correo="lucia@mail.com",
        roles_ids=[inquilino.id],
        password=passwordAll,
        id_tipo_identificacion=pasaporte.id,
        numero_identificacion="B9876543",
        id_pais=pais_chi.id,
        fecha_nacimiento="1995-11-30"
    )
    user7 = users.create_usuario(
        nombre="Martín",
        apellido="Suárez",
        correo="martin@mail.com",
        roles_ids=[inquilino.id],
        password=passwordAll,
        id_tipo_identificacion=dni.id,
        numero_identificacion="45678901",
        id_pais=pais_arg.id,
        fecha_nacimiento="1998-04-18"
    )
    user8 = users.create_usuario(
        nombre="Emilia",
        apellido="SinReservas",
        correo="noreservas@mail.com",
        roles_ids=[encargado.id],
        password=passwordAll,
        id_tipo_identificacion=dni.id,
        numero_identificacion="1244788",
        id_pais=pais_arg.id,
        fecha_nacimiento="1998-04-18"
    )
    print("Usuarios empleados e inquilinos adicionales creados")

    # Paramétricas de tarjetas
    from src.models.users.user import MarcaTarjeta, TipoTarjeta
    from src.models.database import db
    visa = MarcaTarjeta(nombre="Visa")
    mastercard = MarcaTarjeta(nombre="Mastercard")
    amex = MarcaTarjeta(nombre="Amex")
    credito = TipoTarjeta(nombre="crédito")
    debito = TipoTarjeta(nombre="débito")
    db.session.add_all([visa, mastercard, amex, credito, debito])
    db.session.commit()

    # Tarjetas de ejemplo solo para usuarios inquilinos
    tarjeta1 = Tarjeta(
        numero="4111111111111111",
        nombre_titular="Juan Pérez",
        fecha_inicio="01/2022",
        fecha_vencimiento="01/2026",
        cvv="123",
        usuario_id=user1.id,
        id_marca=visa.id,
        id_tipo=credito.id
    )
    tarjeta2 = Tarjeta(
        numero="5500000000000004",
        nombre_titular="Juan Pérez",
        fecha_inicio="05/2023",
        fecha_vencimiento="05/2027",
        cvv="456",
        usuario_id=user1.id,
        id_marca=mastercard.id,
        id_tipo=debito.id
    )
    tarjeta3 = Tarjeta(
        numero="4000000000000002",
        nombre_titular="Raul Gómez",
        fecha_inicio="06/2021",
        fecha_vencimiento="06/2025",
        cvv="789",
        usuario_id=user2.id,
        id_marca=visa.id,
        id_tipo=debito.id
    )
    tarjeta4 = Tarjeta(
        numero="340000000000009",
        nombre_titular="Roberto López",
        fecha_inicio="09/2022",
        fecha_vencimiento="09/2026",
        cvv="321",
        usuario_id=user3.id,
        id_marca=amex.id,
        id_tipo=credito.id
    )
    db.session.add_all([tarjeta1, tarjeta2, tarjeta3, tarjeta4])
    db.session.commit()
    print("Tarjetas de ejemplo creadas y asociadas a usuarios inquilinos")

    # Tarjetas para los nuevos inquilinos
    tarjeta5 = Tarjeta(
        numero="6011000000000004",
        nombre_titular="Lucía García",
        fecha_inicio="02/2023",
        fecha_vencimiento="02/2025",
        cvv="654",
        usuario_id=user6.id,
        id_marca=visa.id,
        id_tipo=credito.id
    )
    tarjeta6 = Tarjeta(
        numero="3530111333300000",
        nombre_titular="Martín Suárez",
        fecha_inicio="01/2024",
        fecha_vencimiento="01/2028",
        cvv="852",
        usuario_id=user7.id,
        id_marca=mastercard.id,
        id_tipo=debito.id
    )
    db.session.add_all([tarjeta5, tarjeta6])
    db.session.commit()
    print("Tarjetas de ejemplo creadas y asociadas a nuevos usuarios inquilinos")

    # Relacionar tarjetas solo con usuarios que sean inquilinos
    user1.tarjetas.extend([tarjeta1, tarjeta2])
    user2.tarjetas.append(tarjeta3)
    user3.tarjetas.append(tarjeta4)
    user6.tarjetas.append(tarjeta5)
    user7.tarjetas.append(tarjeta6)
    db.session.add_all([user1, user2, user3, user6, user7, user4, user5,user8])
    db.session.commit()
    print("Tarjetas asociadas a usuarios inquilinos en la relación uno-a-muchos.")

    # Propiedades de ejemplo
    prop1 = propiedades.create_propiedad(
        nombre="Casa de Playa",
        descripcion="Hermosa casa frente al mar",
        entre_calles="Calle A y Calle B",
        calle="Calle del Mar",
        numero="123",
        piso="1",
        depto="A",
        huespedes=6,
        ambientes=4,
        banios=2,
        cocheras=1,
        precioNoche=150.0,
        codigoAcceso="1234",
        is_habilitada=True,
        id_pol_reserva=1,
        id_tipo=dpto.id,
        id_ciudad=1,
        id_encargado=1,
        requiere_documentacion=False
    )

    prop2 = propiedades.create_propiedad(
        nombre="Departamento Centrico",
        descripcion="Cómodo departamento en el centro",
        entre_calles="Av. Principal y Calle 9",
        calle="Calle Central",
        numero="456",
        piso="2",
        depto="B",
        huespedes=3,
        ambientes=2,
        banios=1,
        cocheras=0,
        precioNoche=75.0,
        codigoAcceso="1234",
        is_habilitada=True,
        id_pol_reserva=1,
        id_tipo=dpto.id,
        id_ciudad=2,
        id_encargado=2,
        requiere_documentacion=False
    )

    prop3 = propiedades.create_propiedad(
        nombre="Cabaña en el bosque",
        descripcion="Acogedora cabaña rodeada de naturaleza",
        entre_calles="Camino viejo y Ruta 5",
        calle="Sendero Verde",
        numero="789",
        piso="PB",
        depto="Único",
        huespedes=4,
        ambientes=3,
        banios=1,
        cocheras=2,
        precioNoche=120.0,
        codigoAcceso="1234",
        is_habilitada=True,
        id_pol_reserva=2,
        id_tipo=cabana.id,
        id_ciudad=3,
        id_encargado=2,
        requiere_documentacion=False
    )
    # --- Ejemplos de Departamentos ---
    prop4 = propiedades.create_propiedad(
        nombre="Departamento Moderno en Microcentro",
        descripcion="Acogedor departamento con balcón, ideal para viajes de negocios o turismo, a pasos del Obelisco.",
        calle="Av. Corrientes",
        numero="1234",
        piso="5",
        depto="A",
        entre_calles="9 de Julio y Lavalle",
        id_ciudad=1, # Reemplaza con un ID de ciudad válido
        id_tipo=dpto.id,
        huespedes=3,
        ambientes=2,
        banios=1,
        cocheras=0,
        precioNoche=50.00,
        codigoAcceso="1001", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=1,
        id_encargado=1,
        requiere_documentacion=False
    )

    prop5 = propiedades.create_propiedad(
        nombre="Departamento con estilo en Palermo Soho",
        descripcion="Luminoso y espacioso, cerca de restaurantes y tiendas de diseño. Ideal para parejas o grupos pequeños.",
        calle="Gorriti",
        numero="5678",
        piso="3",
        depto="B",
        entre_calles="Malabia y Armenia",
        id_ciudad=1, # Reemplaza con un ID de ciudad válido
        id_tipo=dpto.id,
        huespedes=4,
        ambientes=3,
        banios=1,
        cocheras=0,
        precioNoche=75.00,
        codigoAcceso="1001", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=1,
        id_encargado=2,
        requiere_documentacion=False
    )

    # --- Ejemplos de Casas ---
    prop6 = propiedades.create_propiedad(
        nombre="Casa Familiar con Jardín en Belgrano",
        descripcion="Amplia casa con 3 habitaciones, patio y parrilla. Perfecta para familias que buscan tranquilidad.",
        calle="Conesa",
        numero="3000",
        piso=None,
        depto=None,
        entre_calles="Juramento y Echeverría",
        id_ciudad=1, # Reemplaza con un ID de ciudad válido
        id_tipo=casa.id,
        huespedes=6,
        ambientes=5,
        banios=2,
        cocheras=1,
        precioNoche=120.00,
        codigoAcceso="2201", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=2,
        id_encargado=1,
        requiere_documentacion=False
    )

    prop7 = propiedades.create_propiedad(
        nombre="Espléndida Casa de Lujo en Nordelta",
        descripcion="Diseño moderno, piscina climatizada y vistas a la laguna. Una experiencia de confort inigualable.",
        calle="Los Sauces",
        numero="100",
        piso=None,
        depto=None,
        entre_calles="El Golf y El Agua",
        id_ciudad=2, # Reemplaza con un ID de ciudad válida (ej. Tigre)
        id_tipo=casa.id,
        huespedes=8,
        ambientes=7,
        banios=3.5,
        cocheras=2,
        precioNoche=300.00,
        codigoAcceso="0202", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=2,
        id_encargado=2,
        requiere_documentacion=False
    )

    # --- Ejemplos de Casas de Campo ---
    prop8 = propiedades.create_propiedad(
        nombre="Casona Colonial en las Sierras de Córdoba",
        descripcion="Paz y naturaleza en una estancia histórica. Ideal para escapadas rurales y desconexión.",
        calle="Ruta E-53",
        numero="50",
        piso=None,
        depto=None,
        entre_calles="Camino al Dique y Los Nogales",
        id_ciudad=3, # Reemplaza con un ID de ciudad válida (ej. La Cumbre, Córdoba)
        id_tipo=casa_de_campo.id,
        huespedes=10,
        ambientes=7,
        banios=3,
        cocheras=3,
        precioNoche=180.00,
        codigoAcceso="3301", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=1,
        id_encargado=2,
        requiere_documentacion=False
    )

    # --- Ejemplos de Casas en la Playa ---
    prop9 = propiedades.create_propiedad(
        nombre="Chalet Playero a pasos del mar en Pinamar",
        descripcion="Comodidad y ubicación privilegiada para disfrutar de la costa atlántica en familia.",
        calle="Av. Libertador",
        numero="800",
        piso=None,
        depto=None,
        entre_calles="Shaw y Júpiter",
        id_ciudad=4, # Reemplaza con un ID de ciudad válida (ej. Pinamar)
        id_tipo=casa_en_la_playa.id,
        huespedes=7,
        ambientes=4,
        banios=2,
        cocheras=1,
        precioNoche=150.00,
        codigoAcceso="4401", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=2,
        id_encargado=2,
        requiere_documentacion=False
    )

    # --- Ejemplos de Chalets ---
    prop10 = propiedades.create_propiedad(
        nombre="Chalet Alpino con vistas al Nahuel Huapi",
        descripcion="Acogedor y cálido, ideal para esquiar en invierno o hacer senderismo en verano. Chimenea y vistas espectaculares.",
        calle="Av. Bustillo",
        numero="2500",
        piso=None,
        depto=None,
        entre_calles="Km 2.5 y Km 3.0",
        id_ciudad=5, # Reemplaza con un ID de ciudad válida (ej. Bariloche)
        id_tipo=chalet.id,
        huespedes=6,
        ambientes=4,
        banios=2.5,
        cocheras=1,
        precioNoche=160.00,
        codigoAcceso="5501", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=1,
        id_encargado=1,
        requiere_documentacion=False
    )

    # --- Ejemplos de Cabañas ---
    prop11 = propiedades.create_propiedad(
        nombre="Cabaña rústica junto al río en El Bolsón",
        descripcion="Inmersión en la naturaleza, perfecta para la pesca y el descanso. Equipada con todo lo necesario.",
        calle="Acceso Ruta 40 Sur",
        numero="10",
        piso=None,
        depto=None,
        entre_calles="Río Azul y Lago Puelo",
        id_ciudad=6, # Reemplaza con un ID de ciudad válida (ej. El Bolsón)
        id_tipo=cabaña.id,
        huespedes=4,
        ambientes=3,
        banios=1,
        cocheras=1,
        precioNoche=90.00,
        codigoAcceso="6001", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=1,
        id_encargado=5,
        requiere_documentacion=False
    )

    # --- Ejemplos de Estudios ---
    prop12 = propiedades.create_propiedad(
        nombre="Estudio Chic en Recoleta",
        descripcion="Funcional y elegante, ideal para viajeros solos o parejas. Cerca de museos y atracciones.",
        calle="Ayacucho",
        numero="1500",
        piso="8",
        depto="C",
        entre_calles="Av. Santa Fe y Marcelo T. de Alvear",
        id_ciudad=1, # Reemplaza con un ID de ciudad válida
        id_tipo=estudio.id,
        huespedes=2,
        ambientes=1,
        banios=1,
        cocheras=0,
        precioNoche=60.00,
        codigoAcceso="7701", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=1,
        id_encargado=1,
        requiere_documentacion=False
    )

    # --- Ejemplos de Lofts ---
    prop13 = propiedades.create_propiedad(
        nombre="Loft Industrial en San Telmo",
        descripcion="Diseño vanguardista en el corazón del barrio histórico. Techos altos y ambiente bohemio.",
        calle="Defensa",
        numero="500",
        piso="PB",
        depto="Loft",
        entre_calles="México y Chile",
        id_ciudad=1, # Reemplaza con un ID de ciudad válida
        id_tipo=loft.id,
        huespedes=2,
        ambientes=2,
        banios=1,
        cocheras=0,
        precioNoche=85.00,
        codigoAcceso="8801", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=2,
        id_encargado=2,
        requiere_documentacion=False
    )

    # --- Ejemplos de Dúplex ---
    prop14 = propiedades.create_propiedad(
        nombre="Dúplex con Vista al Mar en Mar del Plata",
        descripcion="Amplio y luminoso, con dos plantas y balcón. Cerca de la playa y el centro.",
        calle="Av. Patricio Peralta Ramos",
        numero="2000",
        piso="1",
        depto="A",
        entre_calles="Peatonal San Martín y Rivadavia",
        id_ciudad=7, # Reemplaza con un ID de ciudad válida (ej. Mar del Plata)
        id_tipo=duplex.id,
        huespedes=5,
        ambientes=3,
        banios=1.5,
        cocheras=1,
        precioNoche=110.00,
        codigoAcceso="9901", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=1,
        id_encargado=1,
        requiere_documentacion=False
    )

    # --- Ejemplos de Condominios ---
    prop15 = propiedades.create_propiedad(
        nombre="Condominio Exclusivo con Amenities en Colonia del Sacramento",
        descripcion="Unidad de lujo en un complejo con piscina, gimnasio y seguridad. Cerca del casco histórico.",
        calle="Ruta 1",
        numero="10",
        piso="2",
        depto="B",
        entre_calles="Acceso a Colonia y Río de la Plata",
        id_ciudad=8, # Reemplaza con un ID de ciudad válida (ej. Colonia del Sacramento, Uruguay)
        id_tipo=condominio.id,
        huespedes=4,
        ambientes=3,
        banios=2,
        cocheras=1,
        precioNoche=130.00,
        codigoAcceso="9910", # Código estático de 6 dígitos
        is_habilitada=True,
        id_pol_reserva=2,
        id_encargado=2,
        requiere_documentacion=False
    )

    print("Propiedades de ejemplo creadas")

    # Crear reservas de ejemplo
    #
    #
    #
    # Crear reservas de ejemplo
    estadoConfirmado = parametricas.create_estado("Confirmada")
    estadoPendiente = parametricas.create_estado("Pendiente")
    estadoCancelada = parametricas.create_estado("Cancelada")
    estadoFinalizada = parametricas.create_estado("Finalizada")

    reserva1 = reservas.create_reserva({
        "id_propiedad": prop1.id,
        "id_inquilino": user6.id,
        "id_usuario_carga": user2.id,
        "cantidad_personas": 4,
        "monto_pagado": 150.0,
        "monto_total": 600.0,
        "id_chat": None,
        "id_estado": estadoFinalizada.id,  
        "fecha_inicio": datetime(2024, 12, 10),
        "fecha_fin": datetime(2024, 12, 14)
    })

    reserva2 = reservas.create_reserva({
        "id_propiedad": prop2.id,
        "id_inquilino": user3.id,
        "id_usuario_carga": user1.id,
        "cantidad_personas": 2,
        "monto_pagado": 75.0,
        "monto_total": 150.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2025, 11, 1),
        "fecha_fin": datetime(2025, 11, 3)
    })

    reserva3 = reservas.create_reserva({
        "id_propiedad": prop3.id,
        "id_inquilino": user7.id,
        "id_usuario_carga": None,
        "cantidad_personas": 3,
        "monto_pagado": 120.0,
        "monto_total": 360.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2025, 10, 20),
        "fecha_fin": datetime(2025, 10, 23)
    })

    reserva4 = reservas.create_reserva({
        "id_propiedad": prop4.id,
        "id_inquilino": user1.id,
        "id_usuario_carga": user4.id,
        "cantidad_personas": 5,
        "monto_pagado": 200.0,
        "monto_total": 800.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2025, 12, 5),
        "fecha_fin": datetime(2025, 12, 10)
    })

    reserva5 = reservas.create_reserva({
        "id_propiedad": prop5.id,
        "id_inquilino": user2.id,
        "id_usuario_carga": user5.id,
        "cantidad_personas": 2,
        "monto_pagado": 90.0,
        "monto_total": 180.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2024, 9, 15),
        "fecha_fin": datetime(2024, 9, 17)
    })

    reserva6 = reservas.create_reserva({
        "id_propiedad": prop6.id,
        "id_inquilino": user4.id,
        "id_usuario_carga": user6.id,
        "cantidad_personas": 6,
        "monto_pagado": 250.0,
        "monto_total": 1000.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2026, 1, 10),
        "fecha_fin": datetime(2026, 1, 15)
    })

    reserva7 = reservas.create_reserva({
        "id_propiedad": prop7.id,
        "id_inquilino": user5.id,
        "id_usuario_carga": user7.id,
        "cantidad_personas": 3,
        "monto_pagado": 100.0,
        "monto_total": 300.0,
        "id_chat": None,
        "id_estado": estadoFinalizada.id,
        "fecha_inicio": datetime(2025, 9, 1),
        "fecha_fin": datetime(2025, 9, 4)
    })

    reserva8 = reservas.create_reserva({
        "id_propiedad": prop8.id,
        "id_inquilino": user6.id,
        "id_usuario_carga": user1.id,
        "cantidad_personas": 2,
        "monto_pagado": 60.0,
        "monto_total": 120.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2025, 10, 1),
        "fecha_fin": datetime(2025, 10, 3)
    })

    reserva9 = reservas.create_reserva({
        "id_propiedad": prop9.id,
        "id_inquilino": user6.id,
        "id_usuario_carga": user2.id,
        "cantidad_personas": 1,
        "monto_pagado": 40.0,
        "monto_total": 80.0,
        "id_chat": None,
        "id_estado": estadoCancelada.id,
        "fecha_inicio": datetime(2024, 10, 25),
        "fecha_fin": datetime(2024, 10, 27)
    })

    reserva10 = reservas.create_reserva({
        "id_propiedad": prop10.id,
        "id_inquilino": user1.id,
        "id_usuario_carga": user3.id,
        "cantidad_personas": 2,
        "monto_pagado": 80.0,
        "monto_total": 240.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2025, 11, 20),
        "fecha_fin": datetime(2025, 11, 23)
    })

    reserva11 = reservas.create_reserva({
        "id_propiedad": prop11.id,
        "id_inquilino": user2.id,
        "id_usuario_carga": user4.id,
        "cantidad_personas": 5,
        "monto_pagado": 180.0,
        "monto_total": 720.0,
        "id_chat": None,
        "id_estado": estadoCancelada.id,
        "fecha_inicio": datetime(2025, 9, 5),
        "fecha_fin": datetime(2025, 9, 9)
    })

    reserva12 = reservas.create_reserva({
        "id_propiedad": prop12.id,
        "id_inquilino": user3.id,
        "id_usuario_carga": user5.id,
        "cantidad_personas": 4,
        "monto_pagado": 130.0,
        "monto_total": 520.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2026, 2, 1),
        "fecha_fin": datetime(2026, 2, 5)
    })

    reserva13 = reservas.create_reserva({
        "id_propiedad": prop13.id,
        "id_inquilino": user4.id,
        "id_usuario_carga": user6.id,
        "cantidad_personas": 3,
        "monto_pagado": 110.0,
        "monto_total": 330.0,
        "id_chat": None,
        "id_estado": estadoFinalizada.id,
        "fecha_inicio": datetime(2024, 11, 10),
        "fecha_fin": datetime(2024, 11, 13)
    })

    reserva14 = reservas.create_reserva({
        "id_propiedad": prop14.id,
        "id_inquilino": user5.id,
        "id_usuario_carga": user7.id,
        "cantidad_personas": 2,
        "monto_pagado": 95.0,
        "monto_total": 190.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2025, 12, 1),
        "fecha_fin": datetime(2025, 12, 3)
    })

    reserva15 = reservas.create_reserva({
        "id_propiedad": prop15.id,
        "id_inquilino": user1.id,
        "id_usuario_carga": user2.id,
        "cantidad_personas": 4,
        "monto_pagado": 160.0,
        "monto_total": 640.0,
        "id_chat": None,
        "id_estado": estadoConfirmado.id,
        "fecha_inicio": datetime(2026, 3, 1),
        "fecha_fin": datetime(2026, 3, 5)
    }) 
    
    print("Reservas de ejemplo creadas")


    # Agregar imagenes a las propiedades

    from src.models import imagenes
    img1 = imagenes.create_imagen(
        url="/imagenes/propiedad/1.png",
        id_propiedad=prop1.id,
    )
    img2 = imagenes.create_imagen(
        url="/imagenes/propiedad/2.png",
        id_propiedad=prop2.id,
    )
    img3 = imagenes.create_imagen(
        url="/imagenes/propiedad/3.png",
        id_propiedad=prop3.id,
    )
    img4 = imagenes.create_imagen(
        url="/imagenes/propiedad/4.png",
        id_propiedad=prop4.id,
    )
    img5 = imagenes.create_imagen(
        url="/imagenes/propiedad/5.png",
        id_propiedad=prop5.id,
    )
    img6 = imagenes.create_imagen(
        url="/imagenes/propiedad/6.png",
        id_propiedad=prop6.id,
    )
    img7 = imagenes.create_imagen(
        url="/imagenes/propiedad/7.png",
        id_propiedad=prop7.id,
    )
    img8 = imagenes.create_imagen(
        url="/imagenes/propiedad/8.png",
        id_propiedad=prop8.id,
    )
    img9 = imagenes.create_imagen(
        url="/imagenes/propiedad/9.png",
        id_propiedad=prop9.id,
    )
    img10 = imagenes.create_imagen(
        url="/imagenes/propiedad/10.png",
        id_propiedad=prop10.id,
    )
    img11 = imagenes.create_imagen(
        url="/imagenes/propiedad/11.png",
        id_propiedad=prop11.id,
    )
    img12 = imagenes.create_imagen(
        url="/imagenes/propiedad/12.png",
        id_propiedad=prop12.id,
    )
    img13 = imagenes.create_imagen(
        url="/imagenes/propiedad/13.png",
        id_propiedad=prop13.id,
    )
    img14 = imagenes.create_imagen(
        url="/imagenes/propiedad/14.png",
        id_propiedad=prop14.id,
    )
    img15 = imagenes.create_imagen(
        url="/imagenes/propiedad/15.png",
        id_propiedad=prop15.id,
    )
    img16 = imagenes.create_imagen(
        url="/imagenes/usuario/16.png",
        id_usuario=user6.id,
    )
    img17 = imagenes.create_imagen(
        url="/imagenes/usuario/17.png",
        id_usuario=user6.id,
    )
    img18 = imagenes.create_imagen(
        url="/imagenes/propiedad/18.png",
        id_propiedad=prop2.id,
    )
    img19 = imagenes.create_imagen(
        url="/imagenes/propiedad/19.png",
        id_propiedad=prop2.id,
    )
    img20 = imagenes.create_imagen(
        url="/imagenes/usuario/20.jpeg",
        id_usuario=user7.id,
    )
    img21 = imagenes.create_imagen(
        url="/imagenes/usuario/21.png",
        id_usuario=user7.id,
    )


