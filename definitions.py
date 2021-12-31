

links_na = {
    "US": "https://www.tesla.com/models/design?redirect=no#overview",
    "CA": "https://www.tesla.com/en_CA/models/design?redirect=no#overview",
    "MX": "https://www.tesla.com/es_MX/models/design?redirect=no#overview",
    "PR": "https://www.tesla.com/en_PR/models/design?redirect=no#overview"
}

links_eu = {
    "BE": "https://www.tesla.com/nl_BE/models/design?redirect=no#overview",
    "CZ": "https://www.tesla.com/cs_CZ/models/design?redirect=no#overview",
    "DK": "https://www.tesla.com/da_DK/models/design?redirect=no#overview",
    "DE": "https://www.tesla.com/de_DE/models/design?redirect=no#overview",
    "EE": "https://www.tesla.com/en_EE/models/design?redirect=no#overview",
    "GR": "https://www.tesla.com/el_GR/models/design?redirect=no#overview",
    "ES": "https://www.tesla.com/es_ES/models/design?redirect=no#overview",
    "FR": "https://www.tesla.com/fr_FR/models/design?redirect=no#overview",
    "HR": "https://www.tesla.com/hr_HR/models/design?redirect=no#overview",
    "IE": "https://www.tesla.com/en_IE/models/design?redirect=no#overview",
    "IS": "https://www.tesla.com/is_IS/models/design?redirect=no#overview",
    "IT": "https://www.tesla.com/it_IT/models/design?redirect=no#overview",
    "LU": "https://www.tesla.com/de_LU/models/design?redirect=no#overview",
    "HU": "https://www.tesla.com/hu_HU/models/design?redirect=no#overview",
    "NL": "https://www.tesla.com/nl_NL/models/design?redirect=no#overview",
    "NO": "https://www.tesla.com/no_NO/models/design?redirect=no#overview",
    "AT": "https://www.tesla.com/de_AT/models/design?redirect=no#overview",
    "PL": "https://www.tesla.com/pl_PL/models/design?redirect=no#overview",
    "PT": "https://www.tesla.com/pt_PT/models/design?redirect=no#overview",
    "RO": "https://www.tesla.com/ro_RO/models/design?redirect=no#overview",
    "SL": "https://www.tesla.com/sl_SI/models/design?redirect=no#overview",
    "CH": "https://www.tesla.com/de_CH/models/design?redirect=no#overview",
    "SE": "https://www.tesla.com/sv_SE/models/design?redirect=no#overview",
    "FI": "https://www.tesla.com/fi_FI/models/design?redirect=no#overview",
    "GB": "https://www.tesla.com/en_GB/models/design?redirect=no#overview"
}

country_codes_na = ["US", "CA", "MX", "PR"]

country_codes_eu = ["BE", "CZ", "DK", "BE", "DE", "EE",
                    "GR", "ES", "FR","HR", "IE", "IS",
                    "IT", "LU", "HU", "NL", "NO", "AT",
                    "PL", "PT", "RO", "SL", "CH", "SE",
                    "FI", "GB"]

def get_links_na():
    return links_na

def get_links_eu():
    return links_eu

def get_country_codes_na():
    return country_codes_na

def get_country_code_eu():
    return country_codes_eu
