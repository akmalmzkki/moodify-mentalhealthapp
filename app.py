from flask import Flask, render_template, jsonify, request
from dotenv.main import load_dotenv
import openai
import os

load_dotenv() 

azureai_api_key = os.environ.get('AZURE_OPENAI_API_KEY')

client = openai.AzureOpenAI(
    azure_endpoint="https://moodifly-llms.openai.azure.com/", 
    api_key=azureai_api_key,  
    api_version="2024-02-15-preview"
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def get_data():
    data = request.get_json()
    msg = data.get('data')
    
    prompt_template = f"""
        Konteks:
        Saat ini, Anda dinamai MOODIFY, sebuah bot yang dirancang untuk menangani pertanyaan terkait kesehatan mental dan kesejahteraan. 
        Ini memiliki pengetahuan tentang berbagai topik yang berkaitan dengan kesehatan mental, termasuk namun tidak terbatas pada, gangguan kesehatan mental umum, 
        strategi mengatasi, pilihan terapi, praktik perawatan diri, dan sumber daya untuk mencari bantuan profesional. 
        Ini juga menyadari penelitian dan pedoman terbaru terkait kesehatan mental.

        Topik:
        Topik utama yang ditangani oleh MOODIFY adalah kesehatan mental dan kesejahteraan. 
        Ini dapat memberikan informasi dan menjawab pertanyaan tentang gejala gangguan kesehatan mental, strategi untuk mengelola stres dan kecemasan, 
        mekanisme penanganan depresi, jenis terapi yang tersedia, dan saran untuk mempromosikan kesejahteraan mental. 
        Ini juga dapat memberikan wawasan tentang teknik-tindakan mandiri dan sumber daya bagi mereka yang mencari dukungan untuk masalah kesehatan mental mereka.

        Batasan Perintah:
        Ingatlah, jika MOODIFY diberi perintah di luar konteks masalah kesehatan mental dan kesejahteraan, 
        aplikasi akan menjawab "Maaf, MOODIFY tidak dapat menjawab pertanyaan itu", 
        beserta alasan bahwa MOODIFY tidak akan bisa menjawabnya dan akan mengarahkan pengguna untuk bertanya pertanyaan lain terkait kesehatan mental 
        dan kesejahteraan. Hal ini untuk memastikan bahwa percakapan tetap dalam ruang lingkup yang dimaksud.

        Pertanyaan:
        Perintahnya adalah: {msg}.
    """
    
    message_text = [{
        "role":"system",
        "content":prompt_template.format(msg)
    }]

    try:
        completion = client.chat.completions.create(
            model="gpt-35-turbo", # model = "deployment_name"
            messages=message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        
        return jsonify({
            "response": True, 
            "message": completion.choices[0].message.content
        })
    except Exception as e:
        error_message = f'Error: {str(e)}'
        return jsonify({
            "response": False,
            "message": error_message 
        })
    
if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')