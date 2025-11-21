from django.db import migrations

def create_user_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    try:
        add_mono = Permission.objects.get(codename='add_monografia')
        change_mono = Permission.objects.get(codename='change_monografia')
        delete_mono = Permission.objects.get(codename='delete_monografia')
        view_mono = Permission.objects.get(codename='view_monografia')
    except Permission.DoesNotExist:
        print("Permissões de Monografia não encontradas (possívelmente em ambiente de teste). Pulando criação de grupos.")
        return

    alunos_group, created = Group.objects.get_or_create(name='Alunos')
    if created:
        
        alunos_group.permissions.set([add_mono, change_mono, delete_mono, view_mono])
        print("Grupo 'Alunos' criado.")


    professores_group, created = Group.objects.get_or_create(name='Professores')
    if created:
        professores_group.permissions.set([change_mono, view_mono])
        print("Grupo 'Professores' criado.")

    pendentes_group, created = Group.objects.get_or_create(name='Professores Pendentes')
    if created:
        print("Grupo 'Professores Pendentes' criado.")

    admin_group, created = Group.objects.get_or_create(name='Administradores')
    if created:
        print("Grupo 'Administradores' criado.")

def remove_user_groups(apps, schema_editor):
    
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=['Alunos', 'Professores', 'Professores Pendentes', 'Administradores']
    ).delete()
    print("Grupos customizados removidos.")


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'), 
        ('auth', '__latest__'),

        ('users', '0001_initial'),
        ('monografias', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_user_groups, remove_user_groups),
    ]