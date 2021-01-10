import requests
from bs4 import BeautifulSoup
import math

from route import Route, Port


class Commodity:
    def __init__(self, t_name, t_cateogry, t_url):
        self.name = t_name
        self.category = t_cateogry
        self.ports_of_purchase = list()
        self.ports_of_sale     = list()
        self.routes            = list()

        page = requests.get(t_url)
        soup = BeautifulSoup(page.content, "html.parser")

        price_unit_tables = soup.find_all("table")

        if len(price_unit_tables) != 2:
            return

        purchase_table = price_unit_tables[0]
        sale_table     = price_unit_tables[1]

        self.ports_of_purchase = self.build_port_list(purchase_table)
        self.ports_of_sale     = self.build_port_list(sale_table)

    def build_port_list(self, t_port_table):
        port_list = list()

        rows = t_port_table.find_all("tr")
        for row in rows:
            table_data = row.find_all("td")

            port = Port()

            port.planetary_body = table_data[0].text.strip()
            port.planetary_body = " ".join(port.planetary_body.split()[:-1])

            port.name = table_data[1].string.strip()

            try:
                port.price = int(float(table_data[2].string.strip()) * 100)
            except AttributeError:
                port.price = 0

            try:
                port.refresh_per_minute = \
                    math.floor(float(table_data[3].string.strip()))
            except AttributeError:
                port.refresh_per_minute = 0

            try:
                port.max_inventory = int(table_data[4].string.strip())
            except AttributeError:
                port.max_inventory = 0

            port_list.append(port)

        return port_list

    def build_routes(self, t_units, t_profit_per_unit, t_buy_time, t_sell_time):
        self.routes.clear()

        for purchase_port in self.ports_of_purchase:
            best_case_buy = self.best_case(purchase_port, t_units)
            worst_case_buy = self.worst_case(purchase_port, t_units)

            if best_case_buy == -1 or worst_case_buy == -1 or\
               worst_case_buy > t_buy_time:
                continue

            for sale_port in self.ports_of_sale:
                profit_per_unit = sale_port.price - purchase_port.price

                if profit_per_unit < t_profit_per_unit:
                    continue

                best_case_sell = self.best_case(sale_port, t_units)
                worst_case_sell = self.worst_case(sale_port, t_units)

                if best_case_sell == -1 or worst_case_sell == -1 or\
                   worst_case_sell > t_buy_time:
                    continue

                route = Route(purchase_port, sale_port, t_units,
                              purchase_port.price, sale_port.price,
                              best_case_buy, best_case_sell,
                              worst_case_buy, worst_case_sell)

                self.routes.append(route)

        self.routes.sort(key=lambda route: route.total_profit(),
                         reverse=True)

    def worst_case(self, t_port, t_units):
        try:
            worst_case = \
                int(t_units / t_port.refresh_per_minute)
        except ZeroDivisionError:
            worst_case = -1

        return worst_case

    def best_case(self, t_port, t_units):
        if t_port.max_inventory > t_units:
            best_case = 0
        else:
            t_units -= t_port.max_inventory
            try:
                best_case = math.ceil(t_units / t_port.refresh_per_minute)
            except ZeroDivisionError:
                best_case = -1

        return best_case
