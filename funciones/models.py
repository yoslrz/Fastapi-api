models = [
    '''CREATE TABLE IF NOT EXISTS accesos (
        id VARCHAR(100) PRIMARY KEY,
        correo VARCHAR(60) NOT NULL,
        password VARCHAR(200) NOT NULL,
        estatus INT(1) NOT NULL DEFAULT '0',
        creacion_fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        rol VARCHAR(60) NOT NULL
    ) ENGINE = InnoDB;''',

    '''CREATE TABLE IF NOT EXISTS usuarios (
        id VARCHAR(100) PRIMARY KEY,
        curp VARCHAR(150) NOT NULL,
        rfc VARCHAR(200) NOT NULL,
        nombre VARCHAR(200) NOT NULL,
        apellido_paterno VARCHAR(200) NOT NULL,
        apellido_materno VARCHAR(200),
        fecha_eliminacion TIMESTAMP,
        id_acceso VARCHAR(200) NOT NULL,
        CONSTRAINT fk_acceso FOREIGN KEY (id_acceso) REFERENCES accesos(id)
    ) ENGINE = InnoDB;''',

    '''CREATE TABLE IF NOT EXISTS info_domicilio (
        id VARCHAR(100) PRIMARY KEY,
        calle VARCHAR(500) NOT NULL,
        colonia VARCHAR(200) NOT NULL,
        codigo_postal VARCHAR(200) NOT NULL,
        delegacion VARCHAR(200) NOT NULL,
        fecha_eliminacion TIMESTAMP,
        id_usuario VARCHAR(200) NOT NULL,
        CONSTRAINT fk_domicio FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
    ) ENGINE = InnoDB;'''
]
