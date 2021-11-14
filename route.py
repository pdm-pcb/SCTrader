from stantondata import planetary_system, travel_distance


class Port:
    def __init(self):
        self.name = ""
        self.planetary_body = ""
        self.price = 0
        self.refresh_per_minute = 0
        self.max_inventory = 0


class Route:
    def __init__(self, t_purchase_port, t_sale_port,
                 t_units, t_buy_price, t_sell_price,
                 t_best_case_buy, t_best_case_sell,
                 t_worst_case_buy, t_worst_case_sell, name):
        self.purchase_port = t_purchase_port
        self.sale_port = t_sale_port
        self.units = t_units
        self.buy_price = t_buy_price
        self.sell_price = t_sell_price
        self.best_case_buy = t_best_case_buy
        self.best_case_sell = t_best_case_sell
        self.worst_case_buy = t_worst_case_buy
        self.worst_case_sell = t_worst_case_sell

        try:
            purchase_system = planetary_system[t_purchase_port.planetary_body]
            sale_system = planetary_system[t_sale_port.planetary_body]
            self.travel_distance = travel_distance[purchase_system][sale_system]
        except KeyError as ex:
            self.travel_distance = 1
            print(f"Route KeyError {ex} for {name}\n"
                  f"  {t_purchase_port.name} ({t_purchase_port.planetary_body})\n"
                  f"  {t_sale_port.name} ({t_sale_port.planetary_body})\n")

    def total_profit(self):
        profit_per_unit = self.sell_price - self.buy_price
        total_profit = int((profit_per_unit * self.units) / 100)

        return total_profit

    def investment(self):
        profit_per_unit = self.sell_price - self.buy_price
        total_profit = int((profit_per_unit * self.units) / 100)

        return total_profit
