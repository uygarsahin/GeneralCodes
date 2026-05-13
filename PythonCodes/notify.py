from notifypy import Notify

notification = Notify()
notification.title = "Test Notification"
notification.message = "Even cooler message."
notification.icon = r"C:\Users\JZWXFG\Documents\alertIcon.png"

notification.send()