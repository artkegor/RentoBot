from datetime import datetime, timedelta
from io import BytesIO
from openpyxl import Workbook


async def generate_statistics_excel(user_service, listing_service, log_service) -> BytesIO:
    """Generate Excel file with statistics for last 12 months."""

    users = await user_service.get_registration_statistics_by_month()
    listings = await listing_service.get_listing_statistics_by_month()
    logs = await log_service.get_action_statistics_by_month()

    wb = Workbook()
    ws = wb.active
    ws.title = "Statistics"

    # Header
    ws.append([
        "Месяц",
        "Пользователи",
        "Создано объявлений",
        "Завершено объявлений",
        "Поиски",
        "Контакты"
    ])

    for i in range(12):
        ws.append([
            users[i]["month"],
            users[i]["count"],
            listings[i]["created"],
            listings[i]["finished"],
            logs[i]["search"],
            logs[i]["contact"],
        ])

    file = BytesIO()
    wb.save(file)
    file.seek(0)

    return file