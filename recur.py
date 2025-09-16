import os
from notion_client import Client
from datetime import datetime, timedelta, UTC

notion = Client(auth=os.environ["NOTION_TOKEN"])
DATABASE_ID = os.environ["DATABASE_ID"]

def get_recurring_tasks():
    res = notion.databases.query(**{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "Status",
                "select": {
                    "equals": "Recurring"
                }
            }
        })
    return res["results"]

def get_target():
    res = notion.databases.query(**{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "Name",
                "rich_text": {
                    "equals": "$target"
                }
            }
        })
    return res["results"][0]

def change_to_tomorrow(task, target):
    task["properties"]["Status"] = target["properties"]["Status"]
    task["properties"]["Date"] = target["properties"]["Date"]

    tomorrow = datetime.now(UTC).date() + timedelta(days=1)
    task["properties"]["Date"]["date"]["start"] = tomorrow.strftime("%Y-%m-%d")
    return task

def create_task(task):
    notion.pages.create(**task)

def main():
    recurring_tasks = get_recurring_tasks()
    target = get_target()
    for task in recurring_tasks:
        create_task(change_to_tomorrow(task, target))

if __name__ == "__main__":
    main()