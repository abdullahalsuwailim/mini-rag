import os
import re
from importlib import import_module
from typing import Any, Optional


class TemplateParser:

    def __init__(
        self,
        language: Optional[str] = None,
        default_language: str = "en"
    ):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = default_language

        self.set_language(language)

    def set_language(self, language: Optional[str] = None) -> None:
        """
        تغيير لغة القوالب يدويًا.

        إذا كانت اللغة غير موجودة، يتم استخدام اللغة الافتراضية.
        """

        selected_language = language or self.default_language
        selected_language = selected_language.strip().lower()

        language_path = os.path.join(
            self.current_path,
            "locales",
            selected_language
        )

        if os.path.isdir(language_path):
            self.language = selected_language
        else:
            self.language = self.default_language

    def set_language_from_text(self, text: str) -> str:
        """
        اكتشاف لغة السؤال وتغيير لغة القوالب بناءً عليها.

        حاليًا يدعم:
        - العربية
        - الإنجليزية
        """

        if re.search(r"[\u0600-\u06FF]", text or ""):
            detected_language = "ar"
        else:
            detected_language = "en"

        self.set_language(detected_language)

        return self.language

    def get(
        self,
        group: str,
        key: str,
        vars: Optional[dict[str, Any]] = None
    ) -> Optional[str]:
        """
        جلب قالب معين من ملف اللغة الحالي.
        """

        if not group or not key:
            return None

        vars = vars or {}

        targeted_language = self.language

        group_path = os.path.join(
            self.current_path,
            "locales",
            targeted_language,
            f"{group}.py"
        )

        # إذا لم يوجد القالب باللغة الحالية، استخدم اللغة الافتراضية
        if not os.path.exists(group_path):
            targeted_language = self.default_language

            group_path = os.path.join(
                self.current_path,
                "locales",
                targeted_language,
                f"{group}.py"
            )

        # إذا لم يوجد حتى باللغة الافتراضية
        if not os.path.exists(group_path):
            return None

        try:
            module = import_module(
                f".locales.{targeted_language}.{group}",
                package=__package__
            )
        except (ModuleNotFoundError, ImportError):
            return None

        key_attribute = getattr(module, key, None)

        if key_attribute is None:
            return None

        # إذا كان القالب من string.Template
        if hasattr(key_attribute, "substitute"):
            return key_attribute.substitute(vars)

        return str(key_attribute)
        
        