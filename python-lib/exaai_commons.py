def get_api_key_from_config(config):
    auth_type = config.get("auth_type", "api_key")
    return config.get("api_key", {}).get("exa_api_key")


def get_exa_key(key):
    if key.startswith("exa_"):
        return key[len("exa_"):]
    else:
        return None


def config_to_params(config):
    params = {}
    for ui_key in config:
        exa_key = get_exa_key(ui_key)
        if exa_key and config.get(ui_key):
            params[exa_key] = config.get(ui_key)
    return params


def set_keys_to_int(dictionary, int_keys):
    for int_key in int_keys:
        if int_key in dictionary:
            dictionary[int_key] = int(dictionary.get(int_key))
    return dictionary


def process_domains_parameters(config):
    domain_mode = config.get("domain_mode", "include")
    if domain_mode == "include":
        config.pop("exa_excludeDomains", None)
        exa_includeDomains = config.get("exa_includeDomains", None)
        if exa_includeDomains:
            config["exa_includeDomains"] = exa_includeDomains.split(",")
    else:
        config.pop("exa_includeDomains", None)
        exa_includeDomains = config.get("exa_excludeDomains", None)
        if exa_includeDomains:
            config["exa_includeDomains"] = exa_includeDomains.split(",")
    return config
