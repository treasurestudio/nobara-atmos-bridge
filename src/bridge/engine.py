import subprocess
import os
import signal
import json

class AtmosEngine:
    def __init__(self, config_path="src/bridge/bridge_config.json"):
        # We use absolute paths to prevent "Home Directory" leaks
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_path, "bridge_config.json")
        self.sink_process = None

        self.settings = {
            "sink_name": "Atmos_Bridge_Sink",
            "layout": "[FL,FR,FC,LFE,RL,RR,SL,SR]"
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.settings.update(json.load(f))
            except:
                pass

    def start(self):
        if self.sink_process:
            return "Already running."

        # Create the 7.1 Virtual Sink
        cmd = [
            "pw-loopback",
            "--name", self.settings["sink_name"],
            "--capture-props", (
                f"node.description='Atmos Bridge (7.1)' "
                f"media.class=Audio/Sink "
                f"audio.position={self.settings['layout']}"
            ),
            "--playback-props", "node.passive=true"
        ]

        try:
            self.sink_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
            return "SUCCESS: Atmos Bridge Sink started."
        except Exception as e:
            return f"ERROR: {e}"

    def stop(self):
        if self.sink_process:
            os.kill(self.sink_process.pid, signal.SIGTERM)
            self.sink_process = None
            return "Atmos Bridge stopped."
        return "Not running."

if __name__ == "__main__":
    engine = AtmosEngine()
    print(engine.start())
    input("Press Enter to close bridge...")
    print(engine.stop())
