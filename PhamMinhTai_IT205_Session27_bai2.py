from abc import ABC, abstractmethod


class BaseProduct(ABC):

    warehouse_name = "Amazon Logistics"
    base_storage_fee = 5000


    def __init__(self, product_code, product_name):
        self.__stock_quantity = 0
        self.product_code = product_code
        self.product_name = product_name.strip().upper()


    @property
    def stock_quantity(self):
        return self.__stock_quantity


    def _update_stock(self, amount):
        self.__stock_quantity += amount


    @abstractmethod
    def import_stock(self, quantity):
        pass


    @abstractmethod
    def export_stock(self, quantity):
        pass


    def __add__(self, other):

        if not isinstance(other, BaseProduct):
            return NotImplemented

        return (
            self.stock_quantity
            +
            other.stock_quantity
        )


    def __lt__(self, other):

        if not isinstance(other, BaseProduct):
            return NotImplemented

        return (
            self.stock_quantity
            <
            other.stock_quantity
        )


    @staticmethod
    def validate_product_code(code):

        return (
            code[0].isalpha()
            and len(code) == 10
        )


    @classmethod
    def update_warehouse_name(cls, name):

        cls.warehouse_name = name




class ColdStorageProduct(BaseProduct):


    def __init__(
        self,
        product_code,
        product_name,
        temperature
    ):

        super().__init__(
            product_code,
            product_name
        )

        self.required_temperature = temperature



    def import_stock(self, quantity):

        self._update_stock(quantity)



    def export_stock(self, quantity):

        loss = quantity * 0.05
        total = quantity + loss


        if total <= self.stock_quantity:

            self._update_stock(-total)
            return True

        return False



    def apply_cooling_cost(self):

        return self.stock_quantity * 3000





class HazardousProduct(BaseProduct):


    def __init__(
        self,
        product_code,
        product_name,
        max_safety_limit
    ):

        super().__init__(
            product_code,
            product_name
        )

        self.max_safety_limit = max_safety_limit



    def import_stock(self, quantity):

        if (
            self.stock_quantity + quantity
            >
            self.max_safety_limit
        ):
            raise Exception(
                "Vượt quá giới hạn an toàn"
            )


        self._update_stock(quantity)



    def export_stock(self, quantity):

        if quantity <= self.stock_quantity:

            self._update_stock(-quantity)

            return True

        return False




class HybridPremiumProduct(
    ColdStorageProduct,
    HazardousProduct
):


    def __init__(
        self,
        product_code,
        product_name,
        temperature,
        limit
    ):

        ColdStorageProduct.__init__(
            self,
            product_code,
            product_name,
            temperature
        )

        self.max_safety_limit = limit



    def import_stock(self, quantity):

        if (
            self.stock_quantity + quantity
            >
            self.max_safety_limit
        ):

            raise Exception(
                "Vượt quá giới hạn an toàn"
            )


        self._update_stock(quantity)




class FedExCarrier:


    def ship_package(
        self,
        product,
        quantity
    ):

        product.export_stock(quantity)

        print(
            "FedEx đã nhận hàng"
        )




class DHLCarrier:


    def ship_package(
        self,
        product,
        quantity
    ):

        product.export_stock(quantity)

        print(
            "DHL đã nhận hàng"
        )




def dispatch_to_carrier(
    carrier_agent,
    product,
    quantity
):

    try:

        carrier_agent.ship_package(
            product,
            quantity
        )


    except AttributeError:

        print(
            "Đơn vị vận chuyển không hợp lệ"
        )




products = []


def menu():

    current_product = None


    while True:


        print("""
1. Register Product
2. Show Product MRO
3. Import / Export
4. Storage Cost
5. Compare Stock
6. Shipping
7. Exit
        """)


        choice = input("Choose: ")



        if choice == "1":


            t = input(
                "1 Cold 2 Hazard 3 Hybrid: "
            )


            code = input(
                "Code: "
            )


            if not BaseProduct.validate_product_code(code):

                print(
                    "Mã sản phẩm không hợp lệ"
                )
                continue



            name = input(
                "Name: "
            )


            if t == "1":

                temp = int(
                    input("Temperature: ")
                )


                current_product = ColdStorageProduct(
                    code,
                    name,
                    temp
                )


            elif t == "2":

                current_product = HazardousProduct(
                    code,
                    name,
                    500
                )


            else:

                current_product = HybridPremiumProduct(
                    code,
                    name,
                    -70,
                    200
                )


            products.append(current_product)



        elif choice == "2":

            if current_product:

                print(
                    current_product.__class__.mro()
                )



        elif choice == "3":

            action = input(
                "1 Import 2 Export:"
            )

            amount = int(
                input("Quantity:")
            )


            if action == "1":

                current_product.import_stock(
                    amount
                )

            else:

                current_product.export_stock(
                    amount
                )



        elif choice == "4":

            if hasattr(
                current_product,
                "apply_cooling_cost"
            ):

                print(
                    current_product.apply_cooling_cost()
                )



        elif choice == "5":

            other = products[0]

            print(
                current_product + other
            )

            print(
                current_product < other
            )



        elif choice == "6":

            carrier = FedExCarrier()

            dispatch_to_carrier(
                carrier,
                current_product,
                20
            )



        elif choice == "7":

            break



menu()