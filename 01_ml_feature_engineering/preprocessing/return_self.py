'''
参照 https://qiita.com/helloworld-yoppy/questions/0b11bc6694295a577340

return selfの必要性について質問をしたいです。

オープンソースを見ているとクラス内の関数の最後に「return self」と設定しているコードが多々あります。
しかし、return selfを記述しないくてもself内の変数の値が受け継がれているようなので、return selfは必要ないのでは、ないでしょうか？

return selfが記述されている理由についてお聞きしたいです。

よろしくお願いいたします。
'''
class sample:
    def __init__(self):
        self.hello()
        print(f"hoge：{self.hoge}")
        print(f"hogehoge：{self.hogehoge}")

    def hello(self):
        self.hoge = 1
        self.hogehoge = 1
        return self

    def hello2(self):
        print(f"hoge：{self.hoge + 1}")
        print(f"hogehoge：{self.hogehoge + 1}")
        return self


s = sample()
s.hello2()


'''
=>hoge：1
=>hogehoge：1
=>hoge：2
=>hogehoge：2
'''


class sample:
    def __init__(self):
        self.hello()
        print(f"hoge：{self.hoge}")
        print(f"hogehoge：{self.hogehoge}")

    def hello(self):
        self.hoge = 1
        self.hogehoge = 1

    def hello2(self):
        print(f"hoge：{self.hoge + 1}")
        print(f"hogehoge：{self.hogehoge + 1}")


s = sample()
s.hello2()

'''
=>hoge：1
=>hogehoge：1
=>hoge：2
=>hogehoge：2
'''

'''
blue32a@blue32a
2021年06月05日に投稿

more_horiz
おそらくメソッドチェーンが出来るようにするためだと思います。
メソッドチェーンというのは次のような書き方です。
'''

object.aaa().bbb().ccc()
#記載されているコードだと次のような書き方が可能です。

s = sample()
s.hello().hello2()

#hello()はselfを返すので、次はself.hello2()と解釈されます。
#selfにはhello2()があるので、これは正しく実行されます。