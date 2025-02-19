from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def criar_grupos_padrao(sender, **kwargs):
    grupos = ["Cliente", "Balconista", "Admin"]

    for grupo in grupos:
        Group.objects.get_or_create(name=grupo)

    print("Grupos criados ou já existentes:", grupos)
