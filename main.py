from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

# INICIALIZACIÓN
app = FastAPI()

# CONFIGURACIÓN DE SEGURIDAD
# En la nube usaremos "Variables de Entorno" para no poner la clave a fuego en el código
openai.api_key = os.getenv("OPENAI_API_KEY")

# DEFINIMOS EL FORMATO DE DATOS QUE EL CLIENTE NOS ENVIARÁ
class CampaignRequest(BaseModel):
    tema: str
    tono: str = "Lujoso y Profesional"
    estilo_visual: str = "Fotografía de estudio, luz suave, colores pasteles"

# EL "ENDPOINT" (LA PUERTA DE ENTRADA DE TU SISTEMA)
@app.post("/generar-campana")
async def generar_campana(data: CampaignRequest):
    
    try:
        # 1. Generar Imagen
        prompt_imagen = f"Imagen publicitaria para clínica de estética sobre {data.tema}. {data.estilo_visual}. 8k, realista."
        
        response_img = openai.images.generate(
            model="dall-e-3",
            prompt=prompt_imagen,
            n=1,
            size="1024x1024"
        )
        url_imagen = response_img.data[0].url

        # 2. Generar Texto
        prompt_texto = f"Crea un post de Instagram para una clínica sobre '{data.tema}'. Tono: {data.tono}. Usa emojis elegantes."
        
        response_text = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt_texto}]
        )
        caption = response_text.choices[0].message.content

        # 3. Enviar Respuesta JSON
        return {
            "status": "success",
            "imagen_url": url_imagen,
            "caption": caption,
            "tema": data.tema
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PARA VERIFICAR QUE EL SERVIDOR ESTÁ VIVO
@app.get("/")
def read_root():
    return {"status": "Sistema AestheticFlow Online"}
