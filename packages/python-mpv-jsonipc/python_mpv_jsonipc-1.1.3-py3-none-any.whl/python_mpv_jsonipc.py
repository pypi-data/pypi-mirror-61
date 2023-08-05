import threading
import socket
import json
import os
import time
import subprocess
import random
import traceback
import queue

if os.name == "nt":
    import _winapi
    from multiprocessing.connection import PipeConnection

TIMEOUT = 120

class MPVError(Exception):
    def __init__(self, *args, **kwargs):
        super(MPVError, self).__init__(*args, **kwargs)

class WindowsSocket(threading.Thread):
    def __init__(self, ipc_socket, callback=None):
        ipc_socket = "\\\\.\\pipe\\" + ipc_socket
        self.callback = callback
        
        openmode = _winapi.PIPE_ACCESS_DUPLEX
        access = _winapi.GENERIC_READ | _winapi.GENERIC_WRITE
        limit = 5 # Connection may fail at first. Try 5 times.
        for _ in range(5):
            try:
                pipe_handle = _winapi.CreateFile(
                    ipc_socket, access, 0, _winapi.NULL, _winapi.OPEN_EXISTING,
                    _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL
                    )
                break
            except OSError:
                time.sleep(1)
        else:
            raise MPVError("Cannot connect to pipe.")
        self.socket = PipeConnection(pipe_handle)

        if self.callback is None:
            self.callback = lambda data: None

        threading.Thread.__init__(self)

    def stop(self):
        if self.socket is not None:
            self.socket.close()
        self.join()

    def send(self, data):
        self.socket.send_bytes(json.dumps(data).encode('utf-8') + b'\n')

    def run(self):
        data = b''
        try:
            while True:
                current_data = self.socket.recv_bytes(2048)
                if current_data == b'':
                    break

                data += current_data
                if data[-1] != 10:
                    continue

                data = data.decode('utf-8', 'ignore').encode('utf-8')
                for item in data.split(b'\n'):
                    if item == b'':
                        continue
                    json_data = json.loads(item)
                    self.callback(json_data)
                data = b''
        except EOFError:
            pass

class UnixSocket(threading.Thread):
    def __init__(self, ipc_socket, callback=None):
        self.ipc_socket = ipc_socket
        self.callback = callback
        self.socket = socket.socket(socket.AF_UNIX)
        self.socket.connect(self.ipc_socket)

        if self.callback is None:
            self.callback = lambda data: None

        threading.Thread.__init__(self)

    def stop(self):
        if self.socket is not None:
            self.socket.shutdown(socket.SHUT_WR)
            self.socket.close()
        self.join()

    def send(self, data):
        self.socket.send(json.dumps(data).encode('utf-8') + b'\n')

    def run(self):
        data = b''
        while True:
            current_data = self.socket.recv(1024)
            if current_data == b'':
                break

            data += current_data
            if data[-1] != 10:
                continue

            data = data.decode('utf-8', 'ignore').encode('utf-8')
            for item in data.split(b'\n'):
                if item == b'':
                    continue
                json_data = json.loads(item)
                self.callback(json_data)
            data = b''

class MPVProcess:
    def __init__(self, ipc_socket, mpv_location=None, **kwargs):
        if mpv_location is None:
            if os.name == 'nt':
                mpv_location = "mpv.exe"
            else:
                mpv_location = "mpv"
        
        ipc_socket_name = ipc_socket
        if os.name == 'nt':
            ipc_socket = "\\\\.\\pipe\\" + ipc_socket

        if os.name != 'nt' and os.path.exists(ipc_socket):
            os.remove(ipc_socket)

        self.ipc_socket = ipc_socket
        args = [mpv_location]
        self._set_default(kwargs, "idle", True)
        self._set_default(kwargs, "input_ipc_server", ipc_socket_name)
        self._set_default(kwargs, "input_terminal", False)
        self._set_default(kwargs, "terminal", False)
        args.extend("--{0}={1}".format(v[0].replace("_", "-"), self._mpv_fmt(v[1]))
                    for v in kwargs.items())
        self.process = subprocess.Popen(args)
        time.sleep(1)
        for _ in range(20):
            time.sleep(0.1)
            self.process.poll()
            if os.path.exists(ipc_socket) or self.process.returncode is not None:
                break
        
        if not os.path.exists(ipc_socket) or self.process.returncode is not None:
            print("dead", os.path.exists(ipc_socket), self.process.returncode)
            raise MPVError("MPV not started.")

    def _set_default(self, prop_dict, key, value):
        if key not in prop_dict:
            prop_dict[key] = value

    def _mpv_fmt(self, data):
        if data == True:
            return "yes"
        elif data == False:
            return "no"
        else:
            return data

    def stop(self):
        self.process.terminate()
        if os.name != 'nt' and os.path.exists(self.ipc_socket):
            os.remove(self.ipc_socket)

class MPVInter:
    def __init__(self, ipc_socket, callback=None):
        Socket = UnixSocket
        if os.name == 'nt':
            Socket = WindowsSocket

        self.callback = callback
        if self.callback is None:
            self.callback = lambda event, data: None
        
        self.socket = Socket(ipc_socket, self.event_callback)
        self.socket.start()
        self.command_id = 1
        self.rid_lock = threading.Lock()
        self.socket_lock = threading.Lock()
        self.cid_result = {}
        self.cid_wait = {}
    
    def stop(self):
        self.socket.stop()

    def event_callback(self, data):
        if "request_id" in data:
            self.cid_result[data["request_id"]] = data
            self.cid_wait[data["request_id"]].set()
        elif "event" in data:
            self.callback(data["event"], data)
    
    def command(self, command, *args):
        self.rid_lock.acquire()
        command_id = self.command_id
        self.command_id += 1
        self.rid_lock.release()

        event = threading.Event()
        self.cid_wait[command_id] = event

        command_list = [command]
        command_list.extend(args)
        try:
            self.socket_lock.acquire()
            self.socket.send({"command":command_list, "request_id": command_id})
        finally:
            self.socket_lock.release()

        has_event = event.wait(timeout=TIMEOUT)
        if has_event:
            data = self.cid_result[command_id]
            del self.cid_result[command_id]
            del self.cid_wait[command_id]
            if data["error"] != "success":
                if data["error"] == "property unavailable":
                    return None
                raise MPVError(data["error"])
            else:
                return data.get("data")
        else:
            raise TimeoutError("No response from MPV.")

class EventHandler(threading.Thread):
    def __init__(self):
        self.queue = queue.Queue()
        threading.Thread.__init__(self)
    
    def put_task(self, func, *args):
        self.queue.put((func, args))

    def stop(self):
        self.queue.put("quit")
        self.join()

    def run(self):
        while True:
            event = self.queue.get()
            if event == "quit":
                break
            try:
                event[0](*event[1])
            except:
                traceback.print_exc()

class MPV:
    def __init__(self, start_mpv=True, ipc_socket=None, mpv_location=None, **kwargs):
        self.properties = {}
        self.event_bindings = {}
        self.key_bindings = {}
        self.property_bindings = {}
        self.mpv_process = None
        self.event_handler = EventHandler()
        self.event_handler.start()
        if ipc_socket is None:
            rand_file = "mpv{0}".format(random.randint(0, 2**48))
            if os.name == "nt":
                ipc_socket = rand_file
            else:
                ipc_socket = "/tmp/{0}".format(rand_file)

        if start_mpv:
            self.mpv_process = MPVProcess(ipc_socket, mpv_location, **kwargs)

        self.mpv_inter = MPVInter(ipc_socket, self._callback)
        self.properties = set(x.replace("-", "_") for x in self.command("get_property", "property-list"))
        for command in self.command("get_property", "command-list"):
            object.__setattr__(self, command["name"].replace("-", "_"), self._get_wrapper(command["name"]))

        self._dir = list(self.properties)
        self._dir.extend(object.__dir__(self))

        self.observer_id = 1
        self.observer_lock = threading.Lock()
        self.keybind_id = 1
        self.keybind_lock = threading.Lock()
        
        @self.on_event("property-change")
        def event_handler(data):
            if data.get("id") in self.property_bindings:
                self.event_handler.put_task(self.property_bindings[data["id"]], data["name"], data["data"])

        @self.on_event("client-message")
        def client_message_handler(data):
            args = data["args"]
            if len(args) == 2 and args[0] == "custom-bind":
                self.event_handler.put_task(self.key_bindings[args[1]])

    def bind_event(self, name, callback):
        if name not in self.event_bindings:
            self.event_bindings[name] = set()
        self.event_bindings[name].add(callback)

    def on_event(self, name):
        def wrapper(func):
            self.bind_event(name, func)
            return func
        return wrapper

    # Added for compatibility.
    def event_callback(self, name):
        return self.on_event(name)

    def on_key_press(self, name):
        def wrapper(func):
            self.bind_key_press(name, func)
            return func
        return wrapper

    def bind_key_press(self, name, callback):
        self.keybind_lock.acquire()
        keybind_id = self.keybind_id
        self.keybind_id += 1
        self.keybind_lock.release()

        self.key_bindings["bind{0}".format(keybind_id)] = callback
        self.keybind(name, "script-message custom-bind bind{0}".format(keybind_id))

    def bind_property_observer(self, name, callback):
        self.observer_lock.acquire()
        observer_id = self.observer_id
        self.observer_id += 1
        self.observer_lock.release()

        self.property_bindings[observer_id] = callback
        self.command("observe_property", observer_id, name)
        return observer_id

    def unbind_property_observer(self, observer_id):
        self.command("unobserve_property", observer_id)
        del self.property_bindings[observer_id]

    def property_observer(self, name):
        def wrapper(func):
            self.bind_property_observer(name, func)
            return func
        return wrapper
    
    def wait_for_property(self, name):
        event = threading.Event()
        def handler(*_):
            event.set()
        observer_id = self.bind_property_observer(name, handler)
        event.wait()
        self.unbind_property_observer(observer_id)

    def _get_wrapper(self, name):
        def wrapper(*args):
            return self.command(name, *args)
        return wrapper

    def _callback(self, event, data):
        if event in self.event_bindings:
            for callback in self.event_bindings[event]:
                self.event_handler.put_task(callback, data)

    def play(self, url):
        self.loadfile(url)

    def __del__(self):
        self.terminate()

    def terminate(self):
        if self.mpv_process:
            self.mpv_process.stop()
        self.mpv_inter.stop()
        self.event_handler.stop()

    def command(self, command, *args):
        return self.mpv_inter.command(command, *args)

    def __getattr__(self, name):
        if name in self.properties:
            return self.command("get_property", name.replace("_", "-"))
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name not in {"properties", "command"} and name in self.properties:
            return self.command("set_property", name.replace("_", "-"), value)
        return object.__setattr__(self, name, value)

    def __hasattr__(self, name):
        if object.__hasattr__(self, name):
            return True
        else:
            try:
                getattr(self, name)
                return True
            except MPVError:
                return False

    def __dir__(self):
        return self._dir
