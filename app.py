from flask import Flask, render_template, request
import time
import os

app = Flask(__name__)

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


@app.route('/', methods=['GET', 'POST'])
def index():
    sorted_data = []
    search_result = None
    elapsed_time = 0

    # โหลดข้อมูลเริ่มต้นจาก data.txt
    data_file = os.path.join(app.root_path, 'data.txt')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            default_data = [line.strip() for line in f if line.strip()]
    else:
        default_data = []

    if request.method == 'POST':
        # อ่านจาก textarea หรือใช้ default_data ถ้าว่าง
        raw = request.form.get('data', '').strip()
        input_data = raw.splitlines() if raw else default_data
        # ทำความสะอาดข้อมูลแต่ละบรรทัด
        input_data = [line.strip() for line in input_data if line.strip()]

        search_input = request.form.get('search', '').strip()

        # เรียงข้อมูลด้วย Heap Sort
        start = time.time()
        sorted_data = heap_sort(input_data.copy())
        elapsed_time = round(time.time() - start, 6)

        # ค้นหาทะเบียน
        if search_input:
            if search_input in sorted_data:
                pos = sorted_data.index(search_input) + 1
                search_result = f"พบทะเบียน {search_input} ในลำดับที่ {pos}"
            else:
                search_result = f"ไม่พบทะเบียน {search_input} ในรายการ"

    return render_template('index.html', data_input=default_data,
                           sorted_data=sorted_data,
                           time=elapsed_time,
                           result=search_result)


if __name__ == '__main__':
    app.run(debug=True, port=5006)
