"""
Provides an abstraction for shared-memory access for the replay jobs.

The goal of this implementation is to avoid using the python library module
shared_memory, due to an existing bug: https://bugs.python.org/issue40882

The implementation of the SharedMemory is basically stripped version of of the
implementation in shared_memory.py of the standard Python library, but stripped
of the Win32 support and without the use of the resource manager (what causes
the issue mentioned above).

Copyright 2024, dSPACE Mechatronic Control Technology (Shanghai) Co., Ltd.
All rights reserved.
"""
import mmap
import os
import _posixshmem


class SharedMemory:
    """Creates a new shared memory block or attaches to an existing
    shared memory block.

    Every shared memory block is assigned a unique name.  This enables
    one process to create a shared memory block with a particular name
    so that a different process can attach to that same shared memory
    block using that same name.

    As a resource for sharing data across processes, shared memory blocks
    may outlive the original process that created them.  When one process
    no longer needs access to a shared memory block that might still be
    needed by other processes, the close() method should be called.
    When a shared memory block is no longer needed by any process, the
    unlink() method should be called to ensure proper cleanup."""

    # Defaults; enables close() and unlink() to run without errors.
    _name = None
    _fd = -1
    _mmap = None
    _buf = None
    _flags = os.O_RDWR

    def __init__(self, name, create=False, size=0):
        if not size >= 0:
            raise ValueError("'size' must be a positive integer")
        if create:
            self._flags = os.O_CREAT | os.O_EXCL | os.O_RDWR
            if size == 0:
                raise ValueError(
                    "'size' must be a positive number different from zero"
                )

        # POSIX Shared Memory
        self._fd = _posixshmem.shm_open(
            "/" + name,
            self._flags,
            mode=0o600,
        )
        try:
            if create:
                os.ftruncate(self._fd, size)
            stats = os.fstat(self._fd)
            size = stats.st_size
            self._mmap = mmap.mmap(self._fd, size)
        except OSError:
            self.unlink()
            raise

        self._name = name
        self._size = size
        self._buf = memoryview(self._mmap)

    def __del__(self):
        try:
            self.close()
        except OSError:
            pass

    @property
    def buf(self):
        "A memoryview of contents of the shared memory block."
        return self._buf

    @property
    def name(self):
        "Unique name that identifies the shared memory block."
        return self._name

    @property
    def size(self):
        "Size in bytes."
        return self._size

    def close(self):
        """Closes access to the shared memory from this instance but does
        not destroy the shared memory block."""
        if self._buf is not None:
            self._buf.release()
            self._buf = None
        if self._mmap is not None:
            self._mmap.close()
            self._mmap = None
        if self._fd >= 0:
            os.close(self._fd)
            self._fd = -1

    def unlink(self):
        """Requests that the underlying shared memory block be destroyed.

        In order to ensure proper cleanup of resources, unlink should be
        called once (and only once) across all processes which have access
        to the shared memory block."""
        if self._name:
            _posixshmem.shm_unlink(self._name)


class ReplayJobSharedMemory:
    MAGIC_WORD = b'DSCDRP'
    VERSION = 1
    SHMEM_SIZE = len(MAGIC_WORD) + 1 + 1

    def __init__(self, job_name, create=False):
        self._create = create
        self._shmem = None
        self._start_offset = len(self.MAGIC_WORD) + 1

        self._shmem = SharedMemory(
            name=f'replayjob_{job_name}',
            create=create,
            size=self.SHMEM_SIZE,
        )

        if create:
            self._shmem.buf[:len(self.MAGIC_WORD)] = self.MAGIC_WORD
            self._shmem.buf[len(self.MAGIC_WORD)] = self.VERSION
            self.start = 0
        else:
            if self._shmem.buf[:len(self.MAGIC_WORD)] != self.MAGIC_WORD:
                raise ValueError('Invalid shared memory!')
            if self._shmem.buf[len(self.MAGIC_WORD)] != self.VERSION:
                raise ValueError('Incompatible shared memory versions!')

    @property
    def start(self):
        return self._shmem.buf[self._start_offset]

    @start.setter
    def start(self, val):
        self._shmem.buf[self._start_offset] = val

    def __del__(self):
        self.destroy()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.destroy()

    def destroy(self):
        if self._shmem is not None:
            self._shmem.close()
            if self._create:
                self._shmem.unlink()
            self._shmem = None
