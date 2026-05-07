

def to_treatDecimal(valor):
    if not valor:
        return ""
        
    if "," in valor:
        parte_inteira, parte_decimal = valor.split(",")
        return f"{parte_inteira},{parte_decimal[:2]}"
    
    return valor

def adding_columns(dataframe, invoice, arrival):
    """
    Add business columns and position them correctly.
    """

    try:
        # 🔹 validação inicial
        if dataframe.empty:
            return dataframe

        # -------------------------
        # Fixed Columns
        # -------------------------
        dataframe["FATURAMENTO"] = invoice
        dataframe["CHEGADA"] = arrival
        dataframe["ENTREGA"] = ""

        # After CIDADE
        dataframe["Caixas"] = ""
        dataframe["Peso Liq"] = ""

        # After Preço Bruto
        dataframe["Preço Liq"] = ""
        dataframe["STATUS"] = "PARADO NO CD"
        dataframe["OBSERVAÇÕES"] = f"CARRETA DO DIA {arrival}"

        cols = list(dataframe.columns)

        # -------------------------
        # Insert after CIDADE
        # -------------------------
        if "CIDADE" in cols:
            idx_cidade = cols.index("CIDADE") + 1
            for col in ["Caixas", "Peso Liq"]:
                cols.remove(col)
            cols[idx_cidade:idx_cidade] = ["Caixas", "Peso Liq"]

        # -------------------------
        # Insert after Preço Bruto
        # -------------------------
        if "Preço Bruto" in cols:
            idx_preco = cols.index("Preço Bruto") + 1
            for col in ["Preço Liq", "STATUS", "OBSERVAÇÕES"]:
                cols.remove(col)
            cols[idx_preco:idx_preco] = [
                "Preço Liq",
                "STATUS",
                "OBSERVAÇÕES"
            ]

        # -------------------------
        # Move priority columns to beginning
        # -------------------------
        priority = ["FATURAMENTO", "CHEGADA", "ENTREGA"]

        for col in priority:
            cols.remove(col)

        final_order = priority + cols

        dataframe = dataframe[final_order]

        # ✅ SUCESSO
        return {
            "ok": True,
            "error": None,
            "data": dataframe
        }

    except Exception as e:
        # ❌ ERRO CONTROLADO
        return {
            "ok": False,
            "error": f"Erro na função adding_columns: {str(e)}",
            "data": None
        }


