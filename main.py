from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import Screen
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.picker import MDTimePicker
from kivy.clock import Clock
import plyer
import schedule


# from kivymd.color_definitions import colors


class MainScreen(Screen):

    subhan_Allah_count = NumericProperty()
    subhan_Allah_count_text = StringProperty(str(subhan_Allah_count))
    alhamdulillah_count = NumericProperty()
    alhamdulillah_count_text = StringProperty(str(alhamdulillah_count))
    allahu_akbar_count = NumericProperty()
    allahu_akbar_count_text = StringProperty(str(alhamdulillah_count))

    def subhan_Allah_counting(self):  # keeps track of the number of dhikr
        self.subhan_Allah_count += 1
        self.subhan_Allah_count_text = str(self.subhan_Allah_count)
        print(self.subhan_Allah_count)

        if self.subhan_Allah_count == 3:
            # plyer.vibrator.pattern(pattern=(0, 1), repeat=-1) # controls the vibration of the device
            print("vibrating")

    def alhamdulillah_counting(self):
        self.alhamdulillah_count += 1
        self.alhamdulillah_count_text = str(self.alhamdulillah_count)
        print(self.alhamdulillah_count)

        if self.alhamdulillah_count == 3:
            # plyer.vibrator.pattern(pattern=(0, 1), repeat=-1)
            print("vibrating")

    def allahu_akbar_counting(self):
        self.allahu_akbar_count += 1
        self.allahu_akbar_count_text = str(self.allahu_akbar_count)
        print(self.allahu_akbar_count)

        if self.allahu_akbar_count == 3:
            # plyer.vibrator.pattern(pattern=(0, 1), repeat=-1)
            print("vibrating")


class LanguageScreen(Screen):
    def on_touch_move(self, touch):
        pass


class NotificationScreen(Screen):
    pass


class ThemeScreen(Screen):
    pass


class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


GUI = "main.kv"


class MainApp(MDApp):
    hour = NumericProperty()
    minute = NumericProperty()

    fullTime_text = StringProperty(str(hour))

    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"

        return Builder.load_file(GUI)

    def change_screen(self, screen_name, screen_direction):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = screen_name
        screen_manager.transition.direction = screen_direction
        # print(screen_name)

    def return_empty(self):
        print(self.theme_cls.primary_color) # place holder test

    def on_tab_switch(self):
        pass

    def dark_theme(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "200"

    def light_theme(self):
        self.theme_cls.theme_style = "Light"

    def show_timePicker(self):
        picker = MDTimePicker()
        picker.bind(time=self.got_time)  # anytime the time changes, got_time is called
        picker.open()

    def got_time(self, picker_widget, time):
        # checks if it is am or pm and adds a 0 accordingly
        # runs show_notification function if it is the time set by the user
        self.hour = time.hour
        self.minute = time.minute
        self.fullTime_text = str(time)

        if self.hour >= 10 and self.minute >= 10:
            schedule.every().day.at(f'{int(self.hour)}:{int(self.minute)}').do(self.show_notification)
        elif self.hour < 10 and self.minute < 10:
            schedule.every().day.at(str(0) + str(self.hour) + ":" + str(0) + str(self.minute)).do(
                self.show_notification)
        Clock.schedule_interval(lambda dt: schedule.run_pending(), 1)

        print(f'{int(self.hour)}:{int(self.minute)}')
        print(self.fullTime_text)

    def show_notification(self):
        plyer.notification.notify(title="Dhikr Reminder", message="Don't forget to perform "
                                                                  "your dhikr today",
                                  app_name="My Dhikr", timeout=10, ticker="dhikr time",
                                  toast=False)


if __name__ == "__main__":
    MainApp().run()
