import base64
import fitz
import re
import pandas as pd
import unicodedata
from itertools import groupby
from components.generics.GenericComponents import to_treatDecimal


STOPWORDS = {
    "supermercado",
    "supermercados",
    "mercado",
    "mercados",
    "ltda",
    "lt",
    "sa",
    "s",
    "comercio",
    "industria",
    "e",
    "do",
    "da",
    "dos",
    "das",
    "super",
}


REGEXNFE = {
    "EMBARQUE": re.compile(r'NR EMB:\s*(\d+)'),
    "VIAGEM": re.compile(r'Viagem NR\s*(\d+)'),
    "NOTA FISCAL": re.compile(r'\n(\d+)-20'),
    "COD CLIENTE": re.compile(r'Cod Cliente\s*(\d+)'),
    "CLIENTE": re.compile(r'NOME/RAZÃO SOCIAL\s*(.+)'),
    "ENDEREÇO": re.compile(r'ENDEREÇO\s*(.+)'),
    "BAIRRO": re.compile(r'BAIRRO/DISTRITO\s*(.+)'),
    "CIDADE": re.compile(r'MUNICÍPIO\s*(.+)'),
    "Peso Bruto": re.compile(
        r'PESO BRUTO[\s\S]*?(\d{1,3}(?:\.\d{3})*,\d+)\s*KG'
    )
}


def decodePDFToNfe(value):
    try:
        if not value:
            return {
                "ok": False,
                "error": "Valor base64 vazio",
                "data": None
            }

        # 🔹 decode
        try:
            pdf_data = base64.b64decode(value)
        except Exception as e:
            return {
                "ok": False,
                "error": f"Erro ao decodificar base64: {str(e)}",
                "data": None
            }

        # 🔹 abrir PDF
        try:
            doc = fitz.open(stream=pdf_data, filetype="pdf")
        except Exception as e:
            return {
                "ok": False,
                "error": f"Erro ao abrir PDF: {str(e)}",
                "data": None
            }

        # 🔹 extrair texto
        texto = "\n".join(page.get_text() for page in doc)

        dados = {}

        # 🔹 extrair campos
        for campo, pattern in REGEXNFE.items():
            try:
                match = pattern.search(texto)

                if match:
                    valor = match.group(1).strip()

                    if campo == "Peso Bruto":
                        valor = to_treatDecimal(valor)

                    dados[campo] = valor
                else:
                    dados[campo] = ""

            except Exception:
                dados[campo] = ""

        # 🔥 VALIDAÇÃO DOS CAMPOS OBRIGATÓRIOS
        campos_faltando = [
            campo for campo, valor in dados.items() if not valor
        ]

        if campos_faltando:
            return {
                "ok": False,
                "error": f"PDF inválido. Envie apenas arquivos de Nota Fiscal Eletrônica (NF-e)",
                "data": None
            }

        # ✅ sucesso
        return {
            "ok": True,
            "error": None,
            "data": dados
        }

    except Exception as e:
        return {
            "ok": False,
            "error": f"Erro geral: {str(e)}",
            "data": None
        }    
    

def group_by_client(records):
    """
    Group dynamically by relevant client name.
    """

    try:
        # 🔹 validação inicial
        if not records or not isinstance(records, list):
            return {
                "ok": False,
                "error": "Records inválido ou vazio",
                "data": None
            }

        # 🔹 criar chave dinâmica
        for record in records:
            try:
                record["_CLIENT_KEY"] = normalize_client_name(
                    record.get("CLIENT", "")
                )
            except Exception:
                record["_CLIENT_KEY"] = ""  # fallback seguro

        # 🔹 ordenar
        try:
            records_sorted = sorted(
                records,
                key=lambda x: x["_CLIENT_KEY"]
            )
        except Exception as e:
            return {
                "ok": False,
                "error": f"Erro ao ordenar registros: {str(e)}",
                "data": None
            }

        grouped_data = []

        # 🔹 agrupar
        try:
            for _, items in groupby(
                records_sorted,
                key=lambda x: x["_CLIENT_KEY"]
            ):
                grouped_data.extend(list(items))
        except Exception as e:
            return {
                "ok": False,
                "error": f"Erro ao agrupar registros: {str(e)}",
                "data": None
            }

        # 🔹 limpar campo auxiliar
        for item in grouped_data:
            item.pop("_CLIENT_KEY", None)

        # ✅ SUCESSO
        return {
            "ok": True,
            "error": None,
            "data": pd.DataFrame(grouped_data)
        }

    except Exception as e:
        return {
            "ok": False,
            "error": f"Erro geral em group_by_client: {str(e)}",
            "data": None
        }

def normalize_client_name(name):
    if not name:
        return ""

    # Remove accents
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))

    # Lowercase
    name = name.lower()

    # Remove punctuation
    name = re.sub(r"[^\w\s]", " ", name)

    # Split words
    words = name.split()

    # Remove stopwords
    filtered_words = [
        word for word in words
        if word not in STOPWORDS
    ]

    # If nothing remains, fallback to original cleaned name
    if not filtered_words:
        return name.strip()

    # Use first relevant word as grouping key
    return filtered_words[0]
