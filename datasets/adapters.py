from datetime import datetime


def get_phase(value):
    mapping = {
        "emp": "empenho",
        "liq": "liquidacao",
        "pag": "pagamento",
    }
    return mapping.get(value.lower().strip(), None)


def currency_to_float(value):
    cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
    return float(cleaned_value)


def to_boolean(value):
    return value.lower() in ["y", "S", 1]


# FIXME eliminar duplicação
def from_str_to_datetime(date_str, supported_formats=["%d/%m/%Y", "%d/%m/%y"]):
    if date_str is None:
        return
    for supported_format in supported_formats:
        try:
            return datetime.strptime(date_str, supported_format)
        except ValueError:
            pass


def from_str_to_date(date_str, supported_formats=["%d/%m/%Y", "%d/%m/%y"]):
    if date_str is None:
        return
    datetime_obj = from_str_to_datetime(date_str, supported_formats)
    if datetime_obj:
        return datetime_obj.date()


citycouncil_expenses = {
    "CODARQUIVO": "file_code",  # TODO
    "CODLINHA": "file_line",  # TODO
    "CODUNIDORCAM": "budget_unit",  # TODO sempre 101
    "DTPUBLICACAO": "published_at",
    "DTREGISTRO": "date",
    "CODETAPA": "phase",
    "NUMPROCADM": "number",
    "NUMPROCLIC": "process_number",
    "DSDESPESA": "summary",
    "NMCREDOR": "company_or_person",
    "NUCPFCNPJ": "document",
    "VALOR": "value",
    "DSFUNCAO": "function",
    "DSSUBFUNCAO": "subfunction",
    "DSNATUREZA": "legal_status",  # TODO natureza do TCM-BA
    "DSFONTEREC": "resource",
    "NUMETAPA": "phase_code",  # TODO
    "MODALIDADE": "modality",  # TODO
    "EXCLUIDO": "excluded",  # TODO
}


def to_expense(item):
    functions = {
        "value": currency_to_float,
        "excluded": to_boolean,
        "published_at": from_str_to_date,
        "date": from_str_to_date,
        "phase": get_phase,
    }
    new_item = {}
    for key, value in item.items():
        field = citycouncil_expenses[key]
        value = value.strip()
        new_item[field] = functions.get(field, lambda x: x)(value)
    return new_item
