import datetime

# 餐廳菜單（字典：菜名 → 價格與類別）
menu = {
    "骰子牛": {"price": 250, "category": "主餐"},
    "明太子烏龍麵": {"price": 150, "category": "主餐"},
    "雞白湯拉麵": {"price": 165, "category": "主餐"},
    "鹽可頌": {"price": 80, "category": "前菜"},
    "味噌湯": {"price": 70, "category": "湯品"},
    "南瓜濃湯": {"price": 80, "category": "湯品"},
    "玉米濃湯": {"price": 75, "category": "湯品"},
    "抹茶鮮奶茶": {"price": 100 , "category": "飲料"},
    "氣泡水": {"price": 60, "category": "飲料"},
    "H2O": {"price": 20, "category": "飲料"}
}

order = {}  # 訂單：菜名 → 數量


#功能區
def show_menu():
    print("\n=== 今日菜單 ===")
    for name, info in menu.items():
        print(f"{name} - ${info['price']} ({info['category']})")


def show_by_category():
    print("\n=== 依類別顯示 ===")
    categories = {}
    for name, info in menu.items():
        cat = info["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(name)

    for cat, dishes in categories.items():
        print(f"\n{cat}:")
        for dish in dishes:
            print(f" - {dish} (${menu[dish]['price']})")


def add_to_order(item, quantity):
    if item in menu.keys():
        order[item] = order.get(item, 0) + quantity
        print(f"✅ 已加入：{item} x{quantity}")
    else:
        print("❌ 沒有這道菜！")


def remove_from_order(item):
    if item in order:
        del order[item]
        print(f"❎ 已刪除 {item}")
    else:
        print("❌ 訂單中沒有這道菜！")


def calc_total(is_member=False, save_receipt=False):
    total = 0
    lines = []
    lines.append("====== 餐廳收據 ======\n")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"時間：{now}\n\n")

    if not order:
        print("⚠️ 尚未點餐！")
        return 0

    lines.append("品項\t數量\t小計\n")
    print("\n=== 訂單明細 ===")
    for item, qty in order.items():
        price = menu.get(item, {}).get("price", 0)
        subtotal = price * qty
        print(f"{item} x{qty} = ${subtotal}")
        lines.append(f"{item}\t{qty}\t${subtotal}\n")
        total += subtotal

    if is_member:
        discount = total * 0.1
        total *= 0.9
        lines.append(f"\n會員折扣：- ${discount:.2f}\n")
        print(f"\n🪪 會員折扣 -${discount:.2f}")

    lines.append(f"\n💰 總金額：${total:.2f}\n")
    print(f"\n💰 總金額：${total:.2f}")

    #是否要儲存收據
    if save_receipt:
        filename = f"receipt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"\n🧾 收據已儲存：{filename}")

    return total


def add_new_dish(name, price, category):
    menu.update({name: {"price": price, "category": category}})
    print(f"🍽️ 新增菜品：{name} - ${price} ({category})")


#主程式
while True:
    print("\n咪咪貓貓今日吃什麼")
    print("1. 顯示菜單")
    print("2. 依類別顯示")
    print("3. 新增糧食")
    print("4. 放入貓貓碗")
    print("5. 又不想吃這個了")
    print("6. 查看總金額")
    print("7. 結帳並離開")
    print("8. 查看貓貓碗內容")

    choice = input("請輸入選項：")

    if choice == "1":
        show_menu()
    elif choice == "2":
        show_by_category()
    elif choice == "3":
        name = input("糧食：")
        price = int(input("價格："))
        cat = input("類別：")
        add_new_dish(name, price, cat)
    elif choice == "4":
        item = input("輸入菜名：")
        qty = int(input("數量："))
        add_to_order(item, qty)
    elif choice == "5":
        item = input("要刪除的菜名：")
        remove_from_order(item)
    elif choice == "6":
        member = input("是否為會員？(y/n)：").lower() == "y"
        calc_total(member)
    elif choice == "7":
        member = input("是否為會員？(y/n)：").lower() == "y"
        calc_total(member, save_receipt=True)
        print("👋 感謝光臨！")
        break
    elif choice == "8":
        print("\n貓貓碗內容")
        if not order:
            print("（還沒放進任何東西喵）")
        else:
            for item, qty in order.items():
                print(f"{item} x{qty}")
    else:
        print("❌ 請輸入正確選項！")
