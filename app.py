from flask import Flask, render_template, request

import time
import os

app = Flask(__name__)

# Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# โหลดทะเบียนจาก data.txt
def load_data():
    path = os.path.join(app.root_path, 'data.txt')
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        # strip, drop empty lines
        return [line.strip() for line in f if line.strip()]

@app.route('/', methods=['GET', 'POST'])
def index():
    default_data = load_data()
    sorted_data = []
    result = None
    elapsed = 0

    if request.method == 'POST':
        # ถ้ามีการแก้ไข textarea จะใช้ค่านั้น ไม่งั้นใช้ default_data
        raw = request.form.get('data','').strip()
        arr = raw.splitlines() if raw else default_data
        arr = [line.strip() for line in arr if line.strip()]

        # ค้นหา
        key = request.form.get('search','').strip()

        # เรียง + วัดเวลา
        t0 = time.time()
        sorted_data = bubble_sort(arr.copy())
        elapsed = round(time.time() - t0, 6)

        # ค้นหา exact ก่อน ถ้าไม่เจอ ลอง substring
        if key:
            if key in sorted_data:
                pos = sorted_data.index(key) + 1
                result = f"พบทะเบียน {key} ในลำดับที่ {pos}"
            else:
                matches = [p for p in sorted_data if key in p]
                if matches:
                    result = f"พบทะเบียนที่มี '{key}': {', '.join(matches[:5])}"
                else:
                    result = f"ไม่พบทะเบียน {key} ในรายการ"

    return render_template(
      'index.html',
      data_input=default_data,
      sorted_data=sorted_data,
      time=elapsed,
      result=result
    )

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # ดึง port จากระบบ
    app.run(debug=False, host='0.0.0.0', port=port)  # ต้องใช้ 0.0.0.0