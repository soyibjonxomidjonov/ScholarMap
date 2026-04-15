from google import genai





MY_KEY = "AIzaSyA06vnIj81lqLgVMqxlZNLmu0RNybc6ipk"

def file_to_text(api, file_path):
    # API kalitni bu yerga qo'ying
    MY_KEY = "AIzaSyA06vnIj81lqLgVMqxlZNLmu0RNybc6ipk"

    client = genai.Client(api_key=MY_KEY)

    try:
        print("Siz foydalana oladigan modellar ro'yxati:")
        print("-" * 30)

        # Modellarni ko'rishning eng oddiy yo'li
        for model in client.models.list():
            # Yangi SDKda modelning nomi model.name da bo'ladi
            print(f"Model: {model.name}")
        # Sizning ro'yxatingizdagi 'gemini-flash-latest' modelini ishlatamiz
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents="Menga rasmni sozlarni olib translate qilib jo'natish kerak shuni qila olasanmi?"
        )

        print("-" * 20)
        print("Javob:")
        print(response.text)
        print("-" * 20)

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")