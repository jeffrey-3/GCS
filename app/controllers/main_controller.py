class MainController:
    def __init__(self, view, telemetry_model, config_model):
        self.view = view
        self.telemetry_model = telemetry_model
        self.config_model = config_model
        self.view.start_page_view.new_mission_signal.connect(self.next_page)
        self.view.start_page_view.reconnect_signal.connect(self.go_to_reconnect_page)
        self.view.params_page_controller.complete_signal.connect(self.next_page)
        self.view.plan_page_controller.complete_signal.connect(self.next_page)
        self.view.plan_page_controller.center_map_signal.connect(self.center_map)
        self.view.connect_page_controller.complete_signal.connect(self.start)
        self.view.reconnect_page_controller.complete_signal.connect(self.reconnect)
    
    def next_page(self):
        current_index = self.view.stacked_widget.currentIndex()
        self.view.stacked_widget.setCurrentIndex(current_index + 1)
    
    def go_to_reconnect_page(self):
        self.view.stacked_widget.setCurrentIndex(self.view.stacked_widget.count() - 1)

    def reconnect(self):
        self.show_flight_view()

    def start(self):
        self.config_model.save_last_flightplan_params()

        # Send parameters and waypoints to vehicle
        self.telemetry_model.send_params(self.config_model.get_waypoints(), 
                                         self.config_model.params_payload)
        
        self.show_flight_view()
    
    def show_flight_view(self):
        # Hide configuration and show flight display
        self.view.stacked_widget.hide()
        self.view.pfd_view.show()
        self.view.tabs.show()
        self.view.live_alt_view.show()
        self.view.state_view.show()
    
    def center_map(self):
        self.view.map_view.pan_to_home()