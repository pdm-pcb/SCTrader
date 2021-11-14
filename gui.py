import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
import enum
import time
from collections import OrderedDict

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from commodity import Commodity


class MaxLength(enum.Enum):
    CATEGORY  = "Agricultural Supply"
    COMMODITY = "Revenant Tree Pollen"
    ROUTES    = "Routes"
    PORT      = "Reclamation & Disposal Orinth (Hur)"
    TRAVEL    = "00 minutes"
    PROFIT    = "0,000,000 aUEC"
    UNITS     = "0,000,000"
    BUY_SELL  = "000.00"
    ROI       = "00.00%"
    TIME      = "0000-0000"


class GUI():
    def __init__(self, t_ship_data):
        self.commodities_dict = dict()
        self.ship_data = t_ship_data

        self.root = tk.Tk()
        self.root.title("Star Citizen Trade Routes")
        self.root.resizable(False, False)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        custom_font = tk.font.Font(font=("Cantarell", 10))

        self.root.option_add("*Font", custom_font)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=custom_font)
        style.configure("Treeview", font=custom_font,
                        rowheight=custom_font.metrics("linespace") + 5)
        style.configure("TButton", font=custom_font)

        # CONFIGURATION WIDGETS
        config_frame = ttk.Frame(self.root, padding="5 5 5 0", relief="sunken")
        config_frame.grid(row=0, column=0, columnspan=1)

        ship_label = ttk.Label(config_frame, text="Ship")
        ship_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.ship_combobox = ttk.Combobox(config_frame,
                                          values=list(self.ship_data.keys()))
        self.ship_combobox.current(8)
        self.ship_combobox.grid(row=0, column=1, padx=5, sticky="ew")

        invest_label = ttk.Label(config_frame, text="Max Investment (aUEC)")
        invest_label.grid(row=1, column=0, padx=5, sticky="w")

        self.invest_entry = ttk.Entry(config_frame, font=custom_font)
        self.invest_entry.insert(0, "25000")
        self.invest_entry.grid(row=1, column=1, padx=5, sticky="ew")

        proft_label = ttk.Label(config_frame, text="Minimum Profit per Unit")
        proft_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.profit_entry = ttk.Entry(config_frame, font=custom_font)
        self.profit_entry.insert(0, "0.05")
        self.profit_entry.grid(row=2, column=1, padx=5, sticky="ew")

        buy_time_label = ttk.Label(config_frame, text="Max Buy Time (Minutes)")
        buy_time_label.grid(row=3, column=0, padx=5, sticky="w")

        self.buy_time_entry = ttk.Entry(config_frame, font=custom_font)
        self.buy_time_entry.insert(0, "10")
        self.buy_time_entry.grid(row=3, column=1, padx=5, sticky="ew")

        sell_time_label = ttk.Label(config_frame,
                                    text="Max Sell Time (Minutes)")
        sell_time_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.sell_time_entry = ttk.Entry(config_frame, font=custom_font)
        self.sell_time_entry.insert(0, "10")
        self.sell_time_entry.grid(row=4, column=1, padx=5, sticky="ew")

        self.refresh_button = ttk.Button(config_frame, text="Refresh",
                                         command=self.refresh_clicked)
        self.refresh_button.grid(row=5, column=0, pady=5)

        self.calculate_button = ttk.Button(config_frame, text="Calculate",
                                           command=self.calculate_clicked,
                                           state="disabled")
        self.calculate_button.grid(row=5, column=1, pady=5)

        self.progress_bar = ttk.Progressbar(config_frame, orient="horizontal",
                                            length=100, mode="determinate")
        self.progress_bar.grid(row=6, column=0, columnspan=2,
                               pady=10, padx=10, sticky="ew")

        # SUMMARY TREEVIEW
        summary_frame = ttk.Frame(self.root, padding="5 5 5 5")
        summary_frame.grid(row=0, column=1, columnspan=10)

        summary_columns = {
            "Commodity":   self.get_padded_size(MaxLength.COMMODITY.value),
            "Max Profit":  self.get_padded_size(MaxLength.PROFIT.value),
            "Investment":  self.get_padded_size(MaxLength.PROFIT.value),
            "ROI":         self.get_padded_size(MaxLength.ROI.value),
            "Routes":      self.get_padded_size(MaxLength.ROUTES.value),
            "Category":    self.get_padded_size(MaxLength.CATEGORY.value)
        }

        self.summary_tree = ttk.Treeview(summary_frame,
                                         columns=list(summary_columns.keys()),
                                         selectmode="browse",
                                         show="headings",
                                         height=10)

        for heading, width in summary_columns.items():
            self.summary_tree.column(heading, width=width, stretch=False)
            self.summary_tree.heading(heading, text=heading)

        for heading, _ in summary_columns.items():
            self.summary_tree.column(heading, stretch=False)
            self.summary_tree.heading(heading, text=heading)

        summary_vsb = ttk.Scrollbar(summary_frame, orient="vertical",
                                    command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=summary_vsb.set,
                                    selectmode="none")

        self.summary_tree.grid(row=0, column=0)
        summary_vsb.grid(row=0, column=1, sticky="ns")

        self.summary_tree.bind("<<TreeviewSelect>>", self.summary_row_clicked)

        # DETAIL TREEVIEW
        detail_frame = ttk.Frame(self.root, padding="5 5 5 5")
        detail_frame.grid(row=1, column=0, columnspan=11)

        detail_columns = {
            "Origin":         self.get_padded_size(MaxLength.PORT.value),
            "Destination":    self.get_padded_size(MaxLength.PORT.value),
            "QT Travel":      self.get_padded_size(MaxLength.TRAVEL.value),
            "Units":          self.get_padded_size(MaxLength.UNITS.value),
            "Bought":         self.get_padded_size(MaxLength.BUY_SELL.value),
            "Sold":           self.get_padded_size(MaxLength.BUY_SELL.value),
            "Profit":         self.get_padded_size(MaxLength.PROFIT.value),
            "Per Hour":       self.get_padded_size(MaxLength.PROFIT.value),
            "Buy Time":       self.get_padded_size(MaxLength.TIME.value),
            "Sell Time":      self.get_padded_size(MaxLength.TIME.value)
        }

        self.detail_tree = ttk.Treeview(detail_frame,
                                        columns=list(detail_columns.keys()),
                                        selectmode="browse",
                                        show="headings",
                                        height=20)

        detail_vsb = ttk.Scrollbar(detail_frame, orient="vertical",
                                   command=self.detail_tree.yview)
        self.detail_tree.configure(yscrollcommand=detail_vsb.set,
                                   selectmode="browse")
        self.detail_tree.grid(row=0, column=0)
        detail_vsb.grid(row=0, column=1, sticky="ns")

        for heading, width in detail_columns.items():
            self.detail_tree.column(heading, width=width, stretch=False)
            self.detail_tree.heading(heading, text=heading)

        for heading, _ in detail_columns.items():
            self.detail_tree.column(heading, stretch=False)
            self.detail_tree.heading(heading, text=heading)

    def run_mainloop(self):
        self.root.mainloop()

    def populate_summary_winodw(self):
        self.commodities_dict = self.build_commodities_dict()

        for row in self.summary_tree.get_children():
            self.summary_tree.delete(row)

        for row in self.detail_tree.get_children():
            self.detail_tree.delete(row)

        for _, commodity in self.commodities_dict.items():
            self.summary_tree.insert("", "end",
                                     value=[commodity.name,
                                            "", "", "", "",
                                            commodity.category],
                                     tags=(commodity.name))

    def calculate_clicked(self):
        units = self.ship_data[self.ship_combobox.get()]["CU"]
        investment = int(float(self.invest_entry.get()) * 100)
        profit_per_unit = int(float(self.profit_entry.get()) * 100)
        buy_time = int(self.buy_time_entry.get())
        sell_time = int(self.sell_time_entry.get())

        commodities_with_good_routes = list()

        for commodity_name, commodity in self.commodities_dict.items():
            commodity.build_routes(investment, units, profit_per_unit,
                                   buy_time, sell_time)
            if len(commodity.routes) < 1:
                continue

            commodities_with_good_routes.append(commodity_name)

        commodities_with_good_routes.sort(
            key=lambda commodity:
            self.commodities_dict[commodity].routes[0].total_profit(),
            reverse=True)

        for row in self.summary_tree.get_children():
            self.summary_tree.delete(row)

        self.summary_tree.configure(selectmode="browse")

        for commodity_name in commodities_with_good_routes:
            category = self.commodities_dict[commodity_name].category

            number_good_routes = \
                len(self.commodities_dict[commodity_name].routes)

            highest_profit = \
                self.commodities_dict[commodity_name].routes[0].total_profit()

            investment = \
                self.commodities_dict[commodity_name].routes[0]\
                .purchase_port.price * \
                self.commodities_dict[commodity_name].routes[0]\
                .units

            investment = int(investment / 100)

            roi = round(float(highest_profit / investment) * 100, 2)

            self.summary_tree.insert("", "end", value=[
                f"{commodity_name}",
                f"{highest_profit:,} aUEC",
                f"{investment:,} aUEC",
                f"{roi}%",
                f"{number_good_routes}",
                f"{category}"],
                tags=(commodity_name))

    def refresh_clicked(self):
        self.summary_tree.configure(selectmode="none")
        self.calculate_button.configure(state="normal")
        self.populate_summary_winodw()

    def summary_row_clicked(self, t_event):
        summary_tree = t_event.widget
        time_ordered_routes = list()

        try:
            row = summary_tree.item(summary_tree.selection()[0])
            commodity = self.commodities_dict[row["values"][0]]
        except IndexError:
            return

        routes = commodity.routes
        qt_speed = self.ship_data[self.ship_combobox.get()]["QT"]

        for row in self.detail_tree.get_children():
            self.detail_tree.delete(row)

        for route in routes:
            travel_time = route.travel_distance / qt_speed
            travel_time = int(travel_time / 60)
            if travel_time < 1:
                travel_time = 1

            if travel_time == 1:
                time_unit_string = "minute"
            else:
                time_unit_string = "minutes"

            total_time = route.worst_case_buy + route.worst_case_sell
            total_time += travel_time
            total_time += 10  # time to fly into port, get to terminal, etc
            per_hour = round(route.total_profit() / (total_time / 60))

            time_route_tuple = (per_hour, travel_time, time_unit_string, route)
            time_ordered_routes.append(time_route_tuple)

        time_ordered_routes.sort(reverse=True, key=lambda route: route[0])

        for (per_hour, travel_time, time_unit_string, route) in time_ordered_routes:
            route_tag = str(routes.index(route))

            self.detail_tree.insert("", "end", value=[
                f"{route.purchase_port.name} "
                f"({route.purchase_port.planetary_body})",
                f"{route.sale_port.name} "
                f"({route.sale_port.planetary_body})",
                f"{travel_time} {time_unit_string}",
                f"{route.units:,}",
                f"{route.buy_price/100:,}",
                f"{route.sell_price/100:,}",
                f"{route.total_profit():,} aUEC",
                f"{per_hour:,} aUEC",
                f"{route.best_case_buy}-{route.worst_case_buy}",
                f"{route.best_case_sell}-{route.worst_case_sell}"],
                tags=(route_tag))

    def get_padded_size(self, t_text):
        string_size = tkfont.Font().measure(t_text)
        return string_size

    def commodity_builder(self, name, type, url, t_list):
        commodity = Commodity(name, type, url)
        t_list.append(commodity)

    def build_commodities_dict(self):
        url = "https://gallog.co/commodities"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        tags = soup.find_all(class_="commodity stat")
        commodities = list()

        threadpool = ThreadPoolExecutor(max_workers=os.cpu_count())
        commodities_list = list()

        #commodities_list.append(Commodity("Agricium", "metal", "https://gallog.co/commodities/metal/agricium"))
        
        for tag in tags:
            name = tag.text.strip();
            url  = f"https://gallog.co{tag['href']}"
            type = tag['href'].split('/')[2];

            threadpool.submit(self.commodity_builder,
                              name,  type, url, commodities_list)
        threadpool.shutdown(wait=False)

        while len(commodities_list) < len(tags):
            progress = (len(commodities_list) / len(tags)) * 100
            self.progress_bar['value'] = progress
            self.root.update_idletasks()
            time.sleep(0.01)

        self.progress_bar['value'] = 100
        self.root.update_idletasks()

        commodities_dict = dict()

        for commodity in commodities_list:
            commodities_dict[commodity.name] = commodity

        return commodities_dict
