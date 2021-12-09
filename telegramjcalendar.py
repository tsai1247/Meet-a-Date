from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from convert_numbers import english_to_hindi

import jdatetime as datetime
import utils
import messages


days = [
    'شنبه', 'یک‌‌شنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'
]

def create_calendar(year=None, month=None):
    now = datetime.datetime.now()
    if not year: year = now.year
    if not month: month = now.month

    keyboard = []

    #First row - Month and Year
    row=[]
    datetime.set_locale('fa_IR')
    row.append(
        InlineKeyboardButton(
            datetime.date(year, month, 1).strftime("%B") + " " + str(year),
            callback_data=create_callback_data("IGNORE")
        )
    )
    keyboard.append(row)

    #Second row - Week Days
    row=[]
    for day in days:
        row.append(InlineKeyboardButton(day,callback_data=create_callback_data("IGNORE")))
    keyboard.append(row)

    month_weeks = monthcalendar(year, month)
    for week in month_weeks:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=create_callback_data("IGNORE")))
            else:
                row.append(
                    InlineKeyboardButton(
                        str(day),
                        callback_data=create_callback_data("DAY", year, month, day)
                    )
                )
        keyboard.append(row)

    #Last row - Buttons
    row = []
    if month != now.month:
        row.append(
            InlineKeyboardButton(
                "<",
                callback_data=create_callback_data("PREV-MONTH", year, month, day)
            )
        )
    else:
        row.append(InlineKeyboardButton(" ", callback_data=create_callback_data("IGNORE")))
    row.append(
        InlineKeyboardButton(
            ">",
            callback_data=create_callback_data("NEXT-MONTH", year, month, day)
        )
    )
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def monthcalendar(year=datetime.datetime.today().year, month=datetime.datetime.today().month):
    start_day_week_day = datetime.date(year, month, 1).weekday()
    weeks = []
    weeks.append([0] * start_day_week_day + list(range(1, 8 - start_day_week_day)))
    days_left = (
        datetime.date(year, month, 1) - datetime.timedelta(days=1)
        ).day - weeks[0][-1]
    for i in range(days_left // 7):
        weeks.append(list(range(weeks[i][-1] + 1, weeks[i][-1] + 8)))
    if days_left % 7:
        weeks.append(list(range(weeks[-1][-1] + 1, weeks[-1][-1] + 1 + (days_left % 7))) + [0] * (7 - days_left % 7))
    
    # remove days before today
    if datetime.date.today().month == month and \
        datetime.date.today().year == year:     
        today = datetime.date.today().day   
        for week in weeks:
            for i in range(7):
                if week[i] <= today: week[i] = 0
                else: break
            else: continue
            break
    
    return weeks


def create_callback_data(action, year=0, month=0, day=0):
    return messages.JCALENDAR_CALLBACK + ";" + ";".join([action, str(year), str(month), str(day)])