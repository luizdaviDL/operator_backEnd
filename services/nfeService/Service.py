from components.nfeComponents.Components import decodePDFToNfe,group_by_client,decodePDF
from components.generics.GenericComponents import adding_columns


class NfeService:
    
 
    def shearch_by_note(self, inputPdfs, valueInput):

        try:

            for pdf in inputPdfs:

                decoded_data = decodePDF(pdf['data'], valueInput, pdf['name'])

                # erro ao decodificar
                if not decoded_data.get("ok", True):
                    continue

                # encontrou
                if decoded_data.get("finded"):
                    return {
                        "ok": True,
                        "finded": True,
                        "status": "Nota achada com sucesso",
                        "data": decoded_data.get("data"),
                        "filename": decoded_data.get("filename"),
                    }

            # não encontrou
            return {
                "ok": False,
                "finded": False,
                "status": "Nota fiscal não encontrada"
            }

        except Exception as e:

            return {
                "ok": False,
                "finded": False,
                "status": str(e)
            }
    
    def treating_nfe_piso(self, inputPdfs, invoiceInput, arrivalInput):

        decoded_records = []
        
        for pdf in inputPdfs:
            decoded_data = decodePDFToNfe(pdf)

            if not decoded_data["ok"]:
                return decoded_data

            decoded_records.append(decoded_data["data"])
                
        groupValues = group_by_client(decoded_records)

        if not groupValues["ok"]:
            return groupValues

        addingColumns = adding_columns(
            groupValues["data"],
            invoiceInput,
            arrivalInput
        )

        if not addingColumns["ok"]:
            return addingColumns

      #  save_dataframe_to_excel(addingColumns["data"])
                
        return {
            "ok": True,
            "data": addingColumns["data"].to_dict(orient="records")
        }