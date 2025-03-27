import azure.functions as func
import logging
from PIL import Image
import io

app = func.FunctionApp()

@app.function_name(name="ImageProcessor")
@app.route(route="process-image", methods=["POST"])
def process_image(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing image...")

    try:
        # الحصول على الصورة من الطلب
        image_data = req.get_body()
        image = Image.open(io.BytesIO(image_data))

        # تحويل الصورة إلى تدرج الرمادي
        image = image.convert("L")

        # حفظ الصورة المعدلة في ذاكرة مؤقتة
        output = io.BytesIO()
        image.save(output, format="PNG")
        output.seek(0)

        return func.HttpResponse(output.read(), mimetype="image/png")
    
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return func.HttpResponse(f"Error processing image: {str(e)}", status_code=500)
