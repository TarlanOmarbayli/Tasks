import abc

class Pizza(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_price(self):
        pass

    @abc.abstractmethod
    def get_status(self):
        pass


class Pepperoni(Pizza):
    def __init__(self):
        self.__pizza_price=3.0

    def get_price(self):
        return self.__pizza_price

    def get_status(self):
        return "Pepperoni"


class Barbeque(Pizza):
    def __init__(self):
        self.__pizza_price=5.0

    def get_price(self):
        return self.__pizza_price

    def get_status(self):
        return "Barbeque"


class PizzaDecorator(Pizza):
    def __init__(self,pizza):
        self.pizza=pizza

    def get_price(self):
        return self.pizza.get_price()

    def get_status(self):
        return self.pizza.get_status()


class Tomato(PizzaDecorator):
    def __init__(self,pizza):
        super().__init__(pizza)
        self.__tomato_price=1.0

    @property
    def price(self):
        return self.__tomato_price

    def get_price(self):
        return super().get_price()+self.price

    def get_status(self):
        return super().get_status()+" Tomato"

class Cheese(PizzaDecorator):
    def __init__(self,pizza):
        super().__init__(pizza)
        self.__cheese_price=2.0

    @property
    def price(self):
        return self.__cheese_price

    def get_price(self):
        return super().get_price()+self.price

    def get_status(self):
        return super().get_status()+" Cheese"

class Mushroom(PizzaDecorator):
    def __init__(self,pizza):
        super().__init__(pizza)
        self.__mushroom_price=3.0

    @property
    def price(self):
        return self.__mushroom_price

    def get_price(self):
        return super().get_price()+self.price

    def get_status(self):
        return super().get_status()+" Mushroom"


class PizzaBuilder():
    def __init__(self,pizza_type):
        self.pizza_type=pizza_type
        self.pizza=eval(pizza_type)()
        self.extentions_list=[]

    def add_extention(self,extention):
        if extention=="Tomato":
            self.pizza=Tomato(self.pizza)
        elif extention=="Cheese":
            self.pizza=Cheese(self.pizza)

        elif extention=="Mushroom":
            self.pizza=Mushroom(self.pizza)

        self.extentions_list.append(extention)

    def remove_extention(self,extention):
        if extention in self.extentions_list:
            self.extentions_list.remove(extention)

        temp_pizza=eval(self.pizza_type)()
        for i in self.extentions_list:
            temp_pizza=eval(i)(temp_pizza)

        self.pizza=temp_pizza

    def get_status(self):
        return self.pizza.get_status()

    def get_price(self):
        return self.pizza.get_price()
