from models import Dia, Empresa, FranjaHoraria, Horario, Rol, Trabajador
from datetime import time

def mockdata_create():
    print("Creating mockdata...")

    # Create days
    lunes     = Dia(nombre="Lunes"     , descripcion="Primer día de la semana" )
    martes    = Dia(nombre="Martes"    , descripcion="Segundo día de la semana")
    miercoles = Dia(nombre="Miércoles" , descripcion="Tercer día de la semana" )
    jueves    = Dia(nombre="Jueves"    , descripcion="Cuarto día de la semana" )
    viernes   = Dia(nombre="Viernes"   , descripcion="Quinto día de la semana" )
    sabado    = Dia(nombre="Sábado"    , descripcion="Sexto día de la semana"  )
    domingo   = Dia(nombre="Domingo"   , descripcion="Séptimo día de la semana")

    lunes.save()
    martes.save()
    miercoles.save()
    jueves.save()
    viernes.save()
    sabado.save()
    domingo.save()
    print("Days created succesfully!")

    # Create companies
    google = Empresa(nombre="Google", latitud=0, longitud=-0, radio=50)
    google.save()
    print("Companies created succesfully!")

    # Create roles
    admin_role = Rol(nombre="Administrador")
    employee_role = Rol(nombre="Empleado")

    admin_role.save()
    employee_role.save()

    print("Roles created succesfully!")

    # Create schedule
    full_time_schedule = Horario(nombre="Full Time", descripcion="Horario de tiempo completo")
    part_time_schedule = Horario(nombre="Part Time", descripcion="Horario de medio tiempo")

    full_time_schedule.save()
    part_time_schedule.save()

    print("Schedule created succesfully!")

    # Create shifts (associate with schedule and day after creation)
    morning_shift = FranjaHoraria(hora_entrada=time(9, 0), hora_salida=time(17, 0))
    afternoon_shift = FranjaHoraria(hora_entrada=time(14, 0), hora_salida=time(22, 0))

    print("Shifts created succesfully!")

    # Create employees (associate with role, schedule, and company after creation)
    admin_user = Trabajador(
        nif="12345678A",
        nombre="John Doe",
        telefono="123456789",
        username="admin",
        password="password",
        debaja=False
    )

    employee_user = Trabajador(
        nif="87654321B",
        nombre="Jane Smith",
        telefono="987654321",
        username="employee",
        password="password"
    )

    print("Employees created succesfully!")

    # Associate relationships
    morning_shift.horario = full_time_schedule
    morning_shift.dia = lunes
    morning_shift.save()

    afternoon_shift.horario = part_time_schedule
    afternoon_shift.dia = martes
    afternoon_shift.save()

    admin_user.rol = admin_role
    admin_user.horario = full_time_schedule
    admin_user.empresa = google
    admin_user.save()

    employee_user.rol = employee_role
    employee_user.horario = part_time_schedule
    employee_user.empresa = google
    employee_user.save()

    print("Mockdata creation has finished!")

"""
SELECT * FROM dias;
SELECT * FROM empresas;
SELECT * FROM franjas_horarias;
SELECT * FROM horarios;
SELECT * FROM incidencias;
SELECT * FROM registros;
SELECT * FROM roles;
SELECT * FROM trabajadores;
"""
