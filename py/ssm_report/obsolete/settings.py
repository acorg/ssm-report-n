error OBSOLETE

import sys, os, json
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
from acmacs_base.json import write_json
from acmacs_base.dict_merge import dict_merge

# ----------------------------------------------------------------------

def make_settings(force=False):
    from .settings_report import make_report_settings
    make_report_settings()
    from .serum_coverage import make_serum_coverage_report_settings
    make_serum_coverage_report_settings()
    from .geographic import make_geographic_settings
    make_geographic_settings(force=force)
    for entry in [
            {"virus_type": "h3", "assay": "hi"},
            {"virus_type": "h3", "assay": "neut"},
            {"virus_type": "h1", "assay": "hi"},
            {"virus_type": "bvic", "assay": "hi"},
            {"virus_type": "byam", "assay": "hi"}
            ]:
        make_map_settings(force=force, **entry)

# ----------------------------------------------------------------------

sMapSettings = """{ "_":"-*- js-indent-level: 2 -*-",
  "labs": %(labs)s,
  "information_labs": %(labs)s,
  "mods": {
%(mods)s
  }
}
"""

def make_map_settings(virus_type, assay, force):
    make_vaccine_settings(virus_type=virus_type, assay=assay, force=force)
    make_serology_settings(virus_type=virus_type, assay=assay, force=force)
    map_settings_file = Path(f"{virus_type}-{assay}.json")
    if force or not map_settings_file.exists():
        module_logger.info("writing {}".format(map_settings_file))
        labs = get_s(virus_type, assay, "labs")
        data = sMapSettings % {
            "labs": json.dumps(labs),
            "mods": get_s(virus_type=virus_type, assay=assay, name="data") + ",\n" + ",\n".join(make_mod(virus_type=virus_type, assay=assay, lab=lab) for lab in labs)
            }
        map_settings_file.open("w").write(data)
    return map_settings_file

# ----------------------------------------------------------------------

def make_vaccine_settings(virus_type, assay, force):
    settings_file = Path(f"vaccines.{virus_type}-{assay}.json")
    if force or not settings_file.exists():
        module_logger.info("writing {}".format(settings_file))
        with settings_file.open("w") as fd:
            fd.write(sVaccineSettings[f"{virus_type}-{assay}"])

# ----------------------------------------------------------------------

def make_serology_settings(virus_type, assay, force):
    settings_file = Path(f"serology.{virus_type}-{assay}.json")
    if force or not settings_file.exists():
        module_logger.info("writing {}".format(settings_file))
        with settings_file.open("w") as fd:
            fd.write(sSerologySettings[f"{virus_type}-{assay}"])

# ----------------------------------------------------------------------

def make_mod(virus_type, assay, lab):
    result = '\n    "?": "===================== {lab}  {virus_type}  {assay} ================================================="'.format(virus_type=virus_type.upper(), assay=assay.upper(), lab=lab)
    result += ",\n" + get_s_lab(virus_type=virus_type, assay=assay, lab=lab, name="data")
    return result

# ----------------------------------------------------------------------

def get_s(virus_type, assay, name):
    return globals()["s_{}_{}_{}".format(virus_type, assay, name)]

def get_s_lab(virus_type, assay, lab, name):
    return globals()["s_{}_{}_{}_{}".format(virus_type, assay, lab, name)]

# ======================================================================
# Vaccines
# ======================================================================

sVaccineSettings = {
    "h1-hi": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "ALL_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "no": 1}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, -1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.9, -0.5], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.5, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
      ],

      "? INFORMATION": "======================================================================",

    "ALL_vaccines_information": [
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"},
      {"?N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 45, "show": true, "order": "raise"}
    ],

    "CDC_vaccines_information": [
    ],
    "MELB_vaccines_information": [
    ],
    "NIID_vaccines_information": [
    ],
    "NIMR_vaccines_information": [
    ],

      "? END": "----------------------------------------------------------------------"
  }
}
""",
    "h3-hi": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "CDC_vaccines": [
      {"N": "antigens", "select": {"index": 1929, "?name": "MICHIGAN/15/2014 MK1/SIAT1 2015-01-12"},
       "size": 26, "fill": "cyan", "outline": "black", "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type", "size": 32},
       "raise_": true, "raise_if_not_found": false},

      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "TEXAS"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "SWITZERLAND"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type", "size": 32, "display_name": "Sw/13-cell"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "HONG KONG/4801/2014"}}, "report": true, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "HONG KONG/4801/2014"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"}}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "display_name": "Si/16-cell", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg", "no": 2}}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0.5, 1], "display_name": "Si/16-egg", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, -1], "display_name": "Si/16-NIB-egg", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise"},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
      {"?N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise"}
    ],

    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.2, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "TEXAS"}}, "label": {"offset": [-1, 0], "display_name": "TX/50/12-cell"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "SWITZERLAND"}}, "label": {"offset": [-1, 0], "display_name": "Sw/13-cell"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "SWITZERLAND"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "TEXAS"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "PERTH"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "display_name": "Si/16-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "display_name": "Si/16-NIB-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "display_name": "Si/16-cell", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise"},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"}
    ],

    "NIMR_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "SWITZERLAND"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "display_name": "Si/16-cell", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg", "no": 1}}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "display_name": "Si/16-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "? INFORMATION": "======================================================================",

    "CDC_vaccines_information": [
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell", "no": 2}}, "fill": "red",   "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"},
      {"?N": "antigens", "select": {"name": "A(H3N2)/SINGAPORE/INFIMH-16-0019/2016", "passage": "cell"}, "label": {}, "fill": "red",   "report": true, "outline": "black", "size": 25, "show": true, "order": "raise"}
    ],

    "MELB_vaccines_information": [
    ],

    "NIMR_vaccines_information": [
    ],

    "? END": "----------------------------------------------------------------------"
  }
}
""",
    "h3-neut": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "CDC_vaccines": [
      {"N": "antigens", "select": {"index": 0, "?name": "MICHIGAN/15/2014 MK1/SIAT1 2015-01-12"},
       "size": 26, "fill": "cyan", "outline": "black",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32},
       "raise_": true, "raise_if_not_found": false},

      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "SWITZERLAND"}},
       "label": {"offset": [1, 0.3], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "display_name": "Si/16-cell", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "display_name": "Si/16-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "HONG KONG"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "SWITZERLAND"}},
       "label": {"offset": [-1, 0], "display_name": "Sw/13-cell", "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "HONG KONG"}},
       "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0.5, 1], "display_name": "Si/16-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "display_name": "Si/16-IVR-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.9, 0.8], "display_name": "Si/16-cell", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "NIID_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "SWITZERLAND"}},
       "label": {"offset": [1, 0], "display_name": "Sw/13-cell", "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "TEXAS"}},
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "4801"}},
       "label": {"offset": [-0.95, -0.3], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "SWITZERLAND"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": false, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant", "name": "SWITZERLAND"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "display_name": "Si/16-cell", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.9, -0.5], "display_name": "Si/16-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "display_name": "Si/16-IVR-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, -1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate", "passage": "cell"}}, "label": {"offset": [0.5, -1], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate", "passage": "egg"}}, "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate", "passage": "reassortant"}}, "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type"}}
    ],

    "NIMR_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "display_name": "Si/16-cell", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "display_name": "Si/16-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "? OLD": "======================================================================",

    "?NIID_vaccines_old": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "SWITZERLAND"}}, "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "TEXAS"}}, "label": {"offset": [0, -1], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "4801"}}, "label": {"offset": [-0.8, -0.5], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "SWITZERLAND"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": false, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant", "name": "SWITZERLAND"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "display_name": "Si/16-cell", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "display_name": "Si/16-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "display_name": "Si/16-IVR-egg", "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, -1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate", "passage": "cell"}}, "label": {"offset": [-0.4, -1], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate", "passage": "egg"}}, "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate", "passage": "reassortant"}}, "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type"}}
    ],

    "? END": "----------------------------------------------------------------------"
  }
}
""",
    "bvic-hi": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "CDC_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.7, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "NIID_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.3, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "NIMR_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "BRISBANE"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.8, -0.9], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.5, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "? INFORMATION": "======================================================================",

    "CDC_vaccines_information": [
    ],
    "MELB_vaccines_information": [
    ],
    "NIID_vaccines_information": [
    ],
    "NIMR_vaccines_information": [
    ],

    "? END": "----------------------------------------------------------------------"
  }
}
""",
    "byam-hi": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "CDC_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell", "name": "WISCONSIN"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.5, -1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "FLORIDA"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": false, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0.7, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, -1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.4, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg", "name": "WISCONSIN"}},
       "label": {"offset": [-0.5, 1], "name_type": "abbreviated_with_passage_type"}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, -1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": false, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "NIID_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.8, -0.8], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "name": "FLORIDA"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "name": "WISCONSIN"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0.5, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "NIMR_vaccines": [
      {"show": false, "N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, -1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"show": false, "N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [1, 0], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "name": "FLORIDA"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "name": "WISCONSIN"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [-0.7, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
       "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],

    "? INFORMATION": "======================================================================",

    "CDC_vaccines_information": [
    ],
    "MELB_vaccines_information": [
    ],
    "NIID_vaccines_information": [
    ],
    "NIMR_vaccines_information": [
      {"show": false, "N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"},
      {"show": false, "N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "name": "FLORIDA"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "name": "WISCONSIN"}}, "show": false},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 45, "show": true, "order": "raise"}
    ],

    "? END": "----------------------------------------------------------------------"
  }
}
""",
    }

# ======================================================================
# Serology
# ======================================================================

sSerologySettings = {
    "h1-hi": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "ALL_serology": [
      {"?": "CDC report --------------------------------------------------"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},

      {"?": "NIID report --------------------------------------------------"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},

      {"?N":"antigens", "select": {"full_name": "A(H1N1)/MICHIGAN/272/2017 MDCK2 (2017-12-18)"},  "label": {"offset": [2, 0.6], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": "SWITZERLAND/2656/2017", "passage": "cell"}, "label": {"offset": [1, 0.5], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ]
  }
}
""",
    "h3-hi": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "CDC_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},

      {"?N":"antigens", "select": {"full_name": "A(H3N2)/SOUTH AUSTRALIA/135/2016 SIAT2/SIAT1 (2018-07-31)"}, "label": {"offset": [-1, 0], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": "A/Maryland/53/2017"},                                 "label": {"offset": [ 0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
      ],
    "MELB_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
      ],
    "NIMR_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
      ]
  }
}
""",
    "h3-neut": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "CDC_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},

      {"?N":"antigens", "select": {"full_name": "A(H3N2)/SOUTH AUSTRALIA/135/2016 SIAT2/SIAT1 (2018-07-31)"}, "label": {"offset": [-1, 0], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": "A/Maryland/53/2017"},                                 "label": {"offset": [ 0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
      ],
    "MELB_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
      ],
    "NIID_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
      ],
    "NIMR_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
      ]
  }
}
""",
    "bvic-hi": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "CDC_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},

      {"?N":"antigens", "select": {"full_name": "B/IOWA/6/2017 QMC2"},                "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": "B/HONG KONG/286/2017", "passage": "egg"}, "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ],
    "MELB_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ],
    "NIID_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ],
    "NIMR_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ]
  }
}
""",
    "byam-hi": """{ "_":"-*- js-indent-level: 2 -*-",
  "mods": {
    "CDC_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},

      {"?N":"antigens", "select": {"full_name": "B/GUYANE/5/2018 MDCK2 (2018-05-02)"}, "label": {"offset": [-1, 0], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": "B/PUERTO RICO/5/2018"},         "label": {"offset": [-1, 0], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ],
    "MELB_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ],
    "NIID_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ],
    "NIMR_serology": [
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"},
      {"?N":"antigens", "select": {"name": ""},  "label": {"offset": [0, 1], "size": 24, "name_type": "abbreviated_with_passage_type"}, "report": true, "size": 18, "outline": "black", "fill": "orange", "order": "raise"}
    ]
  }
}
""",
    }

# ======================================================================
# H1 HI
# ======================================================================

s_h1_hi_labs = ["ALL"]

s_h1_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "information": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "antigens", "select": {"older_than_days": 730}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "antigens", "select": {"younger_than_days": 730, "older_than_days": 365}, "fill": "#6F93E6", "outline": "black", "raise_": true},
      {"N": "antigens", "select": {"younger_than_days": 365}, "fill": "#F9DA4A", "outline": "black", "raise_": true}
    ],
    "information_clades": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "clades_last_12_months", "size": 15},
      "no_legend"
    ]
    """

# --------------- ALL H1 -------------------------------------------------------

s_h1_hi_ALL_data = """
    "ALL_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "ALL_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "ALL_viewport": [
      {"N": "viewport", "rel": [8, 5.5, -12]}
    ],
    "ALL_pre": [
    ],
    "ALL_mid": [
    ],
    "ALL_post": [
    ]"""

# --------------- CDC H1 -------------------------------------------------------

s_h1_hi_CDC_data = """
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# ======================================================================
# H3 HI
# ======================================================================

s_h3_hi_labs = ["CDC", "MELB", "NIMR"]

s_h3_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "aa_at_142": [
      {"N": "amino-acids", "pos": [142], "colors": {"G": "#049457", "K": "#F76A05", "R": "#A020F0", "N": "#93EDC3", "E": "#ED93BD", "I": "#742f32", "X": "#666666"}, "outline": "black", "legend": {"count": true}, "order": "raise"}
    ],
    "information": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "antigens", "select": {"older_than_days": 730}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "antigens", "select": {"younger_than_days": 730, "older_than_days": 365}, "fill": "#6F93E6", "outline": "black", "raise_": true},
      {"N": "antigens", "select": {"younger_than_days": 365}, "fill": "#F9DA4A", "outline": "black", "raise_": true}
    ],
    "information_clades": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "clades_last_12_months", "size": 15},
      "no_legend"
    ]"""

    # "serum_sectors": [
    #   {"N": "serum_circle", "serum": {"lab": "provide-lab", "index": "provide serum selector"}, "?antigen": {"index": 0}, "report": true,
    #    "circle": {"fill": "#C08080FF", "outline": "blue", "outline_width": 2, "angle_degrees": [0, 30], "radius_line_dash": "dash2", "?radius_line_color": "red", "?radius_line_width": 1},
    #    "mark_serum": {"fill": "lightblue", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12}},
    #    "mark_antigen": {"fill": "lightblue", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12}}}
    # ],
    # "serum_coverage_hk": [
    #   {"N": "serum_coverage", "serum": {"lab": "provide lab", "index": "provide serum selector"}, "?antigen": {"index": 1}, "report": true,
    #    "mark_serum": {"fill": "red", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12, "weight": "bold"}},
    #    "within_4fold": {"outline": "pink", "outline_width": 3, "order": "raise"},
    #    "outside_4fold": {"fill": "grey50", "outline": "black", "order": "raise"}}
    # ]

# --------------- CDC H3 HI -------------------------------------------------------

s_h3_hi_CDC_data = """
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [6.5, 7.5, -11]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# --------------- MELB H3 HI -------------------------------------------------------

s_h3_hi_MELB_data = """
    "MELB_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "MELB_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "MELB_viewport": [
      {"N": "viewport", "rel": [3.2, 1, -6]}
    ],
    "MELB_pre": [
    ],
    "MELB_mid": [
    ],
    "MELB_post": [
    ]"""

# --------------- NIMR H3 HI -------------------------------------------------------

s_h3_hi_NIMR_data = """
    "NIMR_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIMR_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIMR_viewport": [
      {"N": "viewport", "rel": [1.5, 2, -3]}
    ],
    "NIMR_pre": [
    ],
    "NIMR_mid": [
    ],
    "NIMR_post": [
    ]"""

# ======================================================================
# H3 Neut
# ======================================================================

s_h3_neut_labs = ["CDC", "MELB", "NIID", "NIMR"]

s_h3_neut_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "information": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "antigens", "select": {"older_than_days": 730}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "antigens", "select": {"younger_than_days": 730, "older_than_days": 365}, "fill": "#6F93E6", "outline": "black", "raise_": true},
      {"N": "antigens", "select": {"younger_than_days": 365}, "fill": "#F9DA4A", "outline": "black", "raise_": true}
    ],
    "information_clades": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "clades_last_12_months", "size": 15},
      "no_legend"
    ]"""

    # "serum_sectors": [
    #   {"N": "serum_circle", "serum": {"lab": "provide-lab", "index": "provide serum selector"}, "?antigen": {"index": 0}, "report": true,
    #    "circle": {"fill": "#C08080FF", "outline": "blue", "outline_width": 2, "angle_degrees": [0, 30], "radius_line_dash": "dash2", "?radius_line_color": "red", "?radius_line_width": 1},
    #    "mark_serum": {"fill": "lightblue", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12}},
    #    "mark_antigen": {"fill": "lightblue", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12}}}
    # ],
    # "serum_coverage_hk": [
    #   {"N": "serum_coverage", "serum": {"lab": "provide lab", "index": "provide serum selector"}, "?antigen": {"index": 1}, "report": true,
    #    "mark_serum": {"fill": "red", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12, "weight": "bold"}},
    #    "within_4fold": {"outline": "pink", "outline_width": 3, "order": "raise"},
    #    "outside_4fold": {"fill": "grey50", "outline": "black", "order": "raise"}}
    # ]

# --------------- CDC H3 Neut -------------------------------------------------------

s_h3_neut_CDC_data = """
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# --------------- MELB H3 Neut -------------------------------------------------------

s_h3_neut_MELB_data = """
    "MELB_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "MELB_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "MELB_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "MELB_pre": [
    ],
    "MELB_mid": [
    ],
    "MELB_post": [
    ]"""

# --------------- NIID H3 Neut -------------------------------------------------------

s_h3_neut_NIID_data = """
    "NIID_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIID_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIID_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "NIID_pre": [
    ],
    "NIID_mid": [
    ],
    "NIID_post": [
    ]"""

# --------------- NIMR H3 Neut -------------------------------------------------------

s_h3_neut_NIMR_data = """
    "NIMR_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIMR_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIMR_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "NIMR_pre": [
    ],
    "NIMR_mid": [
    ],
    "NIMR_post": [
    ]"""

# ======================================================================
# B/Vic HI
# ======================================================================

s_bvic_hi_labs = ["CDC", "MELB", "NIID", "NIMR"]

s_bvic_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "information": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "antigens", "select": {"older_than_days": 730}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "antigens", "select": {"younger_than_days": 730, "older_than_days": 365}, "fill": "#6F93E6", "outline": "black", "raise_": true},
      {"N": "antigens", "select": {"younger_than_days": 365}, "fill": "#F9DA4A", "outline": "black", "raise_": true},
      {"N": "antigens", "select": {"clade": "DEL2017"}, "fill": "#DE8244", "outline": "black", "raise_": true},
      {"N": "antigens", "select": {"clade": "TRIPLEDEL2017"}, "fill": "#BF3EFF", "outline": "black", "raise_": true}
    ],
    "information_clades": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "clades_last_12_months", "size": 15},
      "no_legend"
    ]"""

# --------------- CDC B/Vic HI -------------------------------------------------------

s_bvic_hi_CDC_data = """
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [2, 2, -4]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# --------------- MELB B/Vic HI -------------------------------------------------------

s_bvic_hi_MELB_data = """
    "MELB_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "MELB_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "MELB_viewport": [
      {"N": "viewport", "rel": [4, 6.5, -7]}
    ],
    "MELB_pre": [
    ],
    "MELB_mid": [
    ],
    "MELB_post": [
    ]"""

# --------------- NIID B/Vic HI -------------------------------------------------------

s_bvic_hi_NIID_data = """
    "NIID_flip": [
      {"N": "flip", "direction": "ew"}
    ],
    "NIID_rotate": [
      {"N": "rotate", "degrees": 90}
    ],
    "NIID_viewport": [
      {"N": "viewport", "rel": [1.6, 1.2, -3]}
    ],
    "NIID_pre": [
    ],
    "NIID_mid": [
    ],
    "NIID_post": [
    ]"""

# --------------- NIMR B/Vic HI -------------------------------------------------------

s_bvic_hi_NIMR_data = """
    "NIMR_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIMR_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIMR_viewport": [
      {"N": "viewport", "rel": [4, 4, -7]}
    ],
    "NIMR_pre": [
    ],
    "NIMR_mid": [
    ],
    "NIMR_post": [
    ]"""

# ======================================================================
# B/Yam HI
# ======================================================================

s_byam_hi_labs = ["CDC", "MELB", "NIID", "NIMR"]

s_byam_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "information": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "antigens", "select": {"older_than_days": 730}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "antigens", "select": {"younger_than_days": 730, "older_than_days": 365}, "fill": "#6F93E6", "outline": "black", "raise_": true},
      {"N": "antigens", "select": {"younger_than_days": 365}, "fill": "#F9DA4A", "outline": "black", "raise_": true}
    ],
    "information_clades": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1},
      {"N": "antigens", "select": "all", "size": 15},
      {"N": "clades_last_12_months", "size": 15},
      "no_legend"
    ]"""

# --------------- B/Yam HI CDC -------------------------------------------------------

s_byam_hi_CDC_data = """
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [2, 5, -7]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# --------------- B/Yam HI MELB -------------------------------------------------------

s_byam_hi_MELB_data = """
    "MELB_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "MELB_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "MELB_viewport": [
      {"N": "viewport", "rel": [2.5, 1.2, -4]}
    ],
    "MELB_pre": [
    ],
    "MELB_mid": [
    ],
    "MELB_post": [
    ]"""

# --------------- B/Yam HI NIID -------------------------------------------------------

s_byam_hi_NIID_data = """
    "NIID_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIID_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIID_viewport": [
      {"N": "viewport", "rel": [-0.7, -0.3, -1]}
    ],
    "NIID_pre": [
    ],
    "NIID_mid": [
    ],
    "NIID_post": [
    ]"""

# --------------- B/Yam HI NIMR -------------------------------------------------------

s_byam_hi_NIMR_data = """
    "NIMR_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIMR_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIMR_viewport": [
      {"N": "viewport", "rel": [1.5, 2.3, -4]}
    ],
    "NIMR_pre": [
    ],
    "NIMR_mid": [
    ],
    "NIMR_post": [
    ]"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
