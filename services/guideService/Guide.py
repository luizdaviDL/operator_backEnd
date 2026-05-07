from components.guideComponents.guideComponents import fitzDecode


class Service:
    
    def decodePDF(self, pdf, trip):
        try:
            for i in pdf:
                result = fitzDecode(i.get('data'))

                if not result["ok"]:
                    continue

                text = result["text"]

                if trip in text:
                    return {
                        "finded": True,
                        "filename": i.get('name'),
                        "data": i.get('data')
                    }

            return {"finded": False}

        except Exception as e:
            return {"erro": str(e)}