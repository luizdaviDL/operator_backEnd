from components.nfeComponents.Components import decodePDFToNfe,group_by_client
from components.generics.GenericComponents import adding_columns


class Service:
    
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