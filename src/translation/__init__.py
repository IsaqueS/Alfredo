from .translations import Translations
from typing import Callable

translation_server: Translations = Translations()
tr: Callable[[str],str] = translation_server.get_message