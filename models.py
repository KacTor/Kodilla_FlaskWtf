import json


class ClimbingRoutes:
    def __init__(self):
        try:
            with open("climbingroutes.json", "r", encoding='UTF8') as f:
                self.routes = json.load(f)
        except FileNotFoundError:
            self.routes = []

    def all(self):
        return self.routes

    def get(self, id):
        route = [route for route in self.all() if route['id'] == id]
        if route:
            return route[0]
        return []

    def add(self, data):
        self.routes.append(data)
        self.save_all()

    def save_all(self):
        with open("climbingroutes.json", "w", encoding='UTF8') as f:
            json.dump(self.routes, f)

    def delete(self, id):
        route = self.get(id)
        if route:
            self.routes.remove(route)
            self.save_all()
            return True
        return False

    def update(self, id, data):
        route = self.get(id)
        if route:
            index = self.routes.index(route)
            self.routes[index] = data
            self.save_all()
            return True
        return False


routes = ClimbingRoutes()
