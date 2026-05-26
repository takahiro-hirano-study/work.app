from pathlib import Path
import json

file_path = Path('data / last_input.json')
file_path.parent.mkdir(parents=True, exist_ok=True)


# 前回の結果を表示
if file_path.exists():
    try:
        data = json.loads(file_path.read_text(encoding='utf-8'))
        print('前回の結果')
        print(f"機種名: {data.get('機種名')}")
        print(f"1台あたりの秒数: {data.get('1台あたりの秒数')}")
    except Exception as e:
        print('前回のデータ読み込みに失敗しました。') 
        print(f'エラー: {e}') 
else:
    print('前回の入力はありません。')  
print()
                                               
#　入力関数
def input_int(prompt):
  while True:
        try:
            value = input(prompt)
            return int(value)
        except ValueError:
            print('数値のみ入力してください')    

def nyuuryoku():
    global part_name, prod_qty, qty, time_min

    print('部品名, 生産台数A, 数B, 時間(分)を記入してください')
    while True:
        part_name = input('機種名: ')
        if part_name in ['A', 'B', 'C']:
            break
        print('もう一度、入力してください。')
    prod_qty = input_int('生産台数A >')
    qty = input_int('数B >')
    time_min = input_int('時間(分) >')           

# メインループ
nyuuryoku()

# 理想時間
part_dict = {'A' :6, 'B' :5, 'C' :3,}   
ideal_time = part_dict[part_name]

# 計算
class WorkCount:
    def __init__ (self, part_name: str, prod_qty: int, qty: int, time_min: int):
        """コンストラクター(初期化)"""
        self.part_name =part_name                         #部品名
        self.prod_qty = prod_qty                          #生産台数
        self.qty = qty                                    #数
        self.time_min = time_min  

    def calculate_cycletime(self):
        total_items = self.prod_qty * self.qty
        if total_items == 0:
            return 0
        return self.time_min / total_items

work = WorkCount(part_name, prod_qty, qty, time_min)
real_cycletime = work.calculate_cycletime()

# 結果表示 
print(f'機種名: {work.part_name}')
print(f'1台あたりの秒数{real_cycletime:3f}分')
print(f'理想のタイムは{ideal_time}分です')

if real_cycletime < ideal_time:
    print('速いです！この調子で仕事しましょう！')
elif ideal_time < real_cycletime:
    print('遅いです、、、 早くしましょう！')
elif real_cycletime == ideal_time:
    print('順調です！')
else :
    print('エラー')

new_data = {
    '機種名': part_name,
    '1台あたりの秒数': real_cycletime,   
}

file_path.write_text(json.dumps(new_data, ensure_ascii=False, indent=2),encoding='utf-8')

print('今回の結果を保存しました。次回表示します。')


    


   

