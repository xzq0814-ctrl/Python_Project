from datetime import datetime

class Merchandise:
    def __init__(self, name, price, num, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.name = name
        self.price = price
        self.num = num
        self.time = time
    def __str__(self):
        return f"商品名称：{self.name} | 商品价格：{self.price} | 商品数量：{self.num} | 添加时间：{self.time}"

class ShopCart:
    wel = "购物车界面来咯"
    def __init__(self):
        self.goods_list = []
    def add_goods(self):
        print("增加商品名称，想添加重复的标序号")
        name = input("想买啥，说：").strip()
        for g in self.goods_list:
            if g.name == name:
                print("已经有了，换个别的")
                return
        price = input("多钱?：").strip()
        num = input("买多少：").strip()
        item = Merchandise(name, price, num)
        self.goods_list.append(item)
        print("ok,给我钱，我帮你买")
    def change_goods(self):
        name = input("要改哪个商品：")
        for g in self.goods_list:
            if g.name == name:
                print(g)
                price = input("再输入价格和数量,要不给你改错了。\n价格：")
                num = input("数量：")
                if g.price == price and g.num == num:
                    g.name = input("改吧，名称：")
                    g.price = input("价格：")
                    g.num = input("数量：")
                    print("修改完成")
                    return
        print("没找着")
    def delete_goods(self):
        print("哪个不想买了，钱先给我再删。")
        name = input("名称：")
        for g in self.goods_list:
            if g.name == name:
                self.goods_list.remove(g)
                print("ok，删完了，就和她当初删你一样果断。")
                return
        print("没找着，你再研究研究")
    def show_goods(self):
        for g in self.goods_list:
            print(g)
        print("看啥啊，不买别看")
    def run_shop(self):
        print(f"{self.wel}")
        while True:
            print()
            print("++ ++ ++ ++ ++ ++ ++  输入序号进行操作哦~ ++ ++ ++ ++ ++ ++ ++")
            print("++1.添加商品  2.修改商品  3.删除商品  4.查询商品  5.退出系统  6.++")
            print("++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++ ++")
            choice = input("想干啥：")
            try:
                match choice:
                    case "1":
                        self.add_goods()
                    case "2":
                        self.change_goods()
                    case "3":
                        self.delete_goods()
                    case "4":
                        self.show_goods()
                    case "5":
                        print("加纳")
                        break
                    case "6":
                        print("哈哈，这个没有啊，这个不行有")
                    case _:
                        print("听得懂人话不")
            except Exception:
                print("整坏了赔钱")
if __name__ == '__main__':
    it = ShopCart()
    it.run_shop()