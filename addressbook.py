from collections import UserDict
from datetime import datetime, timedelta

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found")
        
    def get_upcoming_birthdays(self, shift_weekend_birthday_to_monday=True):
        today = datetime.now().date()
        one_week_forward = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.date
                birthday_this_year = birthday.replace(year=today.year)

                if today <= birthday_this_year <= one_week_forward:
                    congratulation_date = birthday_this_year

                    if shift_weekend_birthday_to_monday:
                        if congratulation_date.weekday() == 5:
                            congratulation_date += timedelta(days=2)
                        elif congratulation_date.weekday() == 6:
                            congratulation_date += timedelta(days=1)
                    else:
                        if congratulation_date.weekday() == 5:
                            congratulation_date -= timedelta(days=1)
                        elif congratulation_date.weekday() == 6:
                            congratulation_date -= timedelta(days=2)

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%d.%m.%Y"),
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays