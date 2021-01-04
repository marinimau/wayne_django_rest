#
#   wayne_production copyright © 2021 - all rights reserved
#   Created at: 03/01/21
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.conf import settings
from .eng.client_config_messages import messages as eng_client_messages
from .eng.password_recovery_messages import messages as eng_reset_password_messages
from .eng.social_messages import messages as eng_social_messages
from .eng.user_messages import messages as eng_user_messages


# ----------------------------------------------------------------------------------------------------------------------
# get messages for the given package
# ----------------------------------------------------------------------------------------------------------------------
def get_messages(package='USER'):
    if package is settings.CONTENT_PACKAGES[0]:
        return dict(eng_user_messages)
    elif package is settings.CONTENT_PACKAGES[1]:
        return dict(eng_reset_password_messages)
    elif package is settings.CONTENT_PACKAGES[2]:
        return dict(eng_client_messages)
    elif package is settings.CONTENT_PACKAGES[3]:
        return dict(eng_social_messages)

