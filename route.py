from stantondata import planetary_system, travel_distance


class Port:
    def __init(self):
        self.name = ""
        self.planetary_body = ""
        self.price = 0
        self.refresh_per_minute = 0
        self.max_inventory = 0


class Route:
    def __init__(self, a_purchase_port, a_sale_port,
                 a_units, a_buy_price, a_sell_price,
                 a_best_case_buy, a_best_case_sell,
                 a_worst_case_buy, a_worst_case_sell):
        self.purchase_port = a_purchase_port
        self.sale_port = a_sale_port
        self.units = a_units
        self.buy_price = a_buy_price
        self.sell_price = a_sell_price
        self.best_case_buy = a_best_case_buy
        self.best_case_sell = a_best_case_sell
        self.worst_case_buy = a_worst_case_buy
        self.worst_case_sell = a_worst_case_sell

        try:
            purchase_system = planetary_system[a_purchase_port.planetary_body]
            sale_system = planetary_system[a_sale_port.planetary_body]
            self.travel_distance = travel_distance[purchase_system][sale_system]
        except KeyError as ex:
            print(f"KeyError {ex}\n"
                  f"{a_purchase_port.name} ({a_purchase_port.planetary_body})\n"
                  f"{a_sale_port.name} ({a_sale_port.planetary_body})\n")
            self.travel_distance = 1

    def total_profit(self):
        profit_per_unit = self.sell_price - self.buy_price
        total_profit = int((profit_per_unit * self.units) / 100)

        return total_profit

    def investment(self):
        profit_per_unit = self.sell_price - self.buy_price
        total_profit = int((profit_per_unit * self.units) / 100)

        return total_profit
