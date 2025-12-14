import re
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def set_username_from_fields(sender, instance, **kwargs):
    if not instance.username:
        if hasattr(instance, 'nickname') and instance.nickname:
            instance.username = instance.nickname
        elif instance.first_name and instance.last_name:
            instance.username = f"{instance.first_name}{instance.last_name}".replace(" ", "")
        elif instance.email:
            instance.username = instance.email.split('@')[0]


class ValidatePassword:
    def validate(self, password, user=None):
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]|\\:;'<>,.?/`~-])[A-Za-z\d!@#$%^&*()_+={}\[\]|\\:;'<>,.?/`~-]{8,}$"

        if not re.match(password_pattern, password):
            raise ValidationError(
                'Password needs to have at minimum one uppercase letter, one lowercase letter, one digit, and one special character'
            )
    
    def get_help_text(self):
        return 'Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'
    

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp) +
                str(user.is_active))
    
activate_token = AccountActivationTokenGenerator()