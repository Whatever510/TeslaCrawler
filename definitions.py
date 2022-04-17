""" Collection of the necessary links"""

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

links_apac = {
    "AU": "https://www.tesla.com/en_AU/models/design?redirect=no#overview",
    "NZ": "https://www.tesla.com/en_NZ/models/design?redirect=no#overview"
}

country_codes_na = ["US", "CA", "MX", "PR"]

country_codes_eu = ["BE", "CZ", "DK", "BE", "DE", "EE",
                    "GR", "ES", "FR", "HR", "IE", "IS",
                    "IT", "LU", "HU", "NL", "NO", "AT",
                    "PL", "PT", "RO", "SL", "CH", "SE",
                    "FI", "GB"]

country_codes_apac = ["AU", "NZ"]


def get_links_na():
    """
    Get the Links for North America.
    :return: The links for north america.
    """
    return links_na


def get_links_eu():
    """
    Get the Links for Europe.
    :return: The links for europe.
    """
    return links_eu

def get_links_apac():
    """
    Get the Links for Asia Pacific.
    :return: The links for Asia Pacific.
    """
    return links_apac


def get_country_codes_na():
    """
    Get the Country Codes for North America.
    :return: The country codes for North America.
    """
    return country_codes_na


def get_country_code_eu():
    """
    Get the Country Codes for europe.
    :return: The country codes for europe.
    """
    return country_codes_eu

def get_country_codes_apac():
    """
    Get the Country Codes for Asia Pacific.
    :return: The country codes for Asia Pacific.
    """
    return country_codes_apac
