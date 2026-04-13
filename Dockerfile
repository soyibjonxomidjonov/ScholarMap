# Use the official Python image from the Docker Hup

FROM python:3.12-slim
#Bunda pythonni kerakli versiyasi yoziladi

#Ser environment variables

ENV PYTHONDONTWRITEBYTECODE 1
# Standart shunday yoziladi
ENV PYTHONUNBUFFERED 1
#Standart shunday yoziladi

WORKDIR /app
# Bunda container yaratilganda uni ichida kichkina app degan papkaga tushadi

COPY requirements.txt .
# Bunda requirments.txt nusxa olib contaninerga tashlanadi
RUN pip install --upgrade pip  # <--- Buni qoshing
RUN pip install --no-cache-dir -r requirements.txt
# Shunday qilib o'rnatiladi



COPY . /app/

#Bunda dockerga loyihani hamma fayllarni containerga tashlanadi
#Bunda hamma narsani o'rnatib app ni ichiga soldi"""

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#Va bunda cmd da run qilish
#uchun shunday yoziladi bu globalni kompyuterda run qilinadi emas balki container ichida run qilinadi