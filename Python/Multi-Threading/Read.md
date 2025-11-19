🧠 What is the Global Interpreter Lock (GIL)?
🔹 Definition:

The GIL (Global Interpreter Lock) is a mutex (mutual exclusion lock) used by the CPython interpreter to ensure that only one thread executes Python bytecode at a time, even if your system has multiple CPU cores.

That means:
👉 In CPython, threads do not truly run in parallel for CPU-bound tasks.
👉 But for I/O-bound tasks (like network requests or file reading), threads can still be useful.

⚙️ Why GIL Exists

Python uses reference counting for memory management — every object keeps track of how many references point to it.
To avoid race conditions when multiple threads modify reference counts simultaneously, the GIL ensures only one thread executes Python code at a time.