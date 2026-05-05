from components.guideComponents import fitzDecode


class Service:
    
    def decodePDF(self, pdf, trip):
        try:
            for i in pdf:
                text = fitzDecode(i.get('data'))

                if trip in text:
                    return {
                        "finded": True,
                        "filename": i.get('name'),  # ← Nome do arquivo
                        "data": i.get('data')
                    }
                else:
                    return {"finded": False}

        except Exception as e:
            return {"erro": str(e)}