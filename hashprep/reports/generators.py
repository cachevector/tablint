from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, summary, full=False, output_file=None):
        pass


# Lazy loading report classes
def _load_generator(format_name):
    if format_name == "md":
        from .markdown import MarkdownReport

        return MarkdownReport()
    elif format_name == "json":
        from .json import JsonReport

        return JsonReport()
    elif format_name == "html":
        try:
            from .html import HtmlReport

            return HtmlReport()
        except ImportError as e:
            raise ImportError("HTML reports require the reports extra: pip install 'hashprep[reports]'") from e
    elif format_name == "pdf":
        try:
            from .pdf import PdfReport

            return PdfReport()
        except Exception as e:
            raise ImportError(
                f"PDF reports require the reports extra: pip install 'hashprep[reports]'. Underlying error: {e}"
            ) from e
    return None


# get generators dictionary
def get_generators():
    if not hasattr(get_generators, "cache"):
        get_generators.cache = {}
    return get_generators.cache


def generate_report(summary, format="md", full=False, output_file=None, theme="minimal"):
    generators = get_generators()
    if format not in generators:
        gen = _load_generator(format)
        if gen is None:
            raise ValueError(f"Unsupported format: {format}")
        generators[format] = gen

    if format in ["html", "pdf"]:
        return generators[format].generate(summary, full, output_file, theme=theme)
    return generators[format].generate(summary, full, output_file)
