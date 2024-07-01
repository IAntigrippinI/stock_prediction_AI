class API:
    def __init__(self, keys: list) -> None:
        self.keys = keys
        self.ind_key = 0

    def get_key(self):
        return self.keys[self.ind_key]

    def next_key(self):
        if self.ind_key >= len(self.keys) - 1:
            print("keys is over")
            return self.keys[self.ind_key]
        else:
            self.ind_key += 1
            return self.keys[self.ind_key]
