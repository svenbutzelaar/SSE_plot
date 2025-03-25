import signal
import subprocess
import os
from dotenv import load_dotenv
import time

class EnergiBridgeManager:
    def __init__(self):
        load_dotenv()
        self.energibridge_path = os.getenv("ENERGIBRIDGE_PATH")
        self.driver_path = os.getenv("DRIVER_PATH")
        self.service_name = os.getenv("SERVICE_NAME")
        self.csv_output_dir = os.getenv("CSV_OUTPUT_DIR_PATH")
        self.process = None

    def run_admin_command(self, command):
        full_command = f'powershell -Command "Start-Process cmd -ArgumentList \'/c {command}\' -Verb RunAs"'
        subprocess.run(full_command, shell=True)


    def service_exists(self):
        try:
            result = subprocess.run(f'sc query {self.service_name}', shell=True, capture_output=True, text=True)
            # FAILED 1060 = Service not Found
            return "FAILED 1060" not in result.stdout
        except Exception as e:
            print(f"Error: {e}")
            return False


    def delete_service(self):
        if self.service_exists():
            print(f"Service '{self.service_name}' will be deleted now...")
            self.run_admin_command(f'sc delete {self.service_name}')


    def setup_service(self):
        self.delete_service()

        print(f"Creating Service '{self.service_name}'...")
        self.run_admin_command(f'sc create {self.service_name} type=kernel binPath=\"{self.driver_path}\"')

        print(f"Starting Service '{self.service_name}'...")
        self.run_admin_command(f'sc start {self.service_name}')


    def start(self, output_file_name, timeout_in_seconds=9999):
        print("Starting EnergiBridge...")

        command = [
            self.energibridge_path,
            "-o", os.path.join(self.csv_output_dir, output_file_name),
            "--summary", "timeout", str(timeout_in_seconds)
        ]

        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        # Waiting for EnergiBridge to start
        time.sleep(1)



    def stop(self, print_output=False):
        if not self.process:
            print("No running EnergiBridge process found.")
            return

        print(f"Stopping EnergiBridge...")

        try:
            self.process.send_signal(signal.CTRL_BREAK_EVENT)
            time.sleep(2)
        except Exception as e:
            print(f"Error sending CTRL_C_EVENT: {e}")

        if print_output:
            stdout, stderr = self.process.communicate()
            if stdout:
                print(f"Last line of output: {stdout}")

            if stderr:
                print(f"Error output: {stderr}")

        # check if process is still running
        if self.process.poll() is None:
            print("Process still running, forcing termination...")
            subprocess.run(f"taskkill /F /T /PID {self.process.pid}", shell=True)


if __name__ == "__main__":
    manager = EnergiBridgeManager()
    manager.setup_service()
    manager.start("test1.csv")
    time.sleep(5)
    manager.stop()