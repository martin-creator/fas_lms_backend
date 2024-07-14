class ControllerManager:
    def __init__(self):
        self.controllers = {}

    def register_controller(self, controller_name, controller_instance):
        self.controllers[controller_name] = controller_instance

    def get_controller(self, controller_name):
        return self.controllers.get(controller_name)

    def health_check(self):
        health_status = {}
        for name, controller in self.controllers.items():
            health_status[name] = controller.check_health()
        return health_status