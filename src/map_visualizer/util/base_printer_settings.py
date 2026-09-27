from dataclasses import dataclass
from typing import Any


@dataclass
class BasePrinterSettings:
    """
    Base configuration for grid printers.

    Subclasses (e.g., CLIPrinterSettings, GUIPrinterSettings) can add
    specific fields like window_size, font, etc.
    """

    area_styles: dict[int, Any]
