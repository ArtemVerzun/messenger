from .authentication import authentication
from .registration import registration
from .email_verification import email_verification
from .code_verification import code_verification
from .encryption_key import encryption_key
from .available_login import available_login
from .available_email import available_email
from .recovery_email_verification import recovery_email_verification
from .recovery_code_verification import recovery_code_verification
from .new_password import new_password
from .statistics import statistics
from .search import search
from .logout import logout
from .user_online import user_online
from .user_info import user_info
from core.types import RequestType

handlers = {
    RequestType.AUTHENTICATION: authentication,
    RequestType.REGISTRATION: registration,
    RequestType.EMAIL_VERIFICATION: email_verification,
    RequestType.CODE_VERIFICATION: code_verification,
    RequestType.ENCRYPTION_KEY: encryption_key,
    RequestType.AVAILABLE_LOGIN: available_login,
    RequestType.AVAILABLE_EMAIL: available_email,
    RequestType.RECOVERY_EMAIl_VERIFICATION: recovery_email_verification,
    RequestType.RECOVERY_CODE_VERIFICATION: recovery_code_verification,
    RequestType.NEW_PASSWORD: new_password,
    RequestType.STATS: statistics,
    RequestType.SEARCH: search,
    RequestType.LOGOUT: logout,
    RequestType.USER_STATUS: user_online,
    RequestType.USER_INFO: user_info
}
