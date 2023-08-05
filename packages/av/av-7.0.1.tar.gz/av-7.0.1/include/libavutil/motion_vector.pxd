from libc.stdint cimport (
    uint8_t, int8_t,
    uint16_t, int16_t,
    uint32_t, int32_t,
    uint64_t, int64_t
)


cdef extern from "libavutil/motion_vector.h" nogil:

    cdef struct AVMotionVector:
        int32_t     source
        uint8_t     w
        uint8_t     h
        int16_t     src_x
        int16_t     src_y
        int16_t     dst_x
        int16_t     dst_y
        uint64_t    flags
        int32_t     motion_x
        int32_t     motion_y
        uint16_t    motion_scale
