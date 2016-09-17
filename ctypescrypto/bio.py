"""
Interface to OpenSSL BIO library
"""
from . import ffi, backend
from . import libcrypto


class Membio(object):
    """
    Provides interface to OpenSSL memory bios
    use str() or unicode() to get contents of writable bio
    use bio member to pass to libcrypto function
    """
    def __init__(self, data=None):
        """
        If data is specified, creates read-only BIO. If data is
        None, creates writable BIO, contents of which can be retrieved
        by str() or unicode()
        """
        if data is None:
            self.bio = backend._create_mem_bio_gc()
        else:
            self.bio = backend._bytes_to_bio(data)

    def __del__(self):
        """
        Cleans up memory used by bio
        """
        # libcrypto.BIO_free(self.bio)
        del self.bio

    def __str__(self):
        """
        Returns current contents of buffer as byte string
        """
        return backend._read_mem_bio(self.bio)
        # result_buffer = ffi.new('char**')
        # buffer_length = libcrypto.BIO_get_mem_data(self.bio, result_buffer)
        # return ffi.buffer(result_buffer[0], buffer_length)[:]

    def __unicode__(self):
        """
        Attempts to interpret current contents of buffer as UTF-8 string
        and convert it to unicode
        """
        return str(self).decode("utf-8")

    def read(self, length=None):
        """
        Reads data from readble BIO. For test purposes.
        @param length - if specifed, limits amount of data read.
        If not BIO is read until end of buffer
        """
        return backend._read_mem_bio(self.bio.bio)
        if not length is None:
            if not isinstance(length, (int, long)):
                raise TypeError("length to read should be number")
            buf = ffi.new('char[]', length)
            readbytes = libcrypto.BIO_read(self.bio, buf, length)
            if readbytes == -2:
                raise NotImplementedError("Function is not supported by" +
                                          "this BIO")
            if readbytes == -1:
                raise IOError
            if readbytes == 0:
                return ""
            return ffi.string(buf, readbytes)
        else:
            buf = ffi.new('char[]', 1024)
            out = ""
            readbytes = 1
            while readbytes > 0:
                readbytes = libcrypto.BIO_read(self.bio, buf, 1024)
                if readbytes == -2:
                    raise NotImplementedError("Function is not supported by " +
                                              "this BIO")
                if readbytes == -1:
                    raise IOError
                if readbytes > 0:
                    out += ffi.string(buf, readbytes)
            return out

    def write(self, data):
        """
        Writes data to writable bio. For test purposes
        """
        if isinstance(data, unicode):
            data = data.encode("utf-8")
        else:
            data = str(data)

        written = libcrypto.BIO_write(self.bio, data, len(data))
        if written == -2:
            raise NotImplementedError("Function not supported by this BIO")
        if written < len(data):
            raise IOError("Not all data were successfully written")

    def reset(self):
        """
        Resets the read-only bio to start and discards all data from
        writable bio
        """
        libcrypto.BIO_ctrl(self.bio, 1, 0, None)

__all__ = ['Membio']
# libcrypto.BIO_s_mem.restype = c_void_p
# libcrypto.BIO_new.restype = c_void_p
# libcrypto.BIO_new.argtypes = (c_void_p, )
# libcrypto.BIO_ctrl.restype = c_long
# libcrypto.BIO_ctrl.argtypes = (c_void_p, c_int, c_long, POINTER(c_char_p))
# libcrypto.BIO_read.argtypes = (c_void_p, c_char_p, c_int)
# libcrypto.BIO_write.argtypes = (c_void_p, c_char_p, c_int)
# libcrypto.BIO_free.argtypes = (c_void_p, )
# libcrypto.BIO_new_mem_buf.restype = c_void_p
# libcrypto.BIO_new_mem_buf.argtypes = (c_char_p, c_int)
