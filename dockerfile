# استخدم صورة بايثون رسمية
FROM python:3.11-slim

# حدد مجلد العمل داخل الكونتينر
WORKDIR /app

# انسخ كل الملفات والمجلدات من المشروع داخل /app
COPY . /app

# CMD: شغل الملف اللي تحب (مثلاً serveur.py)
CMD ["python", "serveur/serveur.py"]
