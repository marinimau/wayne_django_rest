#
#   wayne_production copyright © 2021 - all rights reserved
#   Created at: 03/01/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from .eng.client_config_messages import messages as eng_client_messages
from .eng.password_recovery_messages import messages as eng_reset_password_messages


def get_messages(language, package):
    return eng_client_messages

