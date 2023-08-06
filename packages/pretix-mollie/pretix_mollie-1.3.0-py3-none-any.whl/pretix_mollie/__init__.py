from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'pretix_mollie'
    verbose_name = 'Mollie payment integration for pretix'

    class PretixPluginMeta:
        name = ugettext_lazy('Mollie')
        author = 'Raphael Michel'
        description = ugettext_lazy('Integration for the Mollie payment provider.')
        category = 'PAYMENT'
        visible = True
        version = '1.3.0'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_mollie.PluginApp'
