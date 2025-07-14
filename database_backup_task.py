from db_utils import get_db_connection
import subprocess
import os
import gradio as gr
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()


def get_all_databases():
    try:
        with get_db_connection("postgres") as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """select datname from pg_database where datistemplate = False"""
                )
                rows = cursor.fetchall()
                if rows:
                    databases = [row[0] for row in rows]
                    if not databases:
                        return []
                    # print(databases)
                    return databases
                else:
                    conn.commit()
                    return cursor.rowcount
    except Exception as e:
        print("error occurred", e)
        return str(e), None


def backup_selected_database(databases):
    for db in databases:
        current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{db}_{current_timestamp}.backup"
        execute_pg_dump(db, filename)
    return "Backup Completed."


def execute_pg_dump(database, filename):
    backup_dir = "backup_files"
    os.makedirs(backup_dir, exist_ok=True)
    filepath = os.path.join(backup_dir, filename)
    pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"
    command = [
        pg_dump_path,
        "-U",
        os.getenv("DB_USER"),
        "-h",
        os.getenv("DB_HOST"),
        "-p",
        os.getenv("DB_PORT"),
        "-F",
        "c",
        "-f",
        filepath,
        database,
    ]

    env = os.environ.copy()
    env["PGPASSWORD"] = os.getenv("DB_PASSWORD")

    try:
        subprocess.run(command, check=True, env=env)
        print(f"Backup Successful: {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Error during pg_dump: {e}")


if __name__ == "__main__":

    # def main_ui():
    with gr.Blocks() as ui:
        gr.Markdown("## PostgreSQL Database Backup Tool")

        db_list = get_all_databases()
        db_selector = gr.CheckboxGroup(
            choices=db_list, label="Select Databases to Backup"
        )

        backup_button = gr.Button("Run Backup")
        output = gr.Textbox(label="Backup Status", lines=10)

        backup_button.click(
            fn=backup_selected_database, inputs=db_selector, outputs=output
        )

    ui.launch()
