import azure.functions as func
import logging
from PIL import Image
import io

app = func.FunctionApp()

@app.function_name(name="ImageProcessor")
@app.blob_trigger(arg_name="myblob",
                  path="uploads/{name}",
                  connection="AzureWebJobsStorage")
def process_image(myblob: func.InputStream, outputBlob: func.Out[str]):
    logging.info(f"Processing image: {myblob.name}, Size: {myblob.length} bytes")

    try:
        # تحميل الصورة
        image = Image.open(myblob)

        # تحويل الصورة إلى تدرج الرمادي
        image = image.convert("L")

        # حفظ الصورة في ذاكرة مؤقتة
        output = io.BytesIO()
        image.save(output, format="PNG")
        output.seek(0)

        # حفظ الصورة المعالجة في مجلد `processed`
        outputBlob.set(output.getvalue())

        logging.info(f"Image {myblob.name} processed successfully and saved to processed/")
    
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
