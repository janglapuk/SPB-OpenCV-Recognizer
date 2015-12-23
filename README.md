# Setup

1. OpenCV
   Silakan download pada laman http://opencv.org/
   
2. Clone repo
```
cd ~
mkdir github
cd github
git clone https://github.com/janglapuk/SPB-OpenCV-Recognizer.git
cd SPB-OpenCV-Recognizer
```
   
3. Gunakan virtual environment
   Asumsikan anda memiliki virtual environment ([virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)) dengan interpreter Python versi 3.x dengan nama `cv3`
```
workon cv3
```
   Pastikan anda beralih menggunakan Python versi >= 3.4 dengan memeriksa versi interpreter
```
python --version
```
   dengan output:
```
Python 3.5.1
```

4. Install requirements
```
pip install -r requirements.txt
```

5. Jalankan aplikasi
```
cd src
python main.py
```

# Screenshot
### Aplikasi utama
[![MAIN APP](img/mainapp.jpg)]