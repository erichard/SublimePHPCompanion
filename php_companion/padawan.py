import sublime
from os import path
import urllib
import json
import subprocess
import re
from .settings import get_setting


server_addr = "http://127.0.0.1:15155"
cli = 'padawan'
server_command = 'padawan-server'


class Server:

    def start(self):
        subprocess.Popen(
            server_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

    def stop(self):
        try:
            self.sendRequest('kill', {})
            return True
        except Exception:
            return False

    def restart(self):
        if self.stop():
            self.start()

    def sendRequest(self, command, params, data=''):
        timeout = get_setting("padawan_timeout", 0.5)
        addr = server_addr + "/"+command+"?" + urllib.parse.urlencode(params)
        response = urllib.request.urlopen(
            addr,
            data.encode("utf8"),
            timeout
        )
        result = json.loads(response.read().decode("utf8"))
        if "error" in result:
            raise ValueError(result["error"])
        return result


class Editor:

    def getView(self):
        return sublime.active_window().active_view()

    def log(self, message):
        print(message)

    def notify(self, message):
        self.getView().set_status("PadawanStatus", message)

    def progress(self, progress):
        bars = int(progress / 5)
        bars_str = ''
        for i in range(20):
            if i < bars:
                bars_str += '='
            else:
                bars_str += ' '
        bars_str = '[' + bars_str + ']'
        message = "Progress {0} {1}%".format(bars_str, str(progress))

        self.getView().set_status("PadawanProgress", message)
        return

    def error(self, error):
        self.notify(error)

    def callAfter(self, timeout, callback):
        def Notifier():
            if callback():
                sublime.set_timeout(Notifier, timeout)
        sublime.set_timeout(Notifier, timeout)

server = Server()
editor = Editor()
pathError = '''padawan command is not found in your $PATH. Please\
 make sure you installed padawan.php package and\
 configured your $PATH'''


class PadawanClient:

    def GetCompletion(self, filepath, line_num, column_num, contents):
        curPath = self.GetProjectRoot(filepath)

        params = {
                'filepath': filepath.replace(curPath, ""),
                'line': line_num,
                'column': column_num,
                'path': curPath
                }
        result = self.DoRequest('complete', params, contents)

        if not result:
            return {"completion": []}

        return result

    def SaveIndex(self, filepath):
        return self.DoRequest('save', {'filepath': filepath})

    def DoRequest(self, command, params={}, data=''):
        try:
            return server.sendRequest(command, params, data)
        except urllib.request.URLError:
            editor.error("Padawan.php is not running")
        except Exception as e:
            editor.error("Error occured {0}".format(e))

        return False

    def AddPlugin(self, plugin):
        composer = get_setting("padawan_composer", "composer")
        composerCommand = composer + ' global require '

        command = '{0} {2} && {1} plugin add {2}'.format(
                composerCommand,
                cli,
                plugin
                )

        stream = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
                )

        def OnAdd(retcode):
            if not retcode:
                server.restart()
                editor.notify("Plugin installed")
            else:
                if retcode == 127:
                    editor.error(pathError)
                editor.error("Plugin installation failed")

        def LogAdding():
            retcode = stream.poll()
            if retcode is not None:
                return OnAdd(retcode)

            line = stream.stdout.readline().decode("ascii")
            editor.log(line)
            return True
        editor.callAfter(1e-4, LogAdding)

    def RemovePlugin(self, plugin):
        composer = get_setting("padawan_composer", "composer")
        composerCommand = composer + ' global remove'

        command = '{0} {1}'.format(
                composerCommand,
                plugin
                )

        stream = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
                )

        def onRemoved():
            subprocess.Popen(
                    '{0}'.format(
                        cli + ' plugin remove ' + plugin
                        ),
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                    ).wait()
            self.RestartServer()
            return editor.notify("Plugin removed")

        def LogRemoving():
            retcode = stream.poll()
            if retcode is not None:
                return onRemoved()

            line = stream.stdout.readline().decode("ascii")
            editor.log(line)
            return True

        editor.callAfter(1e-4, LogRemoving)

    def GetInstalledPlugins(self):
        return self.DoRequest("plugins")["plugins"]

    def Generate(self, filepath):
        curPath = self.GetProjectRoot(filepath)
        stream = subprocess.Popen(
                'cd ' + curPath + ' && ' + cli + ' generate',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
                )

        def onGenerationEnd(retcode):
            if retcode > 0:
                if retcode == 127:
                    editor.error(pathError)
                else:
                    editor.error("Error occured, code: {0}".format(
                        str(retcode)
                        ))
                return
            server.restart()
            editor.progress(100)
            editor.notify("Index generated")

        def ProcessGenerationPoll():
            retcode = stream.poll()
            if retcode is not None:
                return onGenerationEnd(retcode)
            line = stream.stdout.readline().decode("utf8")
            errorMatch = re.search('Error: (.*)', line)
            if errorMatch is not None:
                retcode = 1
                editor.error("{0}".format(
                    errorMatch.group(1).replace("'", "''")
                    ))
                return
            match = re.search('Progress: ([0-9]+)', line)
            if match is None:
                return True
            progress = int(match.group(1))
            editor.progress(progress)
            return True

        editor.callAfter(1e-4, ProcessGenerationPoll)

    def StartServer(self):
        server.start()

    def StopServer(self):
        server.stop()

    def RestartServer(self):
        server.restart()

    def GetProjectRoot(self, filepath):
        curPath = path.dirname(filepath)
        while curPath != '/' and not path.exists(
                path.join(curPath, 'composer.json')
                ):
            curPath = path.dirname(curPath)

        if curPath == '/':
            curPath = path.dirname(filepath)

        return curPath

client = PadawanClient()
