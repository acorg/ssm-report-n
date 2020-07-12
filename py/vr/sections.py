import inspect
import logging; module_logger = logging.getLogger(__name__)
from . import latex
from .report import generate, substitute

# ----------------------------------------------------------------------

class cover:

    def __init__(self,
                 cover_top_space="130pt",
                 cover_after_meeting_date_space="180pt",
                 cover_quotation="\\quotation",
                 report_hemisphere="Southern",
                 report_year="2021",
                 teleconference="Teleconference 1",
                 addendum="",
                 meeting_date="11th August 2020"
    ):
        self.args = inspect.getargvalues(inspect.currentframe()).locals

    def latex(self):
        return [
            substitute(latex.T_Cover,
                       **self.args
                       )
            ]

# ----------------------------------------------------------------------

class _single_latex_entry:

    def __init__(self, latex_ref, **args):
        self.latex_ref = latex_ref
        self.args = args

    def latex(self):
        try:
            return [substitute(self.latex_ref, **self.args)]
        except Exception as err:
            module_logger.error(f"args: {self.args}")
            raise

# ----------------------------------------------------------------------

# toc()
class toc (_single_latex_entry):
    def __init__(self): super().__init__(latex.T_TOC)

# vspace(1)
class vspace (_single_latex_entry):
    def __init__(self, em=1): super().__init__(latex.T_VSpace, em=em)

# text_no_indent("text")
class text_no_indent (_single_latex_entry):
    def __init__(self, text): super().__init__(latex.T_Text_NoIndent, text=text)

# section_title("H1N1pdm09")
class section_title (_single_latex_entry):
    def __init__(self, title): super().__init__(latex.T_Section, title=title)

# subsection_title("H1N1pdm09 geographic data")
class subsection_title (_single_latex_entry):
    def __init__(self, title): super().__init__(latex.T_Subsection, title=title)

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
