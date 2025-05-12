--- Creación de tablas ---
CREATE TABLE estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL
);

CREATE TABLE intereses_estudiante (
    id_estudiante INTEGER NOT NULL,
    interes VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_estudiante, interes),
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE
);

CREATE TABLE instructores (
    id_instructor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    especialidad VARCHAR(100) NOT NULL
);

CREATE TABLE cursos (
    id_curso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    duracion_horas INTEGER NOT NULL CHECK (duracion_horas > 0),
    id_instructor INTEGER NOT NULL,
    FOREIGN KEY (id_instructor) REFERENCES instructores(id_instructor) ON DELETE SET NULL
);

CREATE TABLE inscripciones (
    id_inscripcion SERIAL PRIMARY KEY,
    id_estudiante INTEGER NOT NULL,
    id_curso INTEGER NOT NULL,
    fecha_inscripcion DATE NOT NULL DEFAULT CURRENT_DATE,
    UNIQUE (id_estudiante, id_curso),
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE CASCADE
);

CREATE TABLE progreso (
    id_progreso SERIAL PRIMARY KEY,
    id_inscripcion INTEGER NOT NULL,
    porcentaje_completado DECIMAL(5,2) NOT NULL CHECK (porcentaje_completado >= 0 AND porcentaje_completado <= 100),
    calificacion_final DECIMAL(5,2) CHECK (calificacion_final >= 0 AND calificacion_final <= 100),
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion) ON DELETE CASCADE
);

CREATE TABLE lecciones (
    id_leccion SERIAL PRIMARY KEY,
    id_curso INTEGER NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE CASCADE
);

CREATE TABLE evaluaciones (
    id_evaluacion SERIAL PRIMARY KEY,
    id_leccion INTEGER NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    puntaje_maximo DECIMAL(5,2) NOT NULL CHECK (puntaje_maximo > 0),
    FOREIGN KEY (id_leccion) REFERENCES lecciones(id_leccion) ON DELETE CASCADE
);

CREATE TABLE entregas (
    id_entrega SERIAL PRIMARY KEY,
    id_evaluacion INTEGER NOT NULL,
    id_estudiante INTEGER NOT NULL,
    fecha_entrega TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    puntaje_obtenido DECIMAL(5,2) CHECK (puntaje_obtenido >= 0),
    FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones(id_evaluacion) ON DELETE CASCADE,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE
);

CREATE TABLE categorias_curso (
    id_categoria SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE curso_categoria (
    id_curso INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    PRIMARY KEY (id_curso, id_categoria),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias_curso(id_categoria) ON DELETE CASCADE
);

--- Triggers ---
---
CREATE FUNCTION check_max_inscripciones()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM inscripciones WHERE id_estudiante = NEW.id_estudiante) >= 5 THEN
        RAISE EXCEPTION 'El estudiante ya está inscrito en el máximo de 5 cursos';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_max_inscripciones
BEFORE INSERT ON inscripciones
FOR EACH ROW
EXECUTE FUNCTION check_max_inscripciones();

---
CREATE FUNCTION update_fecha_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_fecha_actualizacion
BEFORE UPDATE ON progreso
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();
---
CREATE FUNCTION check_puntaje_obtenido()
RETURNS TRIGGER AS $$
DECLARE
    max_puntaje DECIMAL(5,2);
BEGIN
    SELECT puntaje_maximo INTO max_puntaje FROM evaluaciones WHERE id_evaluacion = NEW.id_evaluacion;
    IF NEW.puntaje_obtenido > max_puntaje THEN
        RAISE EXCEPTION 'El puntaje obtenido no puede superar el puntaje máximo de la evaluación';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_puntaje_obtenido
BEFORE INSERT OR UPDATE ON entregas
FOR EACH ROW
EXECUTE FUNCTION check_puntaje_obtenido();