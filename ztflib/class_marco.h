#pragma once

#include <mutex>

#ifndef DISALLOW_COPY_AND_ASSIGN
#if LANG_CXX11
#define DISALLOW_COPY_AND_ASSIGN(classname) \
private:                                    \
    classname(const classname &) = delete;  \
    classname &operator=(const classname &) = delete
#else
#define DISALLOW_COPY_AND_ASSIGN(classname) \
private:                                    \
    classname(const classname &);           \
    classname &operator=(const classname &)
#endif
#endif