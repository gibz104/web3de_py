import platform
import subprocess


class Ganache:
    def __init__(self):
        self.system = platform.system()
        self.release = platform.release()
        self.processes = []

        if not self.check_ganache():
            if self.check_npm():
                self.install_ganache('npm')
                print('LOG: Installed Ganache using npm.')
            elif self.check_yarn():
                self.install_ganache('yarn')
                print('LOG: Installed Ganache using Yarn.')
            else:
                raise Exception('Please install NPM or Yarn package manager.')

    def check_ganache(self):
        check = subprocess.run("ganache-cli --version", shell=True, capture_output=True, text=True)
        if check.returncode == 0:
            return True
        else:
            return False

    def check_nodejs(self):
        check = subprocess.run("node -v", shell=True, capture_output=True, text=True)
        if check.returncode == 0:
            return True
        else:
            return False

    def check_npm(self):
        check = subprocess.run("npm -v", shell=True, capture_output=True, text=True)
        if check.returncode == 0:
            return True
        else:
            return False

    def check_yarn(self):
        check = subprocess.run("yarn --version", shell=True, capture_output=True, text=True)
        if check.returncode == 0:
            return True
        else:
            return False

    def install_ganache(self, pm: str):
        result = None
        if pm == 'npm':
            result = subprocess.run('npm install -g ganache-cli', shell=True, capture_output=True, text=True)
        elif pm == 'yarn':
            result = subprocess.run('yarn global add ganache-cli', shell=True, capture_output=True, text=True)

        if result.returncode != 0 or result is None:
            raise Exception('Cannot install Ganache-CLI.')

    def fork_mainnet(self):
        result = subprocess.run('ganache-cli --fork http://localhost:8545 --port 8555', shell=True, text=True)
        self.processes.append(result)

    def kill_latest_process(self):
        p = self.processes[-1]
        p.terminate()
        p.wait()

    def kill_all_process(self):
        for p in self.processes:
            p.terminate()
            p.wait()
