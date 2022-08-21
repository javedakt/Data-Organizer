import csv
import sys

# Creating separate classes to assist organizing information from the input files


class Team:
    def __init__(self, team_name, team_id=None):
        self.team_id = team_id
        self.team_name = team_name


class Matched_Team:
    def __init__(self, matched_team_id, matched_id, matched_team_quantity):
        self.matched_team_id = matched_team_id
        self.matched_id = matched_id
        self.matched_team_quantity = matched_team_quantity


class Product:
    def __init__(self, product_name, product_id, product_price=None, product_lot_size=0, quantity_sold=None):
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.product_lot_size = product_lot_size
        self.quantity_sold = quantity_sold


class Matched:
    def __init__(self, matched_id, matched_quantity, matched_discount):
        self.matched_id = matched_id
        self.matched_quantity = matched_quantity
        self.matched_discount = matched_discount


# Making empty lists to store all relevant information

def main():
    team_items = []
    matched_team_items = []
    product_items = []
    matched_items = []

    # Creating the command line arguments

    TeamMap_arg = sys.argv[1]
    ProductMaster_arg = sys.argv[2]
    Sales_arg = sys.argv[3]

    TeamReport_arg = sys.argv[4]
    TeamReportValue = TeamReport_arg.split('=')[1]

    product_argument = sys.argv[5]
    ProductReportValue = product_argument.split('=')[1]

    # Reading and organizing input files into their respective lists

    with open(TeamMap_arg, "r") as TeamMap:
        reader = csv.reader(TeamMap, delimiter=",")
        header = next(reader)
        for row in reader:
            team_id = row[0]
            team_name = row[1]

            team_details = Team(team_id=team_id, team_name=team_name)
            team_items.append(team_details)

    with open(ProductMaster_arg, "r") as ProductMaster:
        reader = csv.reader(ProductMaster, delimiter=",")
        for row in reader:
            product_id = row[0]
            product_name = row[1]
            product_price = row[2]
            product_lot_size = row[3]

            product_details = Product(product_id=product_id, product_name=product_name,
                                      product_price=product_price, product_lot_size=product_lot_size)
            product_items.append(product_details)

    # Creating the report files and adding headers

    product_output = open(ProductReportValue, 'w')
    product_output_header = "Name,GrossRevenue,TotalUnits,DiscountCost\n"
    product_output.write(product_output_header)

    team_output = open(TeamReportValue, 'w')
    team_output_header = "Team,GrossRevenue\n"
    team_output.write(team_output_header)

    with open(Sales_arg, "r") as Salesdoc:
        reader = csv.reader(Salesdoc, delimiter=",")
        for row in reader:
            sale_id = row[0]
            product_id = row[1]
            team_id = row[2]
            quantity_products_sold = row[3]
            sale_discount = row[4]

            for product_details in product_items:
                if product_details.product_id == product_id:
                    match_details = Matched(
                        matched_id=product_id, matched_quantity=quantity_products_sold, matched_discount=sale_discount)
                    matched_items.append(match_details)

            for x in team_items:
                if x.team_id == team_id:
                    team_match = Matched_Team(
                        matched_team_id=team_id, matched_id=product_id, matched_team_quantity=quantity_products_sold)
                    matched_team_items.append(team_match)

    # Calculating information for the "ProductReport" output file

    for x in product_items:

        temp_product_id = x.product_id
        temp_product_lot = x.product_lot_size
        temp_product_price = x.product_price
        temp_product_name = x.product_name
        temp_total_units = 0
        gross_revenue = 0
        temp_sale_discount = 0

        for x in matched_items:
            if temp_product_id == x.matched_id:
                temp_total_units += int(x.matched_quantity) * \
                    int(temp_product_lot)
                gross_revenue = temp_total_units*float(temp_product_price)
                temp_sale_discount = gross_revenue * \
                    (float(x.matched_discount)/100)
        # print(temp_product_name, gross_revenue,
        #       temp_total_units, temp_sale_discount)

        # Formatting and writing the newly calculated information to "ProductReport"

        product_line = "{},{},{},{}\n".format(
            temp_product_name, gross_revenue, temp_total_units, temp_sale_discount)
        product_output.write(product_line)
    product_output.close()

    # Calculating information for the "TeamReport" output file

    for x in team_items:

        temp_team_id = x.team_id
        temp_team_name = x.team_name
        temp_team_units = 0

        for x in matched_team_items:
            temp_product_id = x.matched_id
            temp_product_quantity = x.matched_team_quantity
            if temp_team_id == x.matched_team_id:
                for x in product_items:
                    temp_product_lot = x.product_lot_size
                    temp_product_price = x.product_price
                    if temp_product_id == x.product_id:
                        temp_team_units += int(temp_product_quantity) * \
                            int(temp_product_lot)
                        gross_revenue = temp_team_units * \
                            float(temp_product_price)
        # print(temp_team_name, gross_revenue)

        # Formatting and writing the newly calculated information to "TeamReport"

        team_line = "{},{}\n".format(temp_team_name, gross_revenue)
        team_output.write(team_line)
    team_output.close()

    # Formulas that I used for calculations

    # Product Report:
    # product_name,
    # (quantity_products_sold * product_lot_size) * product_price,
    # (quantity_products_sold * product_lot_size),
    # (gross_revenue * sale_discount)

    # Team Report:
    # team_name,
    # gross_revenue


if __name__ == "__main__":
    main()

# Code by Gugudu Javed Akthar
