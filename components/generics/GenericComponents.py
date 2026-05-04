from tkinter import filedialog
import tkinter as tk

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
        if dataframe is None or dataframe.empty:
            return {
                "ok": False,
                "error": "DataFrame vazio ou inválido",
                "data": None
            }

        # -------------------------
        # 🔹 adicionar colunas fixas
        # -------------------------
        dataframe["FATURAMENTO"] = invoice
        dataframe["CHEGADA"] = arrival
        dataframe["ENTREGA"] = ""

        dataframe["Caixas"] = ""
        dataframe["Peso Liq"] = ""

        dataframe["Preço Liq"] = ""
        dataframe["STATUS"] = "PARADO NO CD"
        dataframe["OBSERVAÇÕES"] = f"CARRETA DO DIA {arrival}"

        cols = list(dataframe.columns)

        # -------------------------
        # 🔹 inserir após CIDADE
        # -------------------------
        if "CIDADE" in cols:
            idx_cidade = cols.index("CIDADE") + 1

            for col in ["Caixas", "Peso Liq"]:
                if col in cols:
                    cols.remove(col)

            cols[idx_cidade:idx_cidade] = ["Caixas", "Peso Liq"]

        # -------------------------
        # 🔹 inserir após Preço Bruto
        # -------------------------
        if "Preço Bruto" in cols:
            idx_preco = cols.index("Preço Bruto") + 1

            for col in ["Preço Liq", "STATUS", "OBSERVAÇÕES"]:
                if col in cols:
                    cols.remove(col)

            cols[idx_preco:idx_preco] = [
                "Preço Liq",
                "STATUS",
                "OBSERVAÇÕES"
            ]

        # -------------------------
        # 🔹 mover colunas prioritárias
        # -------------------------
        priority = ["FATURAMENTO", "CHEGADA", "ENTREGA"]

        for col in priority:
            if col in cols:
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


def save_dataframe_to_excel(dataframe):
    """
    Open a save dialog window and allow the user
    to choose where to save the Excel file.
    """

    if dataframe.empty:
        print("DataFrame is empty. Nothing to save.")
        return None

    # Hide main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open save dialog
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Save Excel File"
    )

    if not file_path:
        print("Save cancelled.")
        return None

    # Save file
    dataframe.to_excel(file_path, index=False)

    print(f"File saved successfully at: {file_path}")
    return file_path
