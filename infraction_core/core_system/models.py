from django.db import models


## CHOICES
ESTADO = (
    ('1','Comparendo'), ('2','Resolución'), ('3','Cobro'), ('4','Archivado')
)

SERVICIO_VEHICULO = (
    ('1','Particular'), ('2','Oficial'), ('3','Otros'), ('4','Publico'), ('5','No reportado'), ('6','Diplomatico')
)

TIPO_VEHICULO = (
    ('1','AUTOMOVIL'), ('2','MOTOCICLETA'), ('3','CAMION'), ('4','CAMIONETA'), ('5','BUSETA'), ('6','MICROBUS'), ('7','DESCONOCIDA'), ('8','CAMPERO'), ('9','TRACTO/CAMION')
)

ORIGEN = (
    ('1','CRM'), ('2','Juzto.co'), ('1','Webhook externo')
)

DESTINO = (
    ('1','Verifik'), ('2','Bot SIMIT'), ('3','Bot Bogotá'), ('4','Bot Medellín')
)

TIPO_PERSONA = (
    ('Persona natural','Persona natural'), ('Persona jurídica','Persona jurídica')
)

TIPO_DOCUMENTO = (
    ('CC','CC'), ('TI','TI'), ('CE','CE'), ('RC','RC'), ('NIP','NIP'), ('NUIP','NUIP'), ('NIT','NIT'), ('PA','PA')
)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class CodigosConsulta(models.Model):
    id_codigo = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'codigos_consulta'


class Comparendos(models.Model):
    id_comparendo = models.CharField(primary_key=True, max_length=25)
    infraccion = models.ForeignKey('Infracciones', models.DO_NOTHING, db_column='infraccion', blank=True, null=True)
    id_persona = models.ForeignKey('Personas', models.DO_NOTHING, db_column='id_persona', blank=True, null=True)
    fotodeteccion = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=11,choices=ESTADO, blank=True, null=True)
    fecha_imposicion = models.DateField(blank=True, null=True)
    fecha_resolucion = models.DateField(blank=True, null=True)
    fecha_cobro_coactivo = models.DateField(blank=True, null=True)
    numero_resolucion = models.CharField(max_length=30, blank=True, null=True)
    numero_cobro_coactivo = models.CharField(max_length=30, blank=True, null=True)
    placa = models.CharField(max_length=6, blank=True, null=True)
    servicio_vehiculo = models.CharField(max_length=12, choices=SERVICIO_VEHICULO, blank=True, null=True)
    tipo_vehiculo = models.CharField(max_length=13, choices=TIPO_VEHICULO, blank=True, null=True)
    secretaria = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=120, blank=True, null=True)
    valor_neto = models.FloatField(blank=True, null=True)
    valor_pago = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comparendos'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Infracciones(models.Model):
    id_infraccion = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=5)
    description = models.CharField(max_length=5000, blank=True, null=True)
    id_sancion = models.ForeignKey('Sanciones', models.DO_NOTHING, db_column='id_sancion')
    inmovilizacion = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'infracciones'
        unique_together = (('id_infraccion', 'id_sancion'),)


class Logs(models.Model):
    id_log = models.OneToOneField(CodigosConsulta, models.DO_NOTHING, db_column='id_log', primary_key=True)
    fecha = models.DateTimeField()
    origen = models.CharField(max_length=15,choices=ORIGEN)
    destino = models.CharField(max_length=12,choices=DESTINO)
    usuario = models.ForeignKey('Personas', models.DO_NOTHING, db_column='usuario', blank=True, null=True)
    resultado = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'logs'
        unique_together = (('id_log', 'resultado'),)


class Personas(models.Model):
    id_persona = models.AutoField(primary_key=True)
    documento = models.CharField(max_length=20)
    tipo_documento = models.CharField(max_length=4,choices=TIPO_DOCUMENTO)
    tipo_persona = models.CharField(max_length=16,choices=TIPO_PERSONA)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    movil = models.CharField(max_length=13, blank=True, null=True)
    fecha_consulta_comp = models.DateTimeField(blank=True, null=True)
    consulta_recurrente = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personas'



class SalariosMensuales(models.Model):
    id_salarios_mensuales = models.AutoField(primary_key=True)
    valor = models.FloatField(blank=True, null=True)
    anio = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salarios_mensuales'


class Sanciones(models.Model):
    id_sancion = models.AutoField(primary_key=True)
    anio = models.IntegerField(blank=True, null=True)
    infraccion = models.CharField(max_length=5, blank=True, null=True)
    smldv = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sanciones'


class Tokens(models.Model):
    id_token = models.AutoField(primary_key=True)
    token_key = models.CharField(max_length=800)

    class Meta:
        managed = False
        db_table = 'tokens'


class Parametrizaciones(models.Model):
    id_codigo = models.AutoField(primary_key=True)
    clave = models.CharField(unique=True, max_length=20)
    valor = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'parametrizaciones'
