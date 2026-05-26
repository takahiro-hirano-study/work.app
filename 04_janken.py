import time
import random
from pathlib import Path
import json

# ファイル作成
p = Path('data') / 'janken_result.json'
p.parent.mkdir(parents=True, exist_ok=True)

if p.exists():
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        print('前回の結果')
        print(f'勝ち:{data.get("勝ち")}, 負け:{data.get("負け")}')
    except Exception as e:
        print('前回のデータの読み込みに失敗しました。')
        print(f'エラー{e}')
else:
    print('前回の入力はありません。')
print()

# 接待成功への返しの関数
def you_win():
    print('→接待成功！ うれしいやろｗ また負けたるで！')

# 接待失敗への返しの関数
def you_lose():  
    print('→接待失敗ｗ 強くてごめんｗ ') 

# ジャンケンした一連の流れの関数
def janken():
    you = input('\nグー, チョキ,パーのどれかを入力して >').strip()
    you = (you.replace('ー', '').replace('!', '').replace('！', '').lower().strip())

    if you in ['グ', 'ぐ', 'g', 'G', '✊']:
        you = 'グー'    
    elif you in ['チョキ', 'ちょき', 'チョキ', 'c', 'C', '✌']:
        you = 'チョキ'  
    elif you in ['パ', 'ぱ', 'パ', 'p', 'P', '✋']:
        you = 'パー' 
    elif any(word in you for word in ['バカ', 'アホ', '暇', 'baka', 'aho', '馬鹿']):
        print('\n名誉棄損や侮辱は控えましょう。')
        return janken() 
    elif any(word in you for word in ['天才', '神', 'かっこいい', 'イケメン']): 
        print('\nありがとう、、、はじめていわれた(泣) ')
        return janken()          
    else:
        print('\n意味分からんW ')
        return janken()
    
    # 接待モードか通常モード選択したときの条件
    if reception_mode:
        enemy_dict = {'グー': 'チョキ', 
                      'チョキ': 'パー',
                      'パー': 'グー'}
        enemy = enemy_dict[you]
    else:
        enemy = random.choice(['グー', 'チョキ', 'パー'])

    print(f'あなた： {you}  相手： {enemy}')

    if you == enemy:
        you_lose()
        return False
    elif (you == 'グー' and enemy == 'チョキ') or \
         (you == 'チョキ' and enemy == 'パー') or\
         (you == 'パー' and enemy == 'グー' ):
        you_win()
        return True
    else:
        you_lose()
        return False   

# メインループ
print('=== 接待じゃんけんへようこそ ===')
print('モードを選べ！')
mode = input('1： 通常モード  2： 完全接待モード >').strip()

if mode == '2':
    reception_mode = True
    print('完全接待モード発動！ いつでも負けたるでｗ')
else:
    reception_mode = False
    print('通常モードで勝負や！') 

win_streak = 0 # 連勝カウント初期化
win_count = 0
lose_count = 0

while True:          
    player_won = janken()

    if player_won:
        win_streak += 1
        if win_streak < 5:
            print(f'おめでとう{win_streak}連勝中！！ 俺の次に強いなｗ')
        elif win_streak == 5:
            print("たくさん勝てて嬉しいやろｗ 【接待】オセロやからな！")
        else:
            print(f'おめでとうｗ {win_streak}連勝中 【接待】した価値はあるわ～')               
    else:
        if win_streak >= 3:
            print(f'{win_streak}連勝でストップやｗ')
        elif win_streak >= 1:
            print(f'連勝ストップ　まだまだ') 
        win_streak  = 0
    if player_won:
        win_count += 1
    else:
        lose_count += 1
    print(f'通算戦績\n勝ち: {win_count}, 負け: {lose_count}')  

    print('\nもっかいしたってもええで？ いつでも負けたるわｗ')
    again = input('yを入力して続ける、nを入力するとやめれるで！').strip().lower()

    if again in ['n', 'no', 'NO', 'N', 'ｎ', 'ね', 'やめる', '終了', '終わり', 'おわり','owari']:
       print('\nやめるん？')
       print('次は手加減してあげる')
       time.sleep(1)
       break
    elif any(word in again for word in['バカ', 'アホ', '暇', 'baka', 'aho', '馬鹿']):
        print('\n名誉棄損や侮辱は控えましょう。')
    elif any(word in again for word in ['天才', '神', 'かっこいい', 'イケメン', '師匠']):
        print('\nありがとう、、、はじめていわれた(泣) ')
    else:
        print('\nやることないねんなｗ')
        time.sleep(1)

new_data = {'勝ち': win_count,'負け': lose_count}  

p.write_text(json.dumps(new_data,ensure_ascii=False, indent=2),encoding='utf-8')
print('\n今回の結果を保存しました。')
